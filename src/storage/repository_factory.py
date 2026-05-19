"""
Fábrica de repositorios: SQLite local, PostgreSQL en Docker/producción,
Firestore en nube o modo automático con fallback.

La configuración se obtiene de ``load_persistence_settings`` (entorno + Streamlit secrets).
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from src.storage.base_repository import IDSMLRepository
from src.storage.config import is_firestore_configured, is_postgres_configured, load_persistence_settings
from src.storage.sqlite_repository import SQLiteRepository

if TYPE_CHECKING:
    from src.storage.firestore_repository import FirestoreRepository
    from src.storage.postgres_repository import PostgreSQLRepository

logger = logging.getLogger("idsml.repository_factory")


def _make_firestore(settings: dict) -> "FirestoreRepository":
    from src.storage.firestore_repository import FirestoreRepository

    return FirestoreRepository.from_settings(settings)


def _make_postgres(settings: dict) -> "PostgreSQLRepository":
    from src.storage.postgres_repository import PostgreSQLRepository

    return PostgreSQLRepository.from_settings(settings)


def get_repository() -> IDSMLRepository:
    """
    Devuelve la implementación activa del repositorio.

    - ``IDSML_PERSISTENCE_BACKEND=sqlite``: siempre SQLite.
    - ``IDSML_PERSISTENCE_BACKEND=postgres``: PostgreSQL; si falla, SQLite.
    - ``IDSML_PERSISTENCE_BACKEND=firestore``: Firestore; si falla, SQLite.
    - ``IDSML_PERSISTENCE_BACKEND=auto``: PostgreSQL si hay ``DATABASE_URL``; si no,
      Firestore si hay proyecto + credenciales; si no hay configuración o hay error, SQLite.
    """
    settings = load_persistence_settings()
    backend = settings.get("backend", "auto")

    if backend == "sqlite":
        return SQLiteRepository()

    if backend == "postgres":
        try:
            return _make_postgres(settings)
        except Exception as exc:
            logger.warning("PostgreSQL solicitado pero no disponible (%s); usando SQLite.", exc)
            return SQLiteRepository()

    if backend == "firestore":
        try:
            return _make_firestore(settings)
        except Exception as exc:
            logger.warning("Firestore solicitado pero no disponible (%s); usando SQLite.", exc)
            return SQLiteRepository()

    # auto
    if is_postgres_configured(settings):
        try:
            return _make_postgres(settings)
        except Exception as exc:
            logger.warning("PostgreSQL configurado pero falló el arranque (%s); usando SQLite.", exc)

    if is_firestore_configured(settings):
        try:
            return _make_firestore(settings)
        except Exception as exc:
            logger.warning("Firestore configurado pero falló el arranque (%s); usando SQLite.", exc)
            return SQLiteRepository()

    return SQLiteRepository()
