# Dissertation: Recurrent Financial Distress Prediction in Portuguese SMEs

## Research Overview

This project models recurring financial distress episodes in Portuguese SMEs using a
**multi-state survival analysis** framework, comparing classical statistical models against
machine learning and deep learning approaches.

The core contribution is framing the problem as a **multi-state model** with competing risks:
- **State 0 — Healthy:** Normal operations
- **State 1 — Transient Distress:** Recoverable distress (negative equity or EBITDA < interest)
- **State 2 — Terminal:** Legal dissolution, liquidation, or bankruptcy (absorbing state)

## Hypotheses

- **H1:** Adding Corporate Governance and Macroeconomic variables significantly reduces
  calibration error (Brier Score) and improves discrimination (C-Index) over financials alone.
- **H2:** DynamicDeepHit outperforms static models (Cox, RSF) by capturing the firm's
  financial memory through longitudinal trajectories.
- **H3:** Recurrence determinants (0→1 after a prior episode) are structurally different
  from first-episode determinants, as evidenced by Cox PWP stratified coefficients.

## Model Stack

| Model | Role | Key Feature |
|-------|------|-------------|
| Cox AG | Baseline | Andersen-Gill recurrent events |
| Cox PWP | Recurrence baseline | Stratified by episode number (Gap Time) |
| RSF | ML benchmark | Non-linearities + SHAP interpretability |
| DynamicDeepHit | Core innovation | LSTM encoder + cause-specific competing risks |

## Directory Structure

```
├── data/
│   ├── raw/          # Immutable source data (SABI exports, PORDATA/INE macro CSVs)
│   ├── interim/      # Intermediate transformations (micro_long, macro_consolidated)
│   ├── processed/    # Final merged dataset (final_survival_dataset.csv)
│   └── modeling/     # Model-ready feature sets by experiment (features_*.parquet)
│
├── notebooks/
│   ├── 01_eda_macro.ipynb           # PIB, Juros, Desemprego (Raw -> Interim)
│   ├── 02_eda_cleaning_micro.ipynb   # Limpeza SABI e Long-Format (Raw -> Interim)
│   ├── 03_feature_engineering.ipynb  # Rácios e Governance (Interim -> Interim)
│   ├── 04_survival_construction.ipynb # Multi-Estado + Lagging + Merge (Interim -> Processed)
│   └── 05_modeling_survival.ipynb    # Cox, RSF, DeepHit (Em breve)
│
├── src/
│   ├── data/
│   │   └── preprocessing.py   # Lag, winsorisation, multi-state restructure
│   ├── features/
│   │   └── engineering.py     # DTD, Governance Entropy, Macro-Beta
│   ├── models/
│   │   ├── cox_pwp.py
│   │   ├── rsf.py
│   │   └── dynamic_deephit.py
│   ├── evaluation/
│   │   ├── metrics.py         # C-Index, IBS, AUC, MCF, D-Calibration
│   │   └── plots.py           # Survival curves, calibration, SHAP
│   └── visualization/         # Thesis-specific EDA figures
│
├── models/            # Saved model artifacts (.pkl, .pt)
├── reports/figures/   # Generated plots for dissertation
├── tests/             # Unit tests
│
├── docs/
│   ├── planning/      # Research architecture (LaTeX source)
│   │   └── latex/     # Main LaTeX environment (ESTG Template)
│   │       └── sections/  # Modular chapters (Mathematics, Models, etc.)
│   ├── dissertation/  # Literature, article, proposal
│   └── templates/     # ESTG administrative templates
```

## Getting Started

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

## Key References

- Zhou et al. (2022) — Recurrence of financial distress: A survival analysis
- Lee et al. (2019) — DynamicDeepHit: longitudinal data with competing risks
- Borges & Carvalho (2024) — SME distress survival models (Portuguese context)
- Ptak-Chmielewska & Matuszyk (2020) — RSF for SME bankruptcy prediction
