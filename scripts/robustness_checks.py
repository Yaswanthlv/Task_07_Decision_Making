"""
Robustness / Sensitivity Checks — World Happiness Report 2019

Writes (repo root):
  outputs/robustness_report.txt
  outputs/robustness_corr_pearson.csv
  outputs/robustness_corr_spearman.csv
"""

from pathlib import Path
import numpy as np
import pandas as pd

# -------- Paths (repo-root aware) --------
THIS_FILE = Path(__file__).resolve()
ROOT = THIS_FILE.parent.parent
DATA_PATH = ROOT / "data" / "world_happiness_2019.csv"
OUT_DIR = ROOT / "outputs"
P_REPORT = OUT_DIR / "robustness_report.txt"
P_PEARSON = OUT_DIR / "robustness_corr_pearson.csv"
P_SPEARMAN = OUT_DIR / "robustness_corr_spearman.csv"

SEED = 42
np.random.seed(SEED)

COLS = [
    "Country or region",
    "Score",
    "GDP per capita",
    "Social support",
    "Healthy life expectancy",
    "Freedom to make life choices",
    "Generosity",
    "Perceptions of corruption",
]

def ensure_dirs():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    missing = [c for c in COLS if c not in df.columns]
    if missing:
        raise ValueError(f"CSV missing columns: {missing}\nFound: {list(df.columns)}")
    for c in COLS[1:]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=COLS[1:])
    return df

def corr_rank_pearson(df: pd.DataFrame) -> pd.Series:
    # Correlation of each factor with Score (descending)
    return (
        df[COLS[1:]]
        .corr(numeric_only=True)["Score"]
        .drop("Score")
        .sort_values(ascending=False)
    )

def corr_rank_spearman(df: pd.DataFrame) -> pd.Series:
    return (
        df[COLS[1:]]
        .corr(method="spearman", numeric_only=True)["Score"]
        .drop("Score")
        .sort_values(ascending=False)
    )

def minmax(s: pd.Series) -> pd.Series:
    rng = s.max() - s.min()
    return (s - s.min()) / rng if rng != 0 else s * 0.0

def write_text(path: Path, text: str):
    path.write_text(text, encoding="utf-8")
    print(f"[WRITE] {path}")

def main():
    ensure_dirs()
    df = load_data()

    lines = []
    lines.append("===== ROBUSTNESS / SENSITIVITY CHECKS =====")
    lines.append(f"Rows analyzed: {len(df)}")

    # -------- Baseline Pearson correlation ranking --------
    pearson = corr_rank_pearson(df)
    pearson.to_csv(P_PEARSON, header=["pearson_corr"])
    lines.append("\n-- Baseline Pearson correlation rank (Score vs. factors) --")
    lines.append(pearson.to_string())

    # -------- Drop top-N by Score and recompute --------
    for n in (3, 5):
        dfd = df.drop(df.nlargest(n, "Score").index)
        pr = corr_rank_pearson(dfd)
        mean_score = dfd["Score"].mean()
        lines.append(f"\n-- After dropping top {n} Score countries --")
        lines.append(f"Mean Score: {mean_score:.3f}")
        lines.append("Pearson correlation rank:")
        lines.append(pr.to_string())

    # -------- Min-max normalize Score and recompute --------
    dfn = df.copy()
    dfn["Score_norm"] = minmax(dfn["Score"])
    pearson_norm = (
        dfn[["GDP per capita", "Social support", "Healthy life expectancy",
             "Freedom to make life choices", "Generosity", "Perceptions of corruption", "Score_norm"]]
        .corr(numeric_only=True)["Score_norm"]
        .drop("Score_norm")
        .sort_values(ascending=False)
    )
    lines.append("\n-- Using min-max normalized Score --")
    lines.append(f"Mean(Score_norm): {dfn['Score_norm'].mean():.3f}")
    lines.append(pearson_norm.to_string())

    # -------- Spearman (rank-based) correlation ranking --------
    spearman = corr_rank_spearman(df)
    spearman.to_csv(P_SPEARMAN, header=["spearman_corr"])
    lines.append("\n-- Spearman correlation rank (rank-based robustness) --")
    lines.append(spearman.to_string())

    # -------- Stability summary --------
    def top(series: pd.Series) -> str:
        return series.index[0]

    lines.append("\n-- Stability Summary --")
    lines.append(f"Top factor (baseline Pearson): {top(pearson)}")
    lines.append(f"Top factor (drop-3): {top(corr_rank_pearson(df.drop(df.nlargest(3, 'Score').index)))}")
    lines.append(f"Top factor (drop-5): {top(corr_rank_pearson(df.drop(df.nlargest(5, 'Score').index)))}")
    lines.append(f"Top factor (Pearson on Score_norm): {top(pearson_norm)}")
    lines.append(f"Top factor (Spearman): {top(spearman)}")

    # -------- Save combined report --------
    write_text(P_REPORT, "\n".join(lines) + "\n")

if __name__ == "__main__":
    main()
