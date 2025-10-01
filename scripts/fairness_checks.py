"""
Fairness / Subgroup Disparity Checks — World Happiness Report 2019

Writes (repo root):
  outputs/fairness_report.txt
  outputs/fairness_gdp_quartiles.csv
  outputs/fairness_corruption_tertiles.csv

Groups used (data-driven because 'Region' may not be present):
  - GDP per capita quartiles (Q1..Q4)
  - Perceptions of corruption tertiles (T1..T3), where higher = perceived LESS corrupt
"""

from pathlib import Path
import pandas as pd
import numpy as np

# ---------- Paths (repo-root aware) ----------
THIS_FILE = Path(__file__).resolve()
ROOT = THIS_FILE.parent.parent
DATA_PATH = ROOT / "data" / "world_happiness_2019.csv"

OUT_DIR = ROOT / "outputs"
P_REPORT = OUT_DIR / "fairness_report.txt"
P_GDPCSV = OUT_DIR / "fairness_gdp_quartiles.csv"
P_CORCSV = OUT_DIR / "fairness_corruption_tertiles.csv"

REQUIRED_COLS = [
    "Country or region",
    "Score",
    "GDP per capita",
    "Perceptions of corruption",
]

def ensure_dirs():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"CSV missing required columns: {missing}\nFound: {list(df.columns)}")
    # Coerce numerics
    for c in ["Score", "GDP per capita", "Perceptions of corruption"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["Score", "GDP per capita", "Perceptions of corruption"])
    return df

def summarize_group(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    out = (
        df.groupby(group_col)["Score"]
          .agg(count="count", mean="mean", std="std")
          .reset_index()
          .sort_values("mean", ascending=False)
    )
    return out

def main():
    ensure_dirs()
    df = load_data()

    lines = []
    lines.append("===== FAIRNESS / SUBGROUP DISPARITY CHECKS =====")
    lines.append(f"Rows analyzed: {len(df)}")

    # -------- GDP per capita quartiles --------
    df["gdp_quartile"] = pd.qcut(
        df["GDP per capita"], 4,
        labels=["Q1 (lowest)", "Q2", "Q3", "Q4 (highest)"]
    )
    gdp_tbl = summarize_group(df, "gdp_quartile")
    gdp_gap = gdp_tbl["mean"].max() - gdp_tbl["mean"].min()

    lines.append("\n-- Score by GDP per capita quartile --")
    lines.append(gdp_tbl.to_string(index=False))
    lines.append(f"Mean score disparity (Q4 - Q1): {gdp_gap:.3f}")
    gdp_tbl.to_csv(P_GDPCSV, index=False)

    # -------- Corruption perception tertiles --------
    # Higher values = perceived less corrupt
    df["corruption_tertile"] = pd.qcut(
        df["Perceptions of corruption"], 3,
        labels=["T1 (more corrupt)", "T2", "T3 (less corrupt)"]
    )
    cor_tbl = summarize_group(df, "corruption_tertile")
    cor_gap = cor_tbl["mean"].max() - cor_tbl["mean"].min()

    lines.append("\n-- Score by Perceptions of corruption tertile --")
    lines.append(cor_tbl.to_string(index=False))
    lines.append(f"Mean score disparity (T3 - T1): {cor_gap:.3f}")
    cor_tbl.to_csv(P_CORCSV, index=False)

    # -------- Brief interpretation hints --------
    lines.append("\nNotes:")
    lines.append("- Quartiles/tertiles are data-driven and not fixed thresholds.")
    lines.append("- Disparity = difference between highest and lowest group means.")
    lines.append("- These results are descriptive (observational) and not causal.")

    P_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[WRITE] {P_REPORT}")
    print(f"[WRITE] {P_GDPCSV}")
    print(f"[WRITE] {P_CORCSV}")

if __name__ == "__main__":
    main()
