"""
Control de acceso mínimo por rol (MVP). No sustituye IAM institucional.
"""

from __future__ import annotations

from src.core.constants import ROLE_ADMIN, ROLE_ANALYST, ROLE_GUEST


def can_access_dataset(role: str) -> bool:
    return role in (ROLE_ADMIN, ROLE_ANALYST, ROLE_GUEST)


def can_train(role: str) -> bool:
    return role in (ROLE_ADMIN, ROLE_ANALYST)


def can_infer(role: str) -> bool:
    return role in (ROLE_ADMIN, ROLE_ANALYST)


def can_manage_alerts(role: str) -> bool:
    return role in (ROLE_ADMIN, ROLE_ANALYST)


def can_change_alert_status(role: str) -> bool:
    return role == ROLE_ADMIN


def can_reports(role: str) -> bool:
    return role in (ROLE_ADMIN, ROLE_ANALYST)


def can_system_status(role: str) -> bool:
    return role in (ROLE_ADMIN, ROLE_ANALYST)


def can_manual_alert_demo(role: str) -> bool:
    """Invitado puede ver alertas; solo roles TI generan alerta manual de prueba."""
    return role in (ROLE_ADMIN, ROLE_ANALYST)
