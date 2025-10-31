
import os
import pandas as pd
from backend.optimization.optimization_run import run_optimization

def test_certificates_block_selection(tmp_path):
    # create minimal csv with one invalid cert
    p = tmp_path / "trainsets.csv"
    df = pd.DataFrame([
        {"trainset_id":"TS1","mileage_km":20000,"cert_days_left_rolling_stock":10,"cert_days_left_signalling":10,"cert_days_left_telecom":10,"certificate_valid":1},
        {"trainset_id":"TS2","mileage_km":21000,"cert_days_left_rolling_stock":0,"cert_days_left_signalling":10,"cert_days_left_telecom":10,"certificate_valid":0},
        {"trainset_id":"TS3","mileage_km":22000,"cert_days_left_rolling_stock":5,"cert_days_left_signalling":5,"cert_days_left_telecom":5,"certificate_valid":1},
    ])
    df.to_csv(p, index=False)
    res = run_optimization(str(p), jobcards_csv=None, model_path=None, min_peak_trainsets=2)
    # TS2 should not be selected
    assert "TS2" not in res["selected_trainsets"]
