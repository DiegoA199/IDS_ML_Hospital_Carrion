from src.alerts.engine import build_alert
from src.storage.sqlite_repository import SQLiteRepository


def test_sqlite_repository_operational_roundtrip(tmp_path):
    repo = SQLiteRepository(tmp_path / "idsml_full.db")

    alert_id = repo.save_alert(build_alert("DDoS", probability=0.98, model_name="RF", backend=repo.backend_name))
    assert repo.update_alert_status(alert_id, "cerrada", "Administrador TI")
    assert repo.list_alerts(limit=1)[0]["estado"] == "cerrada"

    run_id = repo.save_prediction_run(
        model_name="RF",
        f1_score=0.91,
        n_rows=2,
        trained_at_model="2026-06-02T10:00:00",
        details=[{"row_index": 0, "label": "normal"}],
    )
    repo.save_prediction_rows(
        run_id,
        [
            {"row_index": 0, "label": "normal", "confidence": 0.88},
            {"row_index": 1, "label": "DDoS", "confidence": 0.97},
        ],
    )

    assert len(repo.list_prediction_runs(limit=1)) == 1
    assert len(repo.list_prediction_rows(run_id)) == 2

    error_id = repo.save_system_error("pytest", "error controlado", {"case": "roundtrip"})
    assert error_id > 0
    assert repo.list_system_errors(limit=1)[0]["source"] == "pytest"

    report_id = repo.save_report_record(
        title="Reporte de prueba",
        report_format="csv",
        file_path="data/reports/test.csv",
        summary_json="{}",
        username="tester",
    )
    assert report_id > 0
    assert repo.list_reports(limit=1)[0]["report_format"] == "csv"

    first_model_id = repo.register_model_version(
        model_name="Decision Tree",
        f1_score=0.72,
        bundle_path="artifacts/models/dt.joblib",
        version_label="v1",
    )
    second_model_id = repo.register_model_version(
        model_name="Random Forest",
        f1_score=0.91,
        bundle_path="artifacts/models/rf.joblib",
        version_label="v2",
    )
    active = repo.get_active_model_version()
    assert first_model_id != second_model_id
    assert active is not None
    assert active["model_name"] == "Random Forest"

    counts = repo.get_dashboard_counts()
    assert counts["alerts"] == 1
    assert counts["prediction_rows"] == 2
    assert counts["amenazas_detectadas"] == 1
    assert counts["reports"] == 1


def test_sqlite_repository_empty_branches(tmp_path):
    repo = SQLiteRepository(tmp_path / "idsml_empty.db")

    assert repo.get_active_model_version() is None
    repo.save_prediction_rows(run_id=999, rows=[])
    assert repo.list_prediction_rows(999) == []
