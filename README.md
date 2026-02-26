# Dissertation: Financial Distress Prediction in Portuguese SMEs

## Project Overview
This research project focuses on the prediction of corporate financial distress recurrence. It compares classical survival analysis models (Cox PH) against modern machine learning (RSF) and deep learning (DeepHit) techniques, using a dataset of Portuguese Small and Medium Enterprises (SMEs).

The primary goal is to build and validate superior models for predicting financial distress by incorporating financial, corporate governance, accounting quality, and macroeconomic variables.

## 📁 Directory Structure
Adopted a software engineering oriented structure for reproducibility and modularity:

- **data/**: Project datasets (Raw, Interim, Processed).
  - `raw/`: Original, immutable data.
  - `interim/`: Data in transformation (e.g., long-format for recurrence).
  - `processed/`: Final datasets ready for modeling.
- **docs/**: Academic documentation and literary resources.
  - `dissertation/`: Thesis text (LaTeX/Word).
  - `literature/`: Academic papers (PDFs) and research notes.
  - `proposal/`: Official research proposal and timelines.
  - `estg-masters/`: Preliminary articles and presentations.
- **src/**: Main source code of the project (Modular).
  - `data/`: Scripts for data gathering and wrangling.
  - `features/`: Feature engineering scripts (ratios, governance metrics).
  - `models/`: Model architecture definitions (Cox, RSF, DeepHit).
  - `visualization/`: Scripts for generating thesis figures and tables.
- **notebooks/**: Jupyter notebooks for EDA and prototyping.
- **models/**: Storage for trained machine learning models binaries.
- **reports/**: Generated figures, tables, and analysis outputs.
- **tests/**: Unit tests for code verification.

## 🚀 Getting Started
1. Create a virtual environment: `python -m venv venv`
2. Activate it: `source venv/bin/activate` (or `.\venv\Scripts\activate` on Windows)
3. Install dependencies: `pip install -r requirements.txt`

## 📊 Hypotheses
- **H1:** Governance and macro data improve C-Index.
- **H2:** RSF/DeepHit outperform Cox PH.
- **H3:** RSF/DeepHit are superior for predicting recurrence.
