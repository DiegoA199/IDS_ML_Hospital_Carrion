"""
IDS-ML Hospital Carrión — orquestador mínimo de la aplicación Streamlit.

La lógica de páginas vive en ``src/ui/pages.py`` y el enrutador en ``src/ui/router.py``.
"""

import streamlit as st

from src.auth.simple_auth import login, require_auth
from src.app.components.sidebar import render_sidebar_navigation
from src.storage.repository_factory import get_repository
from src.ui.router import render_page
from src.ui.theme import apply_global_theme

st.set_page_config(
    page_title="IDS-ML Hospital Carrión",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_global_theme()

for _k, _v in [
    ("df", None),
    ("dataset_profile", None),
    ("prepared_dataset", None),
    ("prepared_target_col", None),
    ("results", None),
    ("best_model", None),
    ("last_pred_df", None),
]:
    if _k not in st.session_state:
        st.session_state[_k] = _v

repo = get_repository()

if not st.session_state.get("authenticated", False):
    login(repo)
    st.stop()

if not require_auth():
    st.stop()

role = st.session_state.get("role", "")
username = st.session_state.get("username", "usuario")

page = render_sidebar_navigation(username=username, role=role)

if st.sidebar.button("Cerrar sesión", key="logout", icon=":material/logout:"):
    for key in ["authenticated", "username", "role", "active_page"]:
        st.session_state.pop(key, None)
    st.rerun()

render_page(page, repo)
