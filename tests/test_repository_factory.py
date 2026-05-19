from src.storage.repository_factory import get_repository
from src.storage.sqlite_repository import SQLiteRepository


def test_factory_sqlite_explicit(monkeypatch):
    monkeypatch.setenv("IDSML_PERSISTENCE_BACKEND", "sqlite")
    monkeypatch.delenv("FIREBASE_PROJECT_ID", raising=False)
    repo = get_repository()
    assert isinstance(repo, SQLiteRepository)
    assert repo.backend_name == "sqlite"


def test_factory_auto_without_firebase_config(monkeypatch):
    monkeypatch.delenv("IDSML_PERSISTENCE_BACKEND", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("POSTGRES_DSN", raising=False)
    monkeypatch.delenv("FIREBASE_PROJECT_ID", raising=False)
    monkeypatch.delenv("GOOGLE_APPLICATION_CREDENTIALS", raising=False)
    monkeypatch.delenv("FIREBASE_CREDENTIALS_PATH", raising=False)
    repo = get_repository()
    assert repo.backend_name == "sqlite"


def test_factory_postgres_falls_back_to_sqlite_when_unavailable(monkeypatch):
    monkeypatch.setenv("IDSML_PERSISTENCE_BACKEND", "postgres")
    monkeypatch.setenv("DATABASE_URL", "postgresql://idsml:bad@127.0.0.1:1/idsml")
    repo = get_repository()
    assert repo.backend_name == "sqlite"


def test_sqlite_audit_roundtrip(tmp_path):
    repo = SQLiteRepository(tmp_path / "audit_test.db")
    rid = repo.save_audit_log("INFO", "prueba", {"x": 1})
    assert rid > 0
    rows = repo.list_audit_log(limit=5)
    assert len(rows) >= 1
    assert rows[0][2] == "prueba"
