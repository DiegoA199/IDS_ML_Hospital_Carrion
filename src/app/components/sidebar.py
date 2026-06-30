"""Navegación lateral alineada con los mockups operativos IDS-ML."""

from __future__ import annotations

import streamlit as st

from src.ui.theme import institution_logo

NAV_ITEMS: tuple[tuple[str, str], ...] = (
    (":material/dashboard:", "Dashboard"),
    (":material/upload_file:", "Carga de datos"),
    (":material/table_chart:", "Preparación de datos"),
    (":material/model_training:", "Entrenamiento"),
    (":material/compare_arrows:", "Comparación"),
    (":material/online_prediction:", "Predicción"),
    (":material/notifications_active:", "Alertas"),
    (":material/assessment:", "Reportes"),
    (":material/settings:", "Configuración"),
)

SIDEBAR_MODULES = [module for _, module in NAV_ITEMS]
SIDEBAR_SECTIONS: tuple[tuple[str, tuple[str, ...]], ...] = (("IDS-ML", tuple(SIDEBAR_MODULES)),)


def _activate_page(page: str) -> None:
    st.session_state["active_page"] = page


def _ensure_active_page() -> str:
    active_page = st.session_state.get("active_page")
    if active_page not in SIDEBAR_MODULES:
        active_page = "Dashboard"
        _activate_page(active_page)
    return str(active_page)


def _render_sidebar_header(username: str, role: str) -> None:
    with st.sidebar.container(key="sidebar_branding"):
        institution_logo()


def render_sidebar_navigation(username: str, role: str) -> str:
    """Renderiza el menú exacto del producto mostrado en los mockups."""
    _render_sidebar_header(username, role)
    active_page = _ensure_active_page()

    for icon, module in NAV_ITEMS:
        is_active = module == active_page
        if st.sidebar.button(
            module,
            key=f"nav_{module}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
            icon=icon,
        ):
            _activate_page(module)
            st.rerun()

    return str(st.session_state.get("active_page", "Dashboard"))


def _sync_global_navigation() -> None:
    """Mantiene el selector principal y la ruta activa en un único estado."""
    selected = st.session_state.get("global_navigation_page")
    if selected in SIDEBAR_MODULES:
        _activate_page(str(selected))


def render_global_navigation(active_page: str) -> tuple[str, bool]:
    """Ofrece navegación accesible incluso cuando Streamlit colapsa el lateral."""
    if active_page not in SIDEBAR_MODULES:
        active_page = _ensure_active_page()

    # Un clic en el lateral debe reflejarse en el selector antes de instanciarlo.
    if st.session_state.get("global_navigation_page") != active_page:
        st.session_state["global_navigation_page"] = active_page

    with st.container(key="global_navigation"):
        label_col, menu_col, exit_col = st.columns([0.24, 0.58, 0.18])
        with label_col:
            st.markdown(
                '<div class="ids-global-nav-label">'
                '<span class="material-symbols-rounded">menu</span>'
                '<div><strong>Menú principal</strong><small>IDS-ML Hospital Carrión</small></div>'
                "</div>",
                unsafe_allow_html=True,
            )
        with menu_col:
            st.selectbox(
                "Ir a módulo",
                SIDEBAR_MODULES,
                key="global_navigation_page",
                on_change=_sync_global_navigation,
            )
        with exit_col:
            logout = st.button(
                "Cerrar sesión",
                key="logout_global",
                icon=":material/logout:",
                use_container_width=True,
            )

    return str(st.session_state.get("active_page", active_page)), logout
