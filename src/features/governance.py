import pandas as pd
import numpy as np

def handle_governance_missingness(df):
    """
    Tratamento de Governance (OwnershipConcentration - 63% missing).
    Cria indicador de observabilidade (Sinal Preditivo de Transparência)
    e imputa mediana.
    """
    df = df.copy()
    if 'OwnershipConcentration' in df.columns:
        df['OwnershipConcentration_obs'] = df['OwnershipConcentration'].notna().astype(int)
        # Imputação neutra (mediana)
        median_val = df['OwnershipConcentration'].median()
        df['OwnershipConcentration'] = df['OwnershipConcentration'].fillna(median_val)
    return df
