import pandas as pd
import numpy as np

def safe_float(col):
    """Converte strings formatadas do SABI (ex: '1.234,56') para float."""
    if col.dtype in ['float64', 'int64']:
        return col
    return pd.to_numeric(
        col.astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).str.extract(r'([-+]?\d*\.?\d+)', expand=False), 
        errors='coerce'
    )
