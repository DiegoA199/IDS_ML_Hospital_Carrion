import numpy as np
import pandas as pd
import pytest

from src.preprocessing.pipeline import _encode_target_after_split, prepare_dataset


def test_prepare_dataset_shapes_and_no_leakage_columns():
    """Split coherente: train+test filas = filas Ãºtiles; mismas columnas en X."""
    df = pd.DataFrame(
        {
            "num": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0],
            "cat": list("aaaabbbb"),
            "label": [0, 0, 0, 0, 1, 1, 1, 1],
        }
    )
    prep = prepare_dataset(df, "label", test_size=0.25, random_state=0, apply_smote=False)
    assert prep.x_train.shape[0] + prep.x_test.shape[0] == len(df)
    assert prep.x_train.shape[1] == prep.x_test.shape[1]
    assert prep.y_train.shape[0] == prep.x_train.shape[0]
    assert prep.y_test.shape[0] == prep.x_test.shape[0]


def test_unseen_label_in_test_raises():
    """Las etiquetas de prueba deben estar en el vocabulario ajustado con y_train."""
    y_train = pd.Series(["benigno", "benigno", "ataque"])
    y_test = pd.Series(["desconocido"])
    with pytest.raises(ValueError, match="no vistas"):
        _encode_target_after_split(y_train, y_test)


def test_smote_increases_minority_only_train():
    """SMOTE aumenta filas de train; el tamaÃ±o de test no cambia respecto a split sin SMOTE."""
    rng = np.random.default_rng(42)
    n0, n1 = 30, 4
    X0 = rng.normal(size=(n0, 3))
    X1 = rng.normal(size=(n1, 3)) + 2.0
    X = np.vstack([X0, X1])
    y = np.array([0] * n0 + [1] * n1)
    df = pd.DataFrame(X, columns=["a", "b", "c"])
    df["label"] = y
    prep_no = prepare_dataset(df, "label", test_size=0.3, random_state=0, apply_smote=False)
    prep_yes = prepare_dataset(df, "label", test_size=0.3, random_state=0, apply_smote=True)
    assert prep_yes.x_test.shape == prep_no.x_test.shape
    assert prep_yes.y_test.shape == prep_no.y_test.shape
    assert prep_yes.x_train.shape[0] >= prep_no.x_train.shape[0]
