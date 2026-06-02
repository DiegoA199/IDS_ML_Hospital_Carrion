import pandas as pd

from src.domain.services.preprocessing_service import run_preprocessing


def test_run_preprocessing_returns_train_test_matrices():
    df = pd.DataFrame(
        {
            "num": list(range(12)),
            "cat": ["a", "b"] * 6,
            "label": [0] * 6 + [1] * 6,
        }
    )
    prepared = run_preprocessing(df, "label", apply_smote=False)
    assert prepared.x_train.shape[0] > 0
    assert prepared.x_test.shape[0] > 0
    assert prepared.x_train.shape[1] == prepared.x_test.shape[1]
