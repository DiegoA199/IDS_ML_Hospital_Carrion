"""Entrenamiento y comparación de modelos ML para el prototipo IDS-ML."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sklearn.ensemble import RandomForestClassifier
from sklearn.base import clone
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

MODELS = {
    "Random Forest": RandomForestClassifier(n_estimators=120, random_state=42),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "SVM": SVC(kernel="rbf", probability=True, random_state=42),
    "KNN": KNeighborsClassifier(n_neighbors=5),
    "Naive Bayes": GaussianNB(),
}


@dataclass
class ModelResult:
    """Resultado serializable de entrenamiento/evaluación de un modelo candidato."""

    name: str
    model: Any
    metrics: dict[str, float]
    confusion_matrix: list


def _calculate_metrics(y_test: Any, predictions: Any) -> dict[str, float]:
    """Calcula métricas ponderadas para comparación entre modelos."""
    average = "weighted"
    return {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "precision": float(precision_score(y_test, predictions, average=average, zero_division=0)),
        "recall": float(recall_score(y_test, predictions, average=average, zero_division=0)),
        "f1_score": float(f1_score(y_test, predictions, average=average, zero_division=0)),
    }


def train_and_evaluate(X_train: Any, X_test: Any, y_train: Any, y_test: Any) -> list[ModelResult]:
    """Entrena todos los modelos candidatos y devuelve métricas comparables."""
    results: list[ModelResult] = []
    for name, estimator_template in MODELS.items():
        model = clone(estimator_template)
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        metrics = _calculate_metrics(y_test, predictions)
        matrix = confusion_matrix(y_test, predictions).tolist()
        results.append(ModelResult(name, model, metrics, matrix))
    return results


def select_best_model(results: list[ModelResult]) -> ModelResult:
    """Selecciona el mejor modelo usando F1-score ponderado."""
    if not results:
        raise ValueError("No hay resultados de entrenamiento para comparar.")
    return max(results, key=lambda r: r.metrics.get("f1_score", 0.0))
