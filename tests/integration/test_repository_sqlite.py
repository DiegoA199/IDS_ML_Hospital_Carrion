from src.alerts.engine import build_alert
from src.storage.sqlite_repository import SQLiteRepository


def test_sqlite_repository_persists_alert(tmp_path):
    repo = SQLiteRepository(tmp_path / "idsml.db")
    alert_id = repo.save_alert(build_alert("DDoS", backend=repo.backend_name))
    alerts = repo.list_alerts()
    assert alert_id
    assert len(alerts) == 1
    assert alerts[0]["severidad"] == "Alta"

