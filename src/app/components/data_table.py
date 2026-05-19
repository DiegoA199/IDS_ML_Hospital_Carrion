"""Helpers para tablas de datos en Streamlit."""

from __future__ import annotations

import pandas as pd
import streamlit as st


def render_data_table(df: pd.DataFrame) -> None:
    """Renderiza una tabla con configuración uniforme."""
    st.dataframe(df, use_container_width=True, hide_index=True)

