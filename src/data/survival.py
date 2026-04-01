import pandas as pd
import numpy as np

from src.data.base import safe_float
from src.features.governance import handle_governance_missingness

def prepare_multistate_data(df_micro, terminal_keywords=None):
    """
    Transforma dados micro long-format num dataset multi-estado (0, 1, 2) 
    com formato Counting Process (t_start, t_stop) e lagging de features.
    """
    if terminal_keywords is None:
        # Keywords atualizadas para bater com os valores reais do SABI
        terminal_keywords = [
            'Insolvência', 'Insolvente', 'Falência', 'Liquidação', 'Dissolução', 
            'Encerramento', 'Extinção', 'Encerrada', 'Trâmites de Composição'
        ]

    df = df_micro.copy()
    df = df.sort_values(['NIF Code', 'Year'])

    # 1. Tratamento de Governance (Isolado no seu módulo)
    df = handle_governance_missingness(df)

    # 2. Drop de colunas sem valor preditivo
    cols_to_drop = [c for c in ['RetainedEarnings'] if c in df.columns]
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)

    # 3. Limpeza de colunas financeiras críticas
    fin_cols = ['TotalAssets', 'Equity', 'EBITDA', 'Interests', 'NetProfit']
    for col in fin_cols:
        if col in df.columns:
            if df[col].dtype not in ['float64', 'int64']:
                df[col] = safe_float(df[col])

    # 4. Definição de Estados (0-Saudável, 1-Distress, 2-Terminal)
    equity = df['Equity']
    ebitda = df['EBITDA']
    interests = df['Interests']

    c1 = equity < 0
    c2 = (ebitda < interests) & (interests > 0)
    
    status_series = df['Status'].fillna('').astype(str)
    c3 = status_series.str.contains('|'.join(terminal_keywords), case=False, na=False, regex=True)

    df['State'] = 0
    df.loc[c1 | c2, 'State'] = 1
    df.loc[c3, 'State'] = 2

    # 5. Lógica de Estado Absorvente (State 2)
    df['Has_Failed_Before'] = df.groupby('NIF Code')['State'].shift(1).eq(2).groupby(df['NIF Code']).cummax()
    df = df[df['Has_Failed_Before'] != True].drop(columns=['Has_Failed_Before'])

    # 6. Cálculo de Tempos e Episódios (Counting Process)
    df['Date of Establishment'] = pd.to_datetime(df['Date of Establishment'], errors='coerce')
    df['Birth_Year'] = df['Date of Establishment'].dt.year
    df = df.dropna(subset=['Birth_Year'])

    df['t_stop'] = df['Year'] - df['Birth_Year']
    df['t_start'] = df['t_stop'] - 1
    df = df[df['t_start'] >= 0]

    # Identificar recorrência (transição 0 -> 1)
    df['State_Prev'] = df.groupby('NIF Code')['State'].shift(1).fillna(0)
    df['New_Episode'] = ((df['State_Prev'] == 0) & (df['State'] == 1)).astype(int)
    df['Episode'] = df.groupby('NIF Code')['New_Episode'].cumsum() + 1

    # 7. Lagging de Features (Prevenir Data Leakage)
    exclude_from_lag = [
        'NIF Code', 'Year', 'State', 't_start', 't_stop', 'Episode', 'Birth_Year', 
        'Status', 'State_Prev', 'New_Episode', 'Company Name', 'CAE', 'CAE_Sector', 
        'District', 'LegalForm', 'FirmAge', 'OwnershipConcentration', 'OwnershipConcentration_obs'
    ]
    cols_to_lag = [c for c in df.columns if c not in exclude_from_lag and not c.endswith('_lag1')]

    for col in cols_to_lag:
        if df[col].dtype in ['float64', 'int64']:
            df[f'{col}_lag1'] = df.groupby('NIF Code')[col].shift(1)

    # Remover a primeira observação de cada empresa (sem histórico para lag)
    lag_cols = [f'{c}_lag1' for c in cols_to_lag if f'{c}_lag1' in df.columns]
    has_no_lags = df[lag_cols].isna().all(axis=1)
    df = df[~has_no_lags | (df['State'] == 2)]

    return df
