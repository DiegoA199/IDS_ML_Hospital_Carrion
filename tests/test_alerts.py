from src.alerts.engine import build_alert

def test_alert_attack_high():
    alert = build_alert("DDoS")
    assert alert["severidad"] == "Alta"

def test_alert_normal_low():
    alert = build_alert("normal")
    assert alert["severidad"] == "Baja"
