"""
Bootstrap confidence intervals for World Happiness Report 2019.

Writes (repo root):
  outputs/bootstrap_results.txt

Methods:
  - 95% CI for mean(Score)
  - 95% CI for corr(Score, GDP per capita)
  - 95% CI for mean difference in Score between Top10 and Bottom20 countries
"""

from pathlib import Path
import numpy as np
import pandas as pd

# ---------- Paths (repo-root aware) ----------
THIS_FILE = Path(__file__).resolve()
ROOT = THIS_FILE.parent.parent
DATA_PATH = ROOT / "data" / "world_happiness_2019.csv"
OUT_PATH = ROOT / "outputs" / "bootstrap_results.txt"

# ---------- Config ----------
SEED = 42
N_BOOT = 5000
rng = np.random.default_rng(SEED)

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

def ensure_dirs():
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

def load_data() -> pd.DataFrame:
    print(f"[INFO] Loading: {DATA_PATH}")
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}\nFound: {list(df.columns)}")
    for c in REQUIRED_COLS[1:]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=REQUIRED_COLS[1:])
    print(f"[INFO] Rows after dropna on numeric cols: {len(df)}")
    return df

def ci_from_bootstrap(samples: np.ndarray, alpha: float = 0.05):
    lo, hi = np.percentile(samples, [100*alpha/2, 100*(1 - alpha/2)])
    return float(lo), float(hi)

def boot_mean(values: np.ndarray, n_boot: int = N_BOOT):
    vals = np.asarray(values)
    boots = [rng.choice(vals, size=len(vals), replace=True).mean() for _ in range(n_boot)]
    return np.mean(boots), ci_from_bootstrap(boots)

def boot_corr(x: np.ndarray, y: np.ndarray, n_boot: int = N_BOOT):
    x = np.asarray(x); y = np.asarray(y)
    n = len(x)
    boots = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        boots.append(np.corrcoef(x[idx], y[idx])[0, 1])
    return np.mean(boots), ci_from_bootstrap(boots)

def boot_meandiff(a: np.ndarray, b: np.ndarray, n_boot: int = N_BOOT):
    a = np.asarray(a); b = np.asarray(b)
    na, nb = len(a), len(b)
    boots = []
    for _ in range(n_boot):
        ma = rng.choice(a, size=na, replace=True).mean()
        mb = rng.choice(b, size=nb, replace=True).mean()
        boots.append(ma - mb)
    return np.mean(boots), ci_from_bootstrap(boots)

def main():
    ensure_dirs()
    df = load_data()

    lines = []
    lines.append("===== BOOTSTRAP RESULTS (95% CI; N_BOOT = {}) =====".format(N_BOOT))

    # 1) Mean Score CI
    mean_est, (lo, hi) = boot_mean(df["Score"].values)
    lines.append(f"\nMean(Score): {mean_est:.3f}  CI95=({lo:.3f}, {hi:.3f})")

    # 2) Corr(Score, GDP) CI
    corr_est, (lo, hi) = boot_corr(df["Score"].values, df["GDP per capita"].values)
    lines.append(f"Corr(Score, GDP per capita): {corr_est:.3f}  CI95=({lo:.3f}, {hi:.3f})")

    # 3) Mean difference Top10 vs Bottom20 (by Score)
    top10 = df.nlargest(10, "Score")["Score"].values
    bottom20 = df.nsmallest(20, "Score")["Score"].values
    md_est, (lo, hi) = boot_meandiff(top10, bottom20)
    lines.append(f"MeanDiff(Top10 - Bottom20) Score: {md_est:.3f}  CI95=({lo:.3f}, {hi:.3f})")

    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[WRITE] {OUT_PATH}")

if __name__ == "__main__":
    main()
