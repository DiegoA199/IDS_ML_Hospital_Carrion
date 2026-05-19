import pandas as pd

from src.domain.services.alert_service import build_alerts_from_predictions, is_threat_label, severity_from_label


def test_severity_from_label_normal_is_low():
    assert severity_from_label("normal") == "Baja"
    assert not is_threat_label("normal")


def test_severity_from_label_attack_is_high():
    assert severity_from_label("DDoS") == "Alta"
    assert is_threat_label("DDoS")


def test_build_alerts_from_predictions():
    df = pd.DataFrame({"prediccion_etiqueta": ["normal", "DDoS"], "confianza": [0.7, 0.95]})
    alerts = build_alerts_from_predictions(df, model_name="RF", backend="sqlite")
    assert len(alerts) == 2
    assert alerts[1]["severidad"] == "Alta"

