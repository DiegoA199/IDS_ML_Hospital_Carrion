"""Servicio de predicción sobre tráfico nuevo."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.models.persistence import ModelBundle, load_model_bundle, predict_dataframe


def load_prediction_bundle(path: Path | str | None = None) -> ModelBundle:
    """Carga un bundle entrenado para inferencia."""
    return load_model_bundle(path)


def predict_traffic(bundle: ModelBundle, df: pd.DataFrame) -> pd.DataFrame:
    """Genera predicciones para un lote de tráfico nuevo."""
    return predict_dataframe(bundle, df)

