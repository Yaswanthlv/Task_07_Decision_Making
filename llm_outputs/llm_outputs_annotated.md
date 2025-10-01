# Annotated LLM Outputs — Task 05 & Task 06

> This file documents the raw outputs produced by LLMs (Claude/ChatGPT) in Task 05 and Task 06, and annotates the edits made for Task 07 reporting.  
> All LLM-generated content is explicitly labeled.

---

## 1. Task 05 — Q&A on World Happiness Data

### Example Q1
**Prompt:**  
*"What are the top 5 countries by happiness score?"*  

**LLM Raw Output (Claude) [LLM-Generated]:**  
> The top 5 countries by happiness score are Finland, Denmark, Norway, Iceland, and Netherlands.  

**Edits for Accuracy:**  
- ✅ Verified against `factual_answers.json`. Correct — no edits.  
- ℹ️ Annotation: Marked as reliable because raw stats matched descriptive output from `basic_stats.py`.  

---

### Example Q2
**Prompt:**  
*"Does GDP per capita strongly correlate with happiness?"*  

**LLM Raw Output [LLM-Generated]:**  
> Yes, GDP per capita is the strongest factor driving happiness scores. Countries with higher GDP are always happier.  

**Edits for Accuracy:**  
- ❌ Removed “always happier” claim — too strong and causal.  
- ✅ Rewritten as: *“GDP per capita shows a positive correlation with happiness scores, but it is one of several factors (alongside social support, life expectancy, etc.).”*  
- ℹ️ Annotation: Changed to align with descriptive correlation stats and avoid overstating causality.  

---

## 2. Task 06 — Interview Script

### Excerpt 1
**LLM Raw Output [LLM-Generated]:**  
> Interviewer: *“How do you feel about the state of global happiness?”*  
> Respondent: *“It’s clear that money is the only thing that matters for happiness worldwide.”*  

**Edits for Balance:**  
- ❌ Removed “only thing that matters.”  
- ✅ Rewritten as: *“Many countries with higher income levels tend to report higher happiness, but social support and health also play strong roles.”*  
- ℹ️ Annotation: Adjusted to reflect multiple indices (social support, life expectancy).  

---

### Excerpt 2
**LLM Raw Output [LLM-Generated]:**  
> Respondent: *“Every region follows the same pattern — richer countries are always the happiest.”*  

**Edits for Accuracy:**  
- ❌ “Every region” and “always” → overgeneralization.  
- ✅ Rewritten as: *“In several regions, particularly Western Europe, higher GDP aligns with higher scores, but exceptions exist (e.g., some Latin American countries show high happiness despite lower GDP).”*  
- ℹ️ Annotation: Grounded with specific counterexamples, aligns with fairness checks.  

---

## 3. General Notes on Edits
- All **causal language** was softened to **correlational** (observational dataset).  
- Added **uncertainty qualifiers** (“tend to,” “often,” “exceptions exist”).  
- Ensured references to **multiple factors** (GDP, social support, health, freedom) instead of GDP-only narratives.  
- Marked each edit with ✅ (kept/modified) or ❌ (removed claim).  

---

## 4. Cross-Referencing
- Raw Q&A → see `llm_outputs_raw.md` and `outputs/factual_answers.json`.  
- Interview script → see Task 06 `interview_script.md`.  
- Annotations align with descriptive stats in `outputs/basic_stats.txt`.  
