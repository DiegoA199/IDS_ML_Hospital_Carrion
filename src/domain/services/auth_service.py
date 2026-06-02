"""Servicio de autenticacion demo desacoplado de la interfaz."""

from __future__ import annotations

import hashlib
import hmac

from src.core.constants import ROLE_ADMIN, ROLE_ANALYST, ROLE_GUEST
from src.domain.entities.user import User

DEMO_USERS = {
    "admin": {
        "credential_hash": "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9",
        "role": ROLE_ADMIN,
    },
    "analista": {
        "credential_hash": "9cd268397030111adacb4268e51f0dbbb0dbc8c59eb34f8f7d55f72d4c888349",
        "role": ROLE_ANALYST,
    },
    "invitado": {
        "credential_hash": "002a8c8f252b5071ea88ac6a33f028236739b9a1c583dcf13d9d01657c178f4c",
        "role": ROLE_GUEST,
    },
}


def authenticate(username: str, password: str) -> User | None:
    """Valida credenciales demo y devuelve un usuario de dominio."""
    record = DEMO_USERS.get(username)
    submitted_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    if not record or not hmac.compare_digest(record["credential_hash"], submitted_hash):
        return None
    return User(username=username, role=record["role"], is_active=True)
