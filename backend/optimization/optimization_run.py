"""
backend/optimization/optimization_run.py

PuLP-based induction optimizer for KMRL SIH25081 project.
"""
import os
import logging
from typing import Optional, Dict, Any
import pandas as pd
import numpy as np
import pickle
from pulp import LpProblem, LpVariable, LpBinary, lpSum, LpMaximize, LpStatus, PULP_CBC_CMD

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_WEIGHTS = {
    "service_readiness": 0.40,
    "punctuality_protection": 0.25,
    "maintenance_cost": 0.15,
    "revenue_protection": 0.12,
    "efficiency": 0.08
}

def safe_load_csv(path: str) -> pd.DataFrame:
    if not path or not os.path.exists(path):
        logger.warning("CSV not found: %s (returning empty DataFrame)", path)
        return pd.DataFrame()
    return pd.read_csv(path)

def compute_readiness_from_ml(df: pd.DataFrame, model_path: Optional[str]) -> pd.Series:
    n = len(df)
    if n == 0:
        return pd.Series(dtype=float)
    try:
        if model_path and os.path.exists(model_path):
            with open(model_path, "rb") as f:
                model = pickle.load(f)
            numeric = df.select_dtypes(include=[np.number]).fillna(0)
            if hasattr(model, "predict_proba"):
                preds = model.predict_proba(numeric)
                if preds.ndim == 2 and preds.shape[1] == 2:
                    readiness = preds[:,1]
                else:
                    readiness = np.array(preds, dtype=float)
            else:
                preds = model.predict(numeric)
                readiness = np.array(preds, dtype=float)
            readiness = np.clip(readiness, 0.0, 1.0)
            logger.info("Readiness computed from ML model at %s", model_path)
            return pd.Series(readiness, index=df.index)
    except Exception as e:
        logger.exception("ML readiness model failed to load/use: %s", e)

    cert_cols = [c for c in df.columns if "cert_days_left" in c]
    if len(cert_cols) == 0:
        if "certificate_valid" in df.columns:
            return df["certificate_valid"].fillna(0).astype(float)
        else:
            return pd.Series(0.5, index=df.index)
    cert_norms = []
    for c in cert_cols:
        v = df[c].fillna(0).astype(float)
        v = np.minimum(v, 30.0) / 30.0
        cert_norms.append(v)
    cert_score = pd.concat(cert_norms, axis=1).mean(axis=1)
    crit_col = None
    for c in ["critical_jobs_open", "n_critical_jobs", "open_critical_jobs"]:
        if c in df.columns:
            crit_col = c
            break
    if crit_col:
        crit = df[crit_col].fillna(0).astype(float)
        crit_score = 1.0 - (np.minimum(crit, 5) / 5.0)
    else:
        crit_score = 1.0
    readiness = 0.7 * cert_score + 0.3 * crit_score
    readiness = np.clip(readiness, 0.0, 1.0)
    logger.info("Readiness computed heuristically (no ML model)")
    return readiness

def normalize_series(s: pd.Series) -> pd.Series:
    if s.empty:
        return s
    mn = s.min()
    mx = s.max()
    if mx - mn < 1e-9:
        return pd.Series(0.0, index=s.index)
    return (s - mn) / (mx - mn)

