"""Componente conceptual para paneles de filtro."""

from __future__ import annotations

import streamlit as st


def render_multiselect_filter(label: str, options: list[str], default: list[str] | None = None) -> list[str]:
    """Renderiza un filtro multiselect y devuelve selección."""
    return st.multiselect(label, options, default=default or options)

