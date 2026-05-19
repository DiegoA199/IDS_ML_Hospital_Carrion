"""Validadores reutilizables para datos de entrada del sistema."""

from __future__ import annotations

import pandas as pd

from src.core.exceptions import DatasetValidationError


def ensure_columns_exist(df: pd.DataFrame, required_columns: list[str]) -> None:
    """Lanza un error controlado si faltan columnas requeridas."""
    missing = [column for column in required_columns if column not in df.columns]
    if missing:
        raise DatasetValidationError(f"Columnas requeridas ausentes: {missing}")


def ensure_non_empty_dataframe(df: pd.DataFrame) -> None:
    """Valida que el DataFrame tenga filas y columnas."""
    if df.empty or df.shape[1] == 0:
        raise DatasetValidationError("El dataset está vacío o no contiene columnas.")


def find_missing_columns(df: pd.DataFrame, required_columns: list[str]) -> list[str]:
    """Devuelve columnas requeridas que no existen en el DataFrame."""
    return [column for column in required_columns if column not in df.columns]

