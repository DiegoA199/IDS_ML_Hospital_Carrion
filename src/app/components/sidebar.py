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
    ("Soporte", ("Soporte operativo",)),
)

SIDEBAR_MODULES = [module for _, modules in SIDEBAR_SECTIONS for module in modules]
SECTION_MODULES = {section: modules for section, modules in SIDEBAR_SECTIONS}

def _section_for_page(page: str) -> str:
    for section, modules in SIDEBAR_SECTIONS:
        if page in modules:
            return section
    return SIDEBAR_SECTIONS[0][0]


def _activate_page(page: str) -> None:
    st.session_state["active_page"] = page
    st.session_state["main_nav_section"] = _section_for_page(page)
    st.session_state["main_nav_page"] = page


def _ensure_active_page() -> str:
    active_page = st.session_state.get("active_page")
    if active_page not in SIDEBAR_MODULES:
        active_page = "Dashboard"
        _activate_page(active_page)
    return str(active_page)


def _render_sidebar_header(username: str, role: str) -> None:
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
                <span class="ids-chip">Acceso verificado</span>
                <span class="ids-chip">RBAC activo</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_navigation(username: str, role: str) -> str:
    """Render grouped navigation and return the selected page."""
    _render_sidebar_header(username, role)
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
                _activate_page(module)
                st.rerun()

    return str(st.session_state.get("active_page", "Dashboard"))


def _on_main_section_change() -> None:
    section = st.session_state.get("main_nav_section", SIDEBAR_SECTIONS[0][0])
    first_page = SECTION_MODULES[str(section)][0]
    _activate_page(first_page)


def _on_main_page_change() -> None:
    page = st.session_state.get("main_nav_page", "Dashboard")
    if page in SIDEBAR_MODULES:
        _activate_page(str(page))


def _sync_main_navigation(active_page: str) -> None:
    section = _section_for_page(active_page)
    modules = SECTION_MODULES[section]
    if st.session_state.get("main_nav_section") != section:
        st.session_state["main_nav_section"] = section
    if st.session_state.get("main_nav_page") not in modules:
        st.session_state["main_nav_page"] = active_page
    if st.session_state.get("main_nav_page") != active_page:
        st.session_state["main_nav_page"] = active_page


def render_main_navigation(active_page: str) -> str:
    """Render always-visible in-page navigation for collapsed sidebar scenarios."""
    active_page = _ensure_active_page()
    _sync_main_navigation(active_page)

    st.markdown(
        """
        <div class="ids-main-nav-note">
            <span>Navegación del sistema</span>
            <strong>Seleccione el área y el módulo operativo que desea revisar.</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section_col, module_col, state_col = st.columns([0.9, 1.15, 1.45])
    with section_col:
        st.selectbox(
            "Área de trabajo",
            [section for section, _ in SIDEBAR_SECTIONS],
            key="main_nav_section",
            on_change=_on_main_section_change,
        )

    modules = SECTION_MODULES[str(st.session_state["main_nav_section"])]
    if st.session_state.get("main_nav_page") not in modules:
        st.session_state["main_nav_page"] = modules[0]

    with module_col:
        st.selectbox(
            "Módulo",
            modules,
            key="main_nav_page",
            on_change=_on_main_page_change,
        )

    current_page = str(st.session_state.get("active_page", "Dashboard"))
    with state_col:
        st.markdown(
            f"""
            <div class="ids-main-nav-state">
                <div class="ids-sidebar-label">Módulo activo</div>
                <div class="ids-card-title">{escape(current_page)}</div>
                <div class="ids-card-subtitle">Use este selector para avanzar por el flujo de monitoreo, análisis y respuesta.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return current_page
