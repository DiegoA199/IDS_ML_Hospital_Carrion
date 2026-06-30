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
        "Carga de datos": pages.render_dataset,
        "Preparación de datos": pages.render_preprocessing,
        "Comparación": pages.render_comparison,
        "Predicción": pages.render_inference,
        "Alertas": pages.render_alerts,
        # Alias internos para conservar sesiones o enlaces de versiones anteriores.
        "Dataset": pages.render_dataset,
        "Preprocesamiento": pages.render_preprocessing,
        "Entrenamiento": pages.render_training,
        "Inferencia": pages.render_inference,
        "Alertas e historial": pages.render_alerts,
        "Reportes": pages.render_reports,
        "Base de datos": pages.render_database_model,
        "Usuarios y roles": pages.render_users,
        "Configuración": pages.render_settings,
        "Estado del sistema": pages.render_system_status,
        "Soporte operativo": pages.render_cloud,
    }
    fn = routes.get(page)
    if fn is None:
        st.error("Módulo no encontrado.")
        return
    fn(repo)
