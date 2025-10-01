"""
Recreate descriptive stats and core visuals for World Happiness Report 2019.
This version is verbose and verifies every write.

Writes to repo-root:
  outputs/basic_stats.txt
  outputs/top10_by_score.txt
  outputs/bottom10_by_score.txt
  outputs/correlations_with_score.txt
  visuals/score_histogram.png
  visuals/gdp_vs_score_scatter.png
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# -------- Paths (repo-root aware) --------
THIS_FILE = Path(__file__).resolve()
ROOT = THIS_FILE.parent.parent             # repo root = .../Banda07
DATA_PATH = ROOT / "data" / "world_happiness_2019.csv"
OUT_DIR = ROOT / "outputs"
VIS_DIR = ROOT / "visuals"

SEED = 42
np.random.seed(SEED)

REQUIRED_COLS = [
    "Country or region",
    "Score",
    "GDP per capita",
    "Social support",
    "Healthy life expectancy",
    "Freedom to make life choices",
    "Generosity",
    "Perceptions of corruption",
]

# Expected artifact paths
P_BASIC   = OUT_DIR / "basic_stats.txt"
P_TOP10   = OUT_DIR / "top10_by_score.txt"
P_BOTTOM  = OUT_DIR / "bottom10_by_score.txt"
P_CORRS   = OUT_DIR / "correlations_with_score.txt"
P_HIST    = VIS_DIR / "score_histogram.png"
P_SCATTER = VIS_DIR / "gdp_vs_score_scatter.png"

def ensure_dirs():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    VIS_DIR.mkdir(parents=True, exist_ok=True)

def load_and_validate():
    print(f"[INFO] Repo root: {ROOT}")
    print(f"[INFO] Looking for dataset at: {DATA_PATH}")
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found:\n  {DATA_PATH}\n"
            "Place the CSV at repo_root/data/world_happiness_2019.csv"
        )
    df = pd.read_csv(DATA_PATH)
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(
            "CSV is missing required columns:\n"
            f"  Missing: {missing}\n"
            f"  Found: {list(df.columns)}"
        )
    # Coerce numeric columns
    for c in REQUIRED_COLS[1:]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=REQUIRED_COLS[1:])
    print(f"[INFO] Loaded rows: {len(df)}  (after dropping NAs in required numeric cols)")
    return df

def write_text(path: Path, text: str):
    path.write_text(text, encoding="utf-8")
    print(f"[WRITE] {path}")

def save_and_check(fig_path: Path):
    if not fig_path.parent.exists():
        fig_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(fig_path, dpi=200)
    plt.close()
    if not fig_path.exists():
        raise RuntimeError(f"[ERROR] Expected image not found after save: {fig_path}")
    print(f"[WRITE] {fig_path}")

def dir_list(p: Path) -> str:
    if not p.exists():
        return f"(dir missing) {p}"
    items = sorted([str(x.name) for x in p.iterdir()])
    return f"{p} -> {items}"

def main():
    ensure_dirs()
    df = load_and_validate()

    # -------- Basic stats --------
    lines = []
    lines.append("===== DATA SHAPE =====")
    lines.append(f"Rows: {len(df)}, Columns: {len(df.columns)}")
    lines.append("\n===== DTYPE SCHEMA =====")
    lines.append(df[REQUIRED_COLS].dtypes.to_string())
    lines.append("\n===== DESCRIPTIVE STATS (NUMERIC) =====")
    desc = df[REQUIRED_COLS[1:]].describe()
    lines.append(desc.to_string())
    write_text(P_BASIC, "\n".join(lines))

    # -------- Top/Bottom tables by Score --------
    top10 = df.nlargest(10, "Score")[["Country or region", "Score"]]
    bottom10 = df.nsmallest(10, "Score")[["Country or region", "Score"]]
    write_text(P_TOP10, top10.to_string(index=False))
    write_text(P_BOTTOM, bottom10.to_string(index=False))

    # -------- Correlations with Score --------
    corrs = df[REQUIRED_COLS[1:]].corr(numeric_only=True)["Score"].sort_values(ascending=False)
    write_text(P_CORRS, corrs.to_string())

    # -------- Visuals (matplotlib; one plot per figure; no custom colors) --------
    # 1) Histogram of Score
    plt.figure()
    df["Score"].plot(kind="hist", bins=20)
    plt.title("Distribution of Happiness Score (2019)")
    plt.xlabel("Score")
    plt.ylabel("Count")
    save_and_check(P_HIST)

    # 2) Scatter: GDP per capita vs Score
    plt.figure()
    plt.scatter(df["GDP per capita"], df["Score"])
    plt.title("GDP per capita vs Happiness Score (2019)")
    plt.xlabel("GDP per capita (index)")
    plt.ylabel("Happiness Score")
    save_and_check(P_SCATTER)

    # Final listing
    print("[DONE] Text outputs:")
    print("  " + dir_list(OUT_DIR))
    print("[DONE] Figures:")
    print("  " + dir_list(VIS_DIR))

if __name__ == "__main__":
    main()
