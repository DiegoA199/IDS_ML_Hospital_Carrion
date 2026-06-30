"""Navegación lateral alineada con los mockups operativos IDS-ML."""

from __future__ import annotations

import streamlit as st

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
    st.sidebar.markdown(
        f"""
        <div class="ids-sidebar-brand">
            <div class="ids-brand-mark">+</div>
            <div>
                <div class="ids-brand">IDS-ML</div>
                <div class="ids-sidebar-meta">Hospital Carrión</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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
