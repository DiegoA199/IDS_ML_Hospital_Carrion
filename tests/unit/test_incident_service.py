from src.domain.services.incident_service import classify_incident_priority


def test_classify_incident_priority_high_values():
    assert classify_incident_priority("Alta") == "alta"
    assert classify_incident_priority("critical") == "alta"
    assert classify_incident_priority("critica") == "alta"


def test_classify_incident_priority_medium_and_low_values():
    assert classify_incident_priority("media") == "media"
    assert classify_incident_priority("moderada") == "media"
    assert classify_incident_priority("baja") == "baja"
    assert classify_incident_priority("desconocida") == "baja"
