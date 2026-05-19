"""Servicio de entrenamiento y selección del mejor modelo."""

from __future__ import annotations

from typing import Any

from src.models.trainer import ModelResult, select_best_model, train_and_evaluate


def train_candidate_models(X_train: Any, X_test: Any, y_train: Any, y_test: Any) -> list[ModelResult]:
    """Entrena modelos candidatos y devuelve resultados comparables."""
    return train_and_evaluate(X_train, X_test, y_train, y_test)


def choose_best_by_f1(results: list[ModelResult]) -> ModelResult:
    """Selecciona el mejor resultado por F1-score."""
    return select_best_model(results)

