from sklearn.dummy import DummyClassifier

from src.domain.services.training_service import choose_best_by_f1
from src.models.trainer import MODELS, ModelResult


def test_models_include_required_algorithms():
    assert {"Random Forest", "Decision Tree", "Logistic Regression", "SVM", "KNN", "Naive Bayes"}.issubset(MODELS)


def test_choose_best_by_f1_returns_highest_score():
    low = ModelResult("low", DummyClassifier(), {"f1_score": 0.3}, [])
    high = ModelResult("high", DummyClassifier(), {"f1_score": 0.9}, [])
    assert choose_best_by_f1([low, high]).name == "high"

