"""Servicios de validación y perfilado de datasets IDS."""

from __future__ import annotations

import pandas as pd

from src.data.profile import profile_dataframe
from src.domain.entities.dataset import DatasetProfile
from src.utils.validators import ensure_columns_exist, ensure_non_empty_dataframe


def validate_dataset(df: pd.DataFrame, required_columns: list[str] | None = None) -> None:
    """Valida condiciones mínimas del dataset sin depender de Streamlit."""
    ensure_non_empty_dataframe(df)
    if required_columns:
        ensure_columns_exist(df, required_columns)


def build_dataset_profile(df: pd.DataFrame) -> DatasetProfile:
    """Construye perfil resumido como entidad de dominio."""
    profile = profile_dataframe(df)
    return DatasetProfile(
        rows=int(profile["rows"]),
        columns=int(profile["columns"]),
        missing_total=int(profile["missing_total"]),
        duplicated_rows=int(profile["duplicated_rows"]),
    )


def calculate_quality_score(profile: DatasetProfile) -> float:
    """Calcula score simple de calidad por nulos y duplicados."""
    total_cells = max(1, profile.rows * profile.columns)
    missing_pct = (profile.missing_total / total_cells) * 100
    duplicate_pct = (profile.duplicated_rows / max(1, profile.rows)) * 100
    return max(0.0, min(100.0, 100.0 - missing_pct - duplicate_pct))

