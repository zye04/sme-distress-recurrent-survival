# Preprocessing pipeline for modeling
#
# Responsibilities:
#   1. Apply 1-year lag to all financial and macro covariates (prevent data leakage)
#   2. Winsorize continuous variables at P1-P99
#   3. Restructure final_survival_dataset.csv into multi-state counting process format:
#        State 0 (Healthy) | State 1 (Transient Distress: C1/C2) | State 2 (Terminal: C3)
#   4. Build feature sets for H1 experiment:
#        - features_financial_only
#        - features_financial_gov
#        - features_full (financial + governance + macro)
#   5. Time-based train/val/test split:
#        - Train : 2005-2018
#        - Val   : 2019-2021
#        - Test  : 2022-2023
#
# Output: data/modeling/features_*.parquet
