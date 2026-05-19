"""Excepciones controladas de la aplicación IDS-ML."""

from __future__ import annotations


class IDSMLException(Exception):
    """Error base controlado del sistema IDS-ML."""


class DatasetValidationError(IDSMLException):
    """El dataset no cumple las reglas mínimas de validación."""


class ModelTrainingError(IDSMLException):
    """No fue posible completar el entrenamiento del modelo."""


class PredictionError(IDSMLException):
    """No fue posible ejecutar predicciones sobre tráfico nuevo."""

