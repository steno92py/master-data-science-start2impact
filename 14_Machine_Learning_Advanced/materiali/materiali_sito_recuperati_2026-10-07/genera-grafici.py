from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

root = Path(__file__).resolve().parent
d = json.loads((root / "risultati.json").read_text())
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#cccccc", "text.color": "#202020", "axes.labelcolor": "#444444",
    "xtick.color": "#444444", "ytick.color": "#444444"})
colors = ["#c52c54", "#177f80", "#63558a"]
fig, ax = plt.subplots(figsize=(10, 6), layout="constrained")
for cls, color, marker in zip(range(3), colors, ["o", "s", "^"]):
    rows = [r for r in d["profiles"] if r["target"] == cls]
    ax.scatter([r["proline"] for r in rows], [r["flavanoids"] for r in rows],
               color=color, marker=marker, s=43, alpha=.85, edgecolors="white", linewidths=.5,
               label=f"Classe {cls} · {len(rows)} campioni")
ax.set_title("Due misure chimiche, tre classi di vino", loc="left", weight="bold", pad=18)
ax.set_xlabel("Prolina · Valori del dataset"); ax.set_ylabel("Flavonoidi · Valori del dataset")
ax.set_ylim(bottom=0); ax.set_xlim(left=200)
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: str(int(x))))
ax.legend(frameon=False, loc="upper right"); ax.grid(alpha=.15); ax.set_axisbelow(True)
fig.savefig(root / "profili-chimici.png", dpi=160); plt.close(fig)

labels = {"LinearDiscriminant": "LDA", "RandomForest": "Random Forest", "SVM_RBF": "SVM RBF",
          "LogisticRegression": "Regressione logistica", "kNN": "k-NN", "GradientBoosting": "Gradient Boosting"}
fig, ax = plt.subplots(figsize=(10, 5.5), layout="constrained")
rows = d["standard_scaler_cv_5fold"]
for i, row in enumerate(rows):
    value = row["mean"]*100
    ax.barh(i, value, height=.58, color="#177f80")
    ax.text(value-1.4, i, f"{value:.2f}%".replace(".", ","), va="center", ha="right", weight="bold", color="white")
ax.set_yticks(range(len(rows)), [labels[r["model"]] for r in rows]); ax.invert_yaxis()
ax.set_xlim(0, 100); ax.grid(axis="x", alpha=.18); ax.set_axisbelow(True)
ax.set_title("Il confronto iniziale fra sei modelli", loc="left", weight="bold", pad=18)
ax.set_xlabel("Accuratezza media (%) · Validazione a 5 gruppi sui 142 campioni di training")
fig.savefig(root / "confronto-modelli.png", dpi=160); plt.close(fig)
print("Creati due grafici; la matrice LDA resta l'immagine originale del notebook.")
