"""Facade ML para entrenamiento comparativo."""

from __future__ import annotations

from src.models.trainer import MODELS, ModelResult, select_best_model, train_and_evaluate

__all__ = ["MODELS", "ModelResult", "select_best_model", "train_and_evaluate"]

