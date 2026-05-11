"""
Carga de configuración de persistencia desde variables de entorno y Streamlit secrets.

No incluye credenciales reales: solo nombres de claves esperadas y valores por defecto.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any


def _secrets_dict() -> dict[str, Any]:
    """Obtiene ``st.secrets`` como dict si la app corre en Streamlit; si no, dict vacío."""
    try:
        import streamlit as st  # type: ignore

        if hasattr(st, "secrets"):
            return {str(k): st.secrets[k] for k in st.secrets}
    except Exception:
        pass
    return {}


def _as_plain_dict(obj: Any) -> dict[str, Any]:
    if obj is None:
        return {}
    if isinstance(obj, dict):
        return obj
    try:
        return dict(obj)
    except Exception:
        return {}


def load_persistence_settings() -> dict[str, Any]:
    """
    Resuelve backend y parámetros Firebase.

    Prioridad: variables de entorno; luego claves en ``.streamlit/secrets.toml``
    (expuestas vía ``st.secrets`` en tiempo de ejecución).

    Claves soportadas (ejemplos, sin valores reales):

    - ``IDSML_PERSISTENCE_BACKEND``: ``auto`` | ``sqlite`` | ``firestore``
    - ``FIREBASE_PROJECT_ID`` / ``[firebase] project_id`` en secrets
    - ``GOOGLE_APPLICATION_CREDENTIALS`` o ``FIREBASE_CREDENTIALS_PATH``: ruta al JSON de cuenta de servicio
    """
    sec = _secrets_dict()
    fb = _as_plain_dict(sec.get("firebase"))

    backend = (
        os.environ.get("IDSML_PERSISTENCE_BACKEND")
        or sec.get("IDSML_PERSISTENCE_BACKEND")
        or "auto"
    )
    backend = str(backend).strip().lower()

    project_id = (
        os.environ.get("FIREBASE_PROJECT_ID")
        or fb.get("project_id")
        or sec.get("FIREBASE_PROJECT_ID")
    )

    cred_path = (
        os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        or os.environ.get("FIREBASE_CREDENTIALS_PATH")
        or fb.get("credentials_path")
        or sec.get("FIREBASE_CREDENTIALS_PATH")
    )

    return {
        "backend": backend,
        "firebase_project_id": project_id,
        "firebase_credentials_path": cred_path,
    }


def is_firestore_configured(settings: dict[str, Any] | None = None) -> bool:
    """True si hay proyecto, ruta de credenciales y el archivo existe en disco."""
    s = settings or load_persistence_settings()
    pid = s.get("firebase_project_id")
    cp = s.get("firebase_credentials_path")
    if not pid or not cp:
        return False
    return Path(cp).is_file()
