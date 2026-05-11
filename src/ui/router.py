"""Enrutador mínimo de páginas Streamlit."""

from __future__ import annotations

from typing import TYPE_CHECKING

import streamlit as st

if TYPE_CHECKING:
    from src.storage.base_repository import IDSMLRepository


def render_page(page: str, repo: IDSMLRepository) -> None:
    from collections.abc import Callable

    from src.ui import pages

    routes: dict[str, Callable[[IDSMLRepository], None]] = {
        "Dashboard": pages.render_dashboard,
        "Dataset": pages.render_dataset,
        "Entrenamiento": pages.render_training,
        "Inferencia": pages.render_inference,
        "Alertas e historial": pages.render_alerts,
        "Reportes": pages.render_reports,
        "Estado del sistema": pages.render_system_status,
        "Nube y despliegue": pages.render_cloud,
    }
    fn = routes.get(page)
    if fn is None:
        st.error("Módulo no encontrado.")
        return
    fn(repo)
