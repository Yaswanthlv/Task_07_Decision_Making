# Task 07 — Decision Making, Ethics, and Reliability
 
**Course Research Assignment:** Research Task 07 — Ethical Implications of Decision Making

---

## 📌 Overview
This repository contains the full workflow and deliverables for **Task 07: Ethical Implications of Decision Making**.  
The task builds on prior work in **Task 05 (Descriptive Statistics)** and **Task 06 (Deep Fake / LLM Narrative)**, and extends them into a **stakeholder-facing decision report** with emphasis on:
- Ethical and legal considerations  
- Reproducibility and auditability  
- LLM transparency and reliability  

The project analyzes the **World Happiness Report 2019 dataset** and produces reproducible code, outputs, and documentation to support transparent, risk-tiered recommendations.

---

## 🎯 Task Requirements (from prompt)
According to the official assignment instructions【272†Research_Task_07.docx†L14-L56】, this task required:
1. Define **stakeholder & decision context**.  
2. Document **data provenance & scope**.  
3. Re-create and validate **descriptive results** (stats + visuals).  
4. Capture **LLM prompts & transcripts**, including annotated edits.  
5. **Quantify uncertainty** (bootstrap, CIs).  
6. Run **sanity checks & domain validation**.  
7. Conduct **bias & fairness checks**.  
8. Test **robustness & sensitivity**.  
9. Produce **tiered recommendations** (low/medium/high risk).  
10. Write a **stakeholder report** with uncertainty, ethical concerns, and clear labeling of any LLM text.  
11. Archive everything in a public repo with supporting scripts, outputs, and README.  

---

## 📂 Repository Structure

```
Banda07/
├── appendices/
│   └── data_lineage.md          # Data provenance, schema, reproducibility steps
├── data/
│   └── world_happiness_2019.csv # Input dataset
├── llm_outputs/
│   ├── llm_outputs_raw.md       # All prompts & raw outputs (Task 05 & Task 06)
│   └── llm_outputs_annotated.md # Annotated outputs (edits & rationale)
├── outputs/
│   ├── basic_stats.txt          # Descriptive statistics
│   ├── bootstrap_results.txt    # Confidence intervals for mean & correlation
│   ├── fairness_report.txt      # Subgroup disparities (GDP quartiles, corruption tertiles)
│   ├── robustness_report.txt    # Sensitivity checks
│   ├── top10_by_score.txt       # Top 10 countries by happiness score
│   └── bottom10_by_score.txt    # Bottom 10 countries by happiness score
├── scripts/
│   ├── reproduce_stats.py       # Reproduce descriptive stats & visuals
│   ├── bootstrap_ci.py          # Bootstrap CIs for mean & GDP correlation
│   ├── fairness_checks.py       # Bias/fairness analysis
│   └── robustness_checks.py     # Robustness & sensitivity analysis
├── visuals/
│   ├── score_histogram.png      # Distribution of happiness scores
│   └── gdp_vs_score_scatter.png # GDP vs Happiness scatterplot
├── Stakeholder_Report.md        # Final decision report
├── README.md                    # (this file)
└── .gitignore                   # Ignore caches, temp files, outputs, etc.
```

---

## 🧾 Key Deliverables

- **Stakeholder Report** (`Stakeholder_Report.md`):  
  Provides executive summary, findings, tiered recommendations, and ethical/legal considerations.  

- **Data Lineage** (`appendices/data_lineage.md`):  
  Documents provenance (Kaggle WHR 2019), schema, and reproducibility steps.  

- **LLM Outputs** (`llm_outputs/`):  
  Raw prompts/responses + annotated edits for transparency.  

- **Scripts** (`scripts/`):  
  Fully reproducible Python scripts with fixed seeds.  

- **Outputs & Visuals** (`outputs/`, `visuals/`):  
  Statistical results, fairness gaps, robustness checks, histograms, scatterplots.  

---

## ⚖️ Ethics & Transparency
- No personally identifiable information (PII) was used.  
- LLM outputs are archived separately and labeled.  
- All code, data lineage, and uncertainty estimates are included for auditability.  
- Limitations: single-year dataset; correlations cannot imply causality.  

---

## 🚀 How to Reproduce
1. Clone the repo.  
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
   (Requires: pandas, numpy, matplotlib, seaborn, scikit-learn).  
3. Run scripts from repo root:  
   ```bash
   python scripts/reproduce_stats.py
   python scripts/bootstrap_ci.py
   python scripts/fairness_checks.py
   python scripts/robustness_checks.py
   ```
4. Outputs will be stored in `outputs/`, visuals in `visuals/`.

---

## 📬 Submission Notes
- Repo title: **Task_07_Decision_Making**  
- Author: **Yaswanth Lalpet Vari**  

---
