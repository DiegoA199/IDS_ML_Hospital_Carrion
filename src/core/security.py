"""Utilidades de seguridad de aplicación sin credenciales reales."""

from __future__ import annotations

from src.core.constants import ROLE_ADMIN, ROLE_ANALYST, ROLE_GUEST


def normalize_role(role: str | None) -> str:
    """Normaliza roles desconocidos al rol invitado."""
    value = (role or "").strip()
    if value in {ROLE_ADMIN, ROLE_ANALYST, ROLE_GUEST}:
        return value
    return ROLE_GUEST


def is_privileged_role(role: str | None) -> bool:
    """Indica si el rol puede ejecutar operaciones TI críticas."""
    return normalize_role(role) in {ROLE_ADMIN, ROLE_ANALYST}

