"""Servicio de autenticación demo desacoplado de la interfaz."""

from __future__ import annotations

from src.core.constants import ROLE_ADMIN, ROLE_ANALYST, ROLE_GUEST
from src.domain.entities.user import User

DEMO_USERS = {
    "admin": {"password": "admin123", "role": ROLE_ADMIN},
    "analista": {"password": "analista123", "role": ROLE_ANALYST},
    "invitado": {"password": "invitado123", "role": ROLE_GUEST},
}


def authenticate(username: str, password: str) -> User | None:
    """Valida credenciales demo y devuelve un usuario de dominio."""
    record = DEMO_USERS.get(username)
    if not record or record["password"] != password:
        return None
    return User(username=username, role=record["role"], is_active=True)

