from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

MODELS = {
    "Random Forest": RandomForestClassifier(n_estimators=120, random_state=42),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "KNN": KNeighborsClassifier(n_neighbors=5),
}

@dataclass
class ModelResult:
    name: str
    model: Any
    metrics: Dict[str, float]
    confusion_matrix: list


def train_and_evaluate(X_train, X_test, y_train, y_test):
    results = []
    average = "weighted"
    for name, model in MODELS.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        metrics = {
            "accuracy": float(accuracy_score(y_test, pred)),
            "precision": float(precision_score(y_test, pred, average=average, zero_division=0)),
            "recall": float(recall_score(y_test, pred, average=average, zero_division=0)),
            "f1_score": float(f1_score(y_test, pred, average=average, zero_division=0)),
        }
        results.append(ModelResult(name, model, metrics, confusion_matrix(y_test, pred).tolist()))
    return results

def select_best_model(results):
    return max(results, key=lambda r: r.metrics.get("f1_score", 0.0))
