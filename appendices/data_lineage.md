# Data Lineage — World Happiness Report 2019

## Source
- **Dataset:** World Happiness Report 2019  
- **Publisher / Collector:** SDSN / Gallup World Poll  
- **Acquisition:** [Kaggle link](https://www.kaggle.com/datasets/unsdsn/world-happiness)  
- **PII:** None — country-level aggregates only  

## Schema (Key Columns)
- Country or region (string)  
- Score (float, 0–10 happiness score)  
- GDP per capita, Social support, Healthy life expectancy, Freedom, Generosity, Corruption perception (float indices)  
- Rows: 156 countries, Year: 2019  

## Transformations
- Loaded CSV into Pandas (`basic_stats.py`).  
- Checked dtypes, no missingness in key vars.  
- Generated descriptive stats + Top/Bottom 10 scores.  
- Created factual answers (`factual_answers.json`) to compare with LLM outputs.  

## Limitations
- One year only (2019) → no trends.  
- Indicators are survey-based → cultural bias possible.  
- Country-level only → cannot infer individual outcomes.  

## Reproducibility
- Place dataset in `data/world_happiness_2019.csv` (gitignored).  
- Run scripts in `scripts/` to regenerate stats, uncertainty, fairness, robustness.  
- Outputs: `outputs/` (logs), `visuals/` (figures).  
