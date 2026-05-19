"""Configuración general no sensible del prototipo IDS-ML."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """Valores no secretos usados por la aplicación."""

    app_name: str = "IDS-ML Core"
    institution_name: str = "Hospital Regional Docente Clínico Quirúrgico Daniel Alcides Carrión"
    default_backend: str = "auto"
    sqlite_database_name: str = "idsml_local.db"


def get_app_config() -> AppConfig:
    """Devuelve configuración de aplicación sin leer secretos."""
    return AppConfig()

