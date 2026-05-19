import pandas as pd

from src.domain.services.preprocessing_service import run_preprocessing
from src.domain.services.training_service import choose_best_by_f1, train_candidate_models


def test_dataset_preprocessing_training_flow():
    df = pd.read_csv("tests/fixtures/sample_dataset.csv")
    prepared = run_preprocessing(df, "label", apply_smote=False)
    results = train_candidate_models(prepared.X_train, prepared.X_test, prepared.y_train, prepared.y_test)
    best = choose_best_by_f1(results)
    assert len(results) >= 6
    assert 0 <= best.metrics["f1_score"] <= 1

