"""Componentes de navegacion lateral para Streamlit."""

from __future__ import annotations

from html import escape

import streamlit as st

SIDEBAR_SECTIONS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("Monitoreo IDS", ("Dashboard", "Alertas e historial", "Reportes")),
    ("Pipeline ML", ("Dataset", "Preprocesamiento", "Entrenamiento", "Inferencia")),
    (
        "Administración",
        ("Base de datos", "Usuarios y roles", "Configuración", "Estado del sistema"),
    ),
    ("Despliegue", ("Nube y despliegue",)),
)

SIDEBAR_MODULES = [module for _, modules in SIDEBAR_SECTIONS for module in modules]

BACKEND_LABELS = {
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "sqlite": "SQLite local",
    "firestore": "Firestore",
    "auto": "Automático",
}


def _backend_label(backend_name: str) -> str:
    return BACKEND_LABELS.get(str(backend_name).lower(), str(backend_name).upper())


def _ensure_active_page() -> str:
    active_page = st.session_state.get("active_page")
    if active_page not in SIDEBAR_MODULES:
        active_page = "Dashboard"
        st.session_state["active_page"] = active_page
    return str(active_page)


def _render_sidebar_header(username: str, role: str, backend_name: str) -> None:
    backend = _backend_label(backend_name)
    st.sidebar.markdown(
        f"""
        <div class="ids-sidebar-brand">
            <div class="ids-brand">IDS-ML Core</div>
            <div class="ids-sidebar-meta">
                Hospital Regional Docente Clínico Quirúrgico Daniel Alcides Carrión
            </div>
        </div>
        <div class="ids-sidebar-user">
            <div class="ids-sidebar-label">Sesión activa</div>
            <div class="ids-card-title">{escape(username)}</div>
            <div class="ids-card-subtitle">{escape(role)}</div>
            <div class="ids-pill-row">
                <span class="ids-chip">{escape(backend)}</span>
                <span class="ids-chip">RBAC activo</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_navigation(username: str, role: str, backend_name: str) -> str:
    """Render grouped navigation and return the selected page."""
    _render_sidebar_header(username, role, backend_name)
    active_page = _ensure_active_page()

    for section_title, modules in SIDEBAR_SECTIONS:
        st.sidebar.markdown(
            f'<div class="ids-sidebar-section-title">{escape(section_title)}</div>',
            unsafe_allow_html=True,
        )
        for module in modules:
            is_active = module == active_page
            if st.sidebar.button(
                module,
                key=f"nav_{module}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state["active_page"] = module
                st.rerun()

    return str(st.session_state.get("active_page", "Dashboard"))
