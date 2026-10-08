"""Legge dati UCI e output salvati del notebook; non esegue celle né addestra modelli.

Uso: python aggrega-dati.py /percorso/wine.data /percorso/notebook.ipynb
"""
from pathlib import Path
import argparse
import base64
import collections
import csv
import hashlib
import json
import re
import statistics

parser = argparse.ArgumentParser()
parser.add_argument("csv", type=Path)
parser.add_argument("notebook", type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parent
features = ["alcohol", "malic_acid", "ash", "alcalinity_of_ash", "magnesium",
            "total_phenols", "flavanoids", "nonflavanoid_phenols", "proanthocyanins",
            "color_intensity", "hue", "od280/od315_of_diluted_wines", "proline"]
rows = []
with args.csv.open() as f:
    for row in csv.reader(f):
        assert len(row) == 14
        rows.append({"target": int(row[0])-1, **dict(zip(features, map(float, row[1:])))})
assert len(rows) == 178
assert len({tuple(row.values()) for row in rows}) == 178
counts = collections.Counter(r["target"] for r in rows)
assert dict(counts) == {0: 59, 1: 71, 2: 48}

notebook = json.loads(args.notebook.read_text())
cells = notebook["cells"]
def output_text(index):
    parts = []
    for out in cells[index].get("outputs", []):
        text = out.get("text", out.get("data", {}).get("text/plain", ""))
        parts.append("".join(text))
    return "\n".join(parts)

assert "df_results_ss" in "".join(cells[44]["source"])
benchmark = []
for line in output_text(44).splitlines():
    match = re.fullmatch(r"\s*\d+\s+(\w+)\s+([\d.]+)\s+([\d.]+)\s*", line)
    if match:
        benchmark.append({"model": match[1], "mean": float(match[2]), "std": float(match[3])})
assert len(benchmark) == 6

assert "best_lda_rs" in "".join(cells[63]["source"])
report = output_text(63)
test_classes = []
for line in report.splitlines():
    match = re.fullmatch(r"\s*Class (\d)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+(\d+)\s*", line)
    if match:
        test_classes.append({"class": int(match[1]), "precision": float(match[2]),
                             "recall": float(match[3]), "f1": float(match[4]), "support": int(match[5])})
assert len(test_classes) == 3 and sum(r["support"] for r in test_classes) == 36
images = [out["data"]["image/png"] for out in cells[63].get("outputs", [])
          if "image/png" in out.get("data", {})]
assert len(images) == 1
(root / "matrice-originale.png").write_bytes(base64.b64decode("".join(images[0])))

result = {
    "rows": len(rows), "features": len(features), "class_counts": dict(counts),
    "profiles": [{key: r[key] for key in ["target", "flavanoids", "proline"]} for r in rows],
    "class_means": {str(cls): {key: statistics.mean(r[key] for r in rows if r["target"] == cls)
                               for key in ["flavanoids", "proline", "color_intensity"]} for cls in counts},
    "standard_scaler_cv_5fold": benchmark,
    "lda_report": test_classes,
    "lda_repeated_cv_output": output_text(74),
    "rf_repeated_cv_output": output_text(104)}
(root / "risultati.json").write_text(json.dumps(result, indent=2) + "\n")
indices = [18, 32, 36, 44, 45, 50, 57, 59, 63, 74, 79, 86, 95, 99, 101, 104]
(root / "risultati-originali.txt").write_text("\n\n".join(f"CELLA {i}\n{output_text(i)}" for i in indices) + "\n")
sources = {
    "dataset": "https://archive.ics.uci.edu/dataset/109/wine",
    "dataset_citation": "Aeberhard, S. & Forina, M. (1992). Wine. UCI Machine Learning Repository. DOI: 10.24432/C5PC7J",
    "dataset_license": "CC BY 4.0",
    "csv": args.csv.name, "csv_sha256": hashlib.sha256(args.csv.read_bytes()).hexdigest(),
    "notebook": args.notebook.name, "notebook_sha256": hashlib.sha256(args.notebook.read_bytes()).hexdigest(),
    "notebook_cells": len(cells),
    "source_cells": {"benchmark_standard": 44, "benchmark_robust": 45, "lda_matrix_and_report": 63,
                     "rf_feature_importances": 101, "lda_repeated_cv": 74, "rf_repeated_cv": 104},
    "notes": ["Il dataset UCI usa classi 1–3; qui convertite in 0–2 come scikit-learn e il notebook.",
              "Confronto modelli ricostruito dagli output salvati, non da un nuovo addestramento.",
              "Matrice originale estratta senza modifiche dall'output PNG della cella 63.",
              "Benchmark su 5 fold; la CV ripetuta è 5 fold per 10 ripetizioni, non nested CV.",
              "Test di 36 campioni consultato più volte nel notebook: non una valutazione esterna indipendente."]}
(root / "fonti.json").write_text(json.dumps(sources, ensure_ascii=False, indent=2) + "\n")
print("Verificati 178 campioni, 6 risultati del benchmark e report LDA su 36 campioni.")
