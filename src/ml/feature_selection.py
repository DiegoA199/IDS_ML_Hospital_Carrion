"""Utilidades mínimas de selección de características."""

from __future__ import annotations

import pandas as pd


def numeric_feature_candidates(df: pd.DataFrame, target_column: str) -> list[str]:
    """Devuelve columnas numéricas candidatas excluyendo la variable objetivo."""
    return [column for column in df.select_dtypes(include="number").columns if column != target_column]

