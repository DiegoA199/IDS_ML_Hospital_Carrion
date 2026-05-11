"""Estado del sistema: entorno de ejecución y salud de persistencia."""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.storage.base_repository import IDSMLRepository


def detect_runtime_environment() -> str:
    if os.environ.get("STREAMLIT_SHARING", "") or os.environ.get("STREAMLIT_CLOUD", ""):
        return "streamlit_cloud"
    if Path("/.dockerenv").exists():
        return "docker"
    return "local"


def firestore_ping_ok() -> bool | None:
    """``True`` si Firestore responde; ``False`` si falla; ``None`` si no aplica (SQLite)."""
    try:
        from src.storage.config import is_firestore_configured, load_persistence_settings
        from src.storage.firestore_repository import FirestoreRepository

        if not is_firestore_configured(load_persistence_settings()):
            return None
        repo = FirestoreRepository.from_settings(load_persistence_settings())
        _ = repo.get_dashboard_counts()
        return True
    except Exception:
        return False


def build_status_payload(repo: IDSMLRepository) -> dict[str, Any]:
    counts = repo.get_dashboard_counts()
    runs = repo.list_prediction_runs(limit=1)
    return {
        "entorno": detect_runtime_environment(),
        "backend": repo.backend_name,
        "firestore_ok": firestore_ping_ok() if repo.backend_name == "firestore" else None,
        "modelo_activo": repo.get_active_model_version(),
        "ultima_prediccion": runs[0].get("created_at") if runs else None,
        "conteos": counts,
    }
