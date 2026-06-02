import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from src.domain.services.prediction_service import load_prediction_bundle, predict_traffic
from src.models.persistence import save_model_bundle
from src.preprocessing.pipeline import prepare_dataset


def test_prediction_service_roundtrip(tmp_path):
    df = pd.DataFrame(
        {
            "n": [0.1, 0.2, 0.3, 0.4, 1.1, 1.2, 1.3, 1.4],
            "c": list("aaaabbbb"),
            "y": [0, 0, 0, 0, 1, 1, 1, 1],
        }
    )
    prepared = prepare_dataset(df, "y", apply_smote=False, random_state=0)
    model = RandomForestClassifier(n_estimators=5, random_state=0)
    model.fit(prepared.x_train, prepared.y_train)
    path = tmp_path / "bundle.joblib"
    save_model_bundle(model, prepared, model_name="RF", f1_score=0.8, path=path)
    bundle = load_prediction_bundle(path)
    output = predict_traffic(bundle, pd.DataFrame({"n": [0.2], "c": ["a"]}))
    assert "prediccion_etiqueta" in output.columns
