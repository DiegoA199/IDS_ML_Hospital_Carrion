"""
IDS-ML Hospital Carrión — orquestador mínimo de la aplicación Streamlit.

La lógica de páginas vive en ``src/ui/pages.py`` y el enrutador en ``src/ui/router.py``.
"""

import streamlit as st

from src.auth.simple_auth import login, require_auth
from src.storage.repository_factory import get_repository
from src.ui.router import render_page

st.set_page_config(page_title="IDS-ML Hospital Carrión", layout="wide")
st.title("IDS-ML — Hospital Regional Docente Clínico Quirúrgico Daniel Alcides Carrión")
st.caption(
    "MVP operativo: ML sobre datos autorizados/controlados (CSV), alertas, bitácora, "
    "persistencia SQLite/Firestore y despliegue portable. No interviene la red institucional sin autorización TI."
)

for _k, _v in [("df", None), ("results", None), ("best_model", None), ("last_pred_df", None)]:
    if _k not in st.session_state:
        st.session_state[_k] = _v

repo = get_repository()
login(repo)

if not require_auth():
    st.stop()

role = st.session_state.get("role", "")
st.sidebar.success(f"Rol activo: {role}")
st.sidebar.caption(f"Persistencia activa: **{repo.backend_name}**")

page = st.sidebar.radio(
    "Módulo",
    [
        "Dashboard",
        "Dataset",
        "Entrenamiento",
        "Inferencia",
        "Alertas e historial",
        "Reportes",
        "Estado del sistema",
        "Nube y despliegue",
    ],
)

render_page(page, repo)
