"""Servicio de resumen de reportes sin dependencias de UI."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.storage.base_repository import IDSMLRepository


def build_operational_summary(repo: "IDSMLRepository") -> dict[str, int]:
    """Devuelve conteos operativos para reportes y validaciones."""
    return repo.get_dashboard_counts()

