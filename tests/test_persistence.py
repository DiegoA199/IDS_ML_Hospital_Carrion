import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from src.models.persistence import (
    align_features,
    load_model_bundle,
    predict_dataframe,
    save_model_bundle,
)
from src.preprocessing.pipeline import prepare_dataset


def test_save_load_roundtrip(tmp_path):
    df = pd.DataFrame(
        {
            "n": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
            "c": list("aaaabbbb"),
            "y": [0, 0, 0, 0, 1, 1, 1, 1],
        }
    )
    prep = prepare_dataset(df, "y", apply_smote=False, random_state=0)
    clf = RandomForestClassifier(n_estimators=5, random_state=0)
    clf.fit(prep.x_train, prep.y_train)
    p = tmp_path / "bundle.joblib"
    save_model_bundle(clf, prep, model_name="RF-test", f1_score=0.9, path=p)
    b = load_model_bundle(p)
    assert b.model_name == "RF-test"
    assert b.f1_score == 0.9
    assert list(b.feature_columns) == ["n", "c"]


def test_predict_new_rows(tmp_path):
    df = pd.DataFrame(
        {
            "n": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
            "c": list("aaaabbbb"),
            "y": [0, 0, 0, 0, 1, 1, 1, 1],
        }
    )
    prep = prepare_dataset(df, "y", apply_smote=False, random_state=0)
    clf = RandomForestClassifier(n_estimators=10, random_state=0)
    clf.fit(prep.x_train, prep.y_train)
    p = tmp_path / "b2.joblib"
    save_model_bundle(clf, prep, model_name="RF", f1_score=0.95, path=p)
    b = load_model_bundle(p)
    new = pd.DataFrame({"n": [0.15], "c": ["a"]})
    out = predict_dataframe(b, new)
    assert "prediccion_etiqueta" in out.columns
    assert len(out) == 1


def test_align_features_adds_missing():
    df = pd.DataFrame({"a": [1]})
    aligned = align_features(df, ["a", "b"])
    assert list(aligned.columns) == ["a", "b"]
    assert pd.isna(aligned["b"].iloc[0])
