from pathlib import Path

from src.storage.config import is_firestore_configured, is_postgres_configured, load_persistence_settings


def test_load_persistence_settings_reads_environment(monkeypatch, tmp_path):
    credentials = tmp_path / "firebase.json"
    credentials.write_text("{}", encoding="utf-8")

    monkeypatch.setenv("IDSML_PERSISTENCE_BACKEND", "postgres")
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/idsml")
    monkeypatch.setenv("FIREBASE_PROJECT_ID", "idsml-demo")
    monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", str(credentials))

    settings = load_persistence_settings()

    assert settings["backend"] == "postgres"
    assert settings["postgres_dsn"].startswith("postgresql://")
    assert is_postgres_configured(settings)
    assert is_firestore_configured(settings)


def test_storage_configuration_detects_missing_credentials():
    settings = {
        "backend": "auto",
        "firebase_project_id": "idsml-demo",
        "firebase_credentials_path": str(Path("no-existe.json")),
        "postgres_dsn": "",
    }

    assert not is_postgres_configured(settings)
    assert not is_firestore_configured(settings)
