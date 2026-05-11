"""Servicio de bitácora: delega en el repositorio con contexto de sesión Streamlit."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.storage.base_repository import IDSMLRepository


def log_action(
    repo: IDSMLRepository,
    *,
    action: str,
    module: str,
    result: str,
    observation: str = "",
    level: str = "INFO",
    extra: dict[str, Any] | None = None,
) -> None:
    """Registra un evento estructurado usando usuario y rol de ``st.session_state``."""
    import streamlit as st

    repo.save_audit_event(
        username=str(st.session_state.get("username", "-")),
        role=str(st.session_state.get("role", "-")),
        action=action,
        module=module,
        result=result,
        observation=observation,
        level=level,
        extra=extra,
    )
