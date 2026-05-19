"""Servicio de preprocesamiento desacoplado de vistas."""

from __future__ import annotations

import pandas as pd

from src.preprocessing.pipeline import PreparedDataset, prepare_dataset


def run_preprocessing(
    df: pd.DataFrame,
    target_column: str,
    *,
    test_size: float = 0.25,
    apply_smote: bool = True,
    drop_na_rows: bool = True,
) -> PreparedDataset:
    """Ejecuta el pipeline de preparación de datos del IDS-ML."""
    return prepare_dataset(
        df,
        target_column,
        test_size=test_size,
        apply_smote=apply_smote,
        drop_na_rows=drop_na_rows,
    )

