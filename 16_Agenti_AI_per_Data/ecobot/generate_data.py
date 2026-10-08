"""Generatore della consegna start2impact: formule e anomalie preservate.

L'unica aggiunta metodologica è il seed 42 prima dello script ufficiale.
La data finale usa datetime.today(), come nella traccia: conserva i CSV generati.
"""
from pathlib import Path
from datetime import datetime
import json
import hashlib
import pandas as pd
import numpy as np


def generate(destination: Path):
    destination.mkdir(parents=True, exist_ok=True)
    np.random.seed(42)
    dates = pd.date_range(end=datetime.today(), periods=24*30, freq="h")
    production = np.maximum(0, np.sin((dates.hour.to_numpy() - 6) * np.pi / 12) * 5 + np.random.normal(0, 0.5, len(dates)))
    production[dates.hour < 6] = 0
    production[dates.hour > 20] = 0
    df_prod = pd.DataFrame({"timestamp": dates, "kwh_produced": production})
    df_prod.loc[100:105, "kwh_produced"] = np.nan
    df_prod.loc[200, "kwh_produced"] = -5
    consumption = np.random.normal(1.5, 0.5, len(dates))
    consumption[dates.hour.isin([19, 20, 21])] += 2
    df_cons = pd.DataFrame({"timestamp": dates, "kwh_consumed": consumption})
    files = {"solar_production_raw.csv": df_prod, "household_consumption.csv": df_cons}
    hashes = {}
    for name, frame in files.items():
        path = destination / name
        frame.to_csv(path, index=False)
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    manifest = {"seed": 42, "start": str(dates[0]), "end": str(dates[-1]), "rows_per_file": 720,
                "source": "Traccia ufficiale Agenti AI per Data, sezione Step preliminare - Dati, consultata 2026-10-07",
                "adaptation": "Seed 42; formule e anomalie originali. Timestamp finali dipendono dalla data di esecuzione.", "sha256": hashes}
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


if __name__ == "__main__":
    print(json.dumps(generate(Path(__file__).parent / "data"), indent=2))