def run_optimization(
    trainset_csv: str,
    jobcards_csv: str = None,
    model_path: Optional[str] = None,
    weights: Optional[Dict[str, float]] = None,
    min_peak_trainsets: int = 18,
    stabling_capacity_field: Optional[str] = "stabling_capacity",
    depot_field: Optional[str] = "location",
    id_field: str = "trainset_id",
    solver_time_limit: int = 30
) -> Dict[str, Any]:
    if weights is None:
        weights = DEFAULT_WEIGHTS.copy()
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("Weights must sum to > 0")
    weights = {k: float(v) / total for k, v in weights.items()}
    df_ts = safe_load_csv('data\trainsets.csv')
    df_jobs = safe_load_csv('data\jobcards.csv') if jobcards_csv else pd.DataFrame()
    if df_ts.empty:
        logger.error("No trainset data found at %s", trainset_csv)
        return {"selected_trainsets": [], "pulp_status": "NO_DATA", "objective_value": 0.0, "details": df_ts}
    if id_field not in df_ts.columns:
        possible_ids = [c for c in df_ts.columns if "train" in c.lower() and "id" in c.lower()]
        if possible_ids:
            id_field = possible_ids[0]
            logger.warning("Using %s as id_field", id_field)
        else:
            raise KeyError(f"Trainset ID column not found (expected '{id_field}')")
    if not df_jobs.empty:
        job_id_col = next((c for c in df_jobs.columns if "train" in c.lower() and "id" in c.lower()), None)
        if job_id_col is None:
            job_id_col = id_field
        critical_flag = None
        for c in ["priority", "priority_level", "is_critical"]:
            if c in df_jobs.columns:
                critical_flag = c
                break
        if critical_flag:
            crit_cond = df_jobs[critical_flag].astype(str).str.lower().isin(["critical", "1", "true", "yes"])
            crit_counts = df_jobs.loc[crit_cond].groupby(job_id_col).size().rename("critical_jobs_open")
            df_ts = df_ts.set_index(id_field).join(crit_counts).reset_index()
            df_ts["critical_jobs_open"] = df_ts["critical_jobs_open"].fillna(0).astype(int)
        else:
            counts = df_jobs.groupby(job_id_col).size().rename("open_jobs_count")
            df_ts = df_ts.set_index(id_field).join(counts).reset_index()
            df_ts["critical_jobs_open"] = (df_ts["open_jobs_count"].fillna(0) > 0).astype(int)
    else:
        df_ts["critical_jobs_open"] = df_ts.get("critical_jobs_open", 0).fillna(0).astype(int)
    df_ts["readiness"] = compute_readiness_from_ml(df_ts, model_path)
    if "withdrawal_risk" not in df_ts.columns:
        df_ts["withdrawal_risk"] = 1.0 - df_ts["readiness"]
    mileage_col = next((c for c in df_ts.columns if "mileage" in c.lower()), None)
    if mileage_col is None:
        df_ts["mileage_km"] = df_ts.get("mileage", 0).fillna(0).astype(float)
    else:
        df_ts["mileage_km"] = df_ts[mileage_col].fillna(0).astype(float)
    if "branding_hours_today" not in df_ts.columns:
        df_ts["branding_hours_today"] = df_ts.get("branding_hours", 0).fillna(0).astype(float)
    if "branding_min_hours" not in df_ts.columns:
        df_ts["branding_min_hours"] = 0.0
    prob = LpProblem("KMRL_Induction_Selection", LpMaximize)
    ids = df_ts[id_field].astype(str).tolist()
    x = {tid: LpVariable(f"x_{tid}", cat=LpBinary) for tid in ids}
    cert_flag = None
    for c in df_ts.columns:
        if "certificate_valid" in c.lower() or "cert_valid" in c.lower():
            cert_flag = c
            break
    if cert_flag:
        for _, row in df_ts.iterrows():
            if int(row.get(cert_flag, 0)) == 0:
                prob += x[str(row[id_field])] == 0, f"cert_required_{row[id_field]}"
    else:
        cert_days_cols = [c for c in df_ts.columns if "cert_days_left" in c]
        if len(cert_days_cols) >= 1:
            for _, row in df_ts.iterrows():
                if any(row.get(c, 999) <= 0 for c in cert_days_cols):
                    prob += x[str(row[id_field])] == 0, f"cert_days_required_{row[id_field]}"
        else:
            logger.warning("No certificate info found; can't enforce certificate hard constraint. Be careful!")
    for _, row in df_ts.iterrows():
        if int(row.get("critical_jobs_open", 0)) > 0:
            prob += x[str(row[id_field])] == 0, f"critical_jobs_block_{row[id_field]}"
    prob += lpSum([x[tid] for tid in ids]) >= int(min_peak_trainsets), "min_peak_trainsets"
    if depot_field in df_ts.columns and "depot_capacities.csv" in os.listdir(os.path.dirname(trainset_csv) or "."):
        try:
            depot_caps = pd.read_csv(os.path.join(os.path.dirname(trainset_csv), "depot_capacities.csv"))
            caps = depot_caps.set_index("location")["capacity"].to_dict()
            for loc, cap in caps.items():
                members = df_ts[df_ts[depot_field] == loc][id_field].astype(str).tolist()
                if members:
                    prob += lpSum([x[m] for m in members]) <= int(cap), f"depot_cap_{loc}"
        except Exception as e:
            logger.warning("Could not apply depot capacities: %s", e)
    readiness_norm = normalize_series(df_ts["readiness"])
    withdrawal_risk_norm = normalize_series(df_ts["withdrawal_risk"])
    mileage_dev = (df_ts["mileage_km"] - df_ts["mileage_km"].mean()).abs()
    mileage_norm = normalize_series(mileage_dev)
    branding_need = np.maximum(df_ts["branding_min_hours"] - df_ts["branding_hours_today"], 0.0)
    branding_norm = normalize_series(pd.Series(branding_need, index=df_ts.index))
    if "shunting_score" in df_ts.columns:
        efficiency_norm = normalize_series(df_ts["shunting_score"])
    else:
        efficiency_norm = pd.Series(0.5, index=df_ts.index)
    service_component = readiness_norm
    punctuality_component = 1.0 - withdrawal_risk_norm
    maintenance_component = 1.0 - mileage_norm
    revenue_component = 1.0 - branding_norm
    efficiency_component = efficiency_norm
    utility = (
        weights["service_readiness"] * service_component +
        weights["punctuality_protection"] * punctuality_component +
        weights["maintenance_cost"] * maintenance_component +
        weights["revenue_protection"] * revenue_component +
        weights["efficiency"] * efficiency_component
    )
    prob += lpSum([utility.iloc[i] * x[str(df_ts.iloc[i][id_field])] for i in range(len(df_ts))]), "Total_Utility"
    solver = PULP_CBC_CMD(timeLimit=solver_time_limit, msg=False)
    prob.solve(solver)
    status = LpStatus.get(prob.status, str(prob.status))
    selected = [tid for tid in ids if x[tid].value() == 1.0]
    objective_value = prob.objective.value() if prob.objective is not None else None
    df_ts["selected_for_induction"] = df_ts[id_field].astype(str).isin(selected).astype(int)
    df_ts["utility_score"] = utility.values
    logger.info("Optimization finished with status %s, objective %s, selected %d trainsets",
                status, objective_value, len(selected))
    return {
        "selected_trainsets": selected,
        "pulp_status": status,
        "objective_value": objective_value,
        "details": df_ts[[id_field, "selected_for_induction", "utility_score", "readiness", "withdrawal_risk", "mileage_km", "critical_jobs_open"] + ([depot_field] if depot_field in df_ts.columns else [])]
    }
