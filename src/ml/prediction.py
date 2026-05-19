"""Facade ML para predicción de tráfico nuevo."""

from __future__ import annotations

from src.models.persistence import load_model_bundle, predict_dataframe

__all__ = ["load_model_bundle", "predict_dataframe"]

