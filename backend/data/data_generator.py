
"""
backend/data/generate_mock_data.py

Generates a realistic mock dataset for testing the optimizer.
"""
import pandas as pd
import numpy as np
import os

def generate(n=30, out_dir="../../data", seed=42):
    np.random.seed(seed)
    ids = [f"TS{str(i+1).zfill(3)}" for i in range(n)]
    locations = np.random.choice(["DepotA", "DepotB", "DepotC"], size=n, p=[0.5,0.3,0.2])
    mileage = np.random.randint(15000, 45000, size=n)
    cert_rs = np.random.randint(0, 31, size=n)  # days left
    cert_sig = np.random.randint(0, 31, size=n)
    cert_tel = np.random.randint(0, 31, size=n)
    branding_hours = np.random.randint(0, 10, size=n)
    branding_min = np.where(np.random.rand(n) < 0.6, 8, 0)  # 60% have contracts
    shunting = np.round(np.random.rand(n), 2)
    # mix some invalid certs and critical jobs
    critical_jobs = (np.random.rand(n) < 0.15).astype(int)
    # certificate_valid boolean if all certs > 0
    cert_valid = ((cert_rs > 0) & (cert_sig > 0) & (cert_tel > 0)).astype(int)
    df = pd.DataFrame({
        "trainset_id": ids,
        "location": locations,
        "mileage_km": mileage,
        "cert_days_left_rolling_stock": cert_rs,
        "cert_days_left_signalling": cert_sig,
        "cert_days_left_telecom": cert_tel,
        "branding_hours_today": branding_hours,
        "branding_min_hours": branding_min,
        "shunting_score": shunting,
        "critical_jobs_open": critical_jobs,
        "certificate_valid": cert_valid
    })
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "trainsets_mock.csv")
    df.to_csv(out, index=False)
    # also create a jobcards CSV for some critical jobs
    jobcards = []
    for i, tid in enumerate(ids):
        for j in range(np.random.poisson(0.3)):
            jobcards.append({"job_id": f"J{tid}_{j}", "trainset_id": tid, "priority": "critical" if np.random.rand() < 0.2 else "medium"})
    jc = pd.DataFrame(jobcards)
    jc.to_csv(os.path.join(out_dir, "jobcards_mock.csv"), index=False)
    print("Wrote", out, "and jobcards_mock.csv to", out_dir)

if __name__ == "__main__":
    generate()
