"""Reusable visual layer for the IDS-ML Streamlit interface."""

from __future__ import annotations

from html import escape
from textwrap import dedent
from typing import Any

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

PALETTE = {
    "background": "#031427",
    "surface": "#0b1c30",
    "surface_high": "#102034",
    "surface_higher": "#1b2b3f",
    "border": "#26364a",
    "border_soft": "#1e293b",
    "text": "#d3e4fe",
    "muted": "#9ca3af",
    "blue": "#7bd0ff",
    "blue_deep": "#0ea5d8",
    "green": "#4edea3",
    "amber": "#fbbf24",
    "red": "#ffaaa5",
    "slate": "#c1c6db",
}

TONE_COLORS = {
    "blue": PALETTE["blue"],
    "green": PALETTE["green"],
    "red": PALETTE["red"],
    "amber": PALETTE["amber"],
    "slate": PALETTE["slate"],
}


def _html(markup: str) -> None:
    st.markdown(dedent(markup).strip(), unsafe_allow_html=True)


def apply_global_theme() -> None:
    """Apply the dark SOC-inspired visual system used across pages."""
    _html(
        f"""
        <style>
        :root {{
            --ids-bg: {PALETTE["background"]};
            --ids-surface: {PALETTE["surface"]};
            --ids-surface-high: {PALETTE["surface_high"]};
            --ids-border: {PALETTE["border"]};
            --ids-border-soft: {PALETTE["border_soft"]};
            --ids-text: {PALETTE["text"]};
            --ids-muted: {PALETTE["muted"]};
            --ids-blue: {PALETTE["blue"]};
            --ids-green: {PALETTE["green"]};
            --ids-red: {PALETTE["red"]};
            --ids-amber: {PALETTE["amber"]};
        }}

        html, body, [class*="css"], .stApp {{
            font-family: Inter, "Segoe UI", Arial, sans-serif;
            letter-spacing: 0 !important;
        }}

        .stApp {{
            background:
                linear-gradient(90deg, rgba(123, 208, 255, 0.035) 1px, transparent 1px),
                linear-gradient(0deg, rgba(123, 208, 255, 0.035) 1px, transparent 1px),
                var(--ids-bg);
            background-size: 48px 48px;
            color: var(--ids-text);
        }}

        [data-testid="stHeader"] {{
            background: rgba(3, 20, 39, 0.78);
            border-bottom: 1px solid var(--ids-border);
            backdrop-filter: blur(12px);
        }}

        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"] {{
            visibility: hidden;
            height: 0;
            position: fixed;
        }}

        [data-testid="stSidebar"] {{
            background: #03111f;
            border-right: 1px solid var(--ids-border);
        }}

        [data-testid="stSidebar"] * {{
            color: var(--ids-text);
        }}

        [data-testid="stSidebar"] [role="radiogroup"] label {{
            border-radius: 8px;
            padding: 0.55rem 0.7rem;
            margin: 0.18rem 0;
            border: 1px solid transparent;
        }}

        [data-testid="stSidebar"] [role="radiogroup"] label:hover {{
            background: rgba(123, 208, 255, 0.09);
            border-color: rgba(123, 208, 255, 0.24);
        }}

        [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {{
            background: #0898c7;
            border-color: #16b7e8;
            box-shadow: 0 0 0 1px rgba(123, 208, 255, 0.22);
        }}

        .main .block-container {{
            max-width: 1440px;
            padding-top: 2.4rem;
            padding-bottom: 3rem;
        }}

        h1, h2, h3 {{
            color: var(--ids-text);
            letter-spacing: 0 !important;
        }}

        p, li, label, span, div {{
            letter-spacing: 0 !important;
        }}

        .stButton > button,
        .stDownloadButton > button,
        button[kind="primary"],
        button[kind="secondary"] {{
            border-radius: 8px;
            border: 1px solid rgba(123, 208, 255, 0.42);
            background: #7bd0ff;
            color: #001e2c;
            font-weight: 700;
            min-height: 2.7rem;
        }}

        .stButton > button:hover,
        .stDownloadButton > button:hover {{
            border-color: #a8e1ff;
            background: #a8e1ff;
            color: #001e2c;
        }}

        div[data-testid="stFileUploader"] section {{
            background: rgba(16, 32, 52, 0.72);
            border: 1px dashed rgba(193, 198, 219, 0.42);
            border-radius: 8px;
        }}

        div[data-testid="stFileUploader"] section:hover {{
            border-color: var(--ids-blue);
            box-shadow: 0 0 0 2px rgba(123, 208, 255, 0.12);
        }}

        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        div[data-baseweb="textarea"] > div,
        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input {{
            background: #07182b;
            border-color: rgba(193, 198, 219, 0.32);
            color: var(--ids-text);
            border-radius: 8px;
        }}

        .stDataFrame,
        [data-testid="stTable"] {{
            border: 1px solid var(--ids-border);
            border-radius: 8px;
            overflow: hidden;
        }}

        .stAlert {{
            border-radius: 8px;
            border: 1px solid rgba(123, 208, 255, 0.2);
            background: rgba(16, 32, 52, 0.72);
        }}

        .ids-page-head {{
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            align-items: flex-start;
            border-bottom: 1px solid var(--ids-border);
            padding: 0 0 1rem 0;
            margin-bottom: 1.35rem;
        }}

        .ids-title {{
            font-size: 2rem;
            line-height: 2.4rem;
            font-weight: 800;
            color: var(--ids-text);
            margin: 0;
        }}

        .ids-kicker {{
            color: var(--ids-blue);
            font-size: 0.78rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 0.35rem;
        }}

        .ids-subtitle {{
            color: var(--ids-muted);
            font-size: 0.95rem;
            margin-top: 0.35rem;
            max-width: 820px;
        }}

        .ids-top-tag,
        .ids-chip {{
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            border-radius: 999px;
            padding: 0.24rem 0.58rem;
            font-size: 0.76rem;
            font-weight: 800;
            border: 1px solid rgba(123, 208, 255, 0.32);
            background: rgba(123, 208, 255, 0.10);
            color: var(--ids-blue);
            white-space: nowrap;
        }}

        .ids-card {{
            background: linear-gradient(180deg, rgba(16, 32, 52, 0.94), rgba(11, 28, 48, 0.94));
            border: 1px solid var(--ids-border);
            border-radius: 8px;
            padding: 1rem;
            min-height: 100%;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03);
        }}

        .ids-card-title {{
            color: var(--ids-text);
            font-size: 1.05rem;
            font-weight: 800;
            margin-bottom: 0.25rem;
        }}

        .ids-card-subtitle {{
            color: var(--ids-muted);
            font-size: 0.86rem;
            line-height: 1.35rem;
        }}

        .ids-metric-title {{
            color: #c6c6cd;
            font-size: 0.78rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 0.55rem;
        }}

        .ids-metric-value {{
            color: var(--ids-text);
            font-size: 2.1rem;
            line-height: 2.35rem;
            font-weight: 850;
            font-variant-numeric: tabular-nums;
        }}

        .ids-metric-caption {{
            color: var(--ids-muted);
            font-size: 0.84rem;
            margin-top: 0.45rem;
        }}

        .ids-progress {{
            height: 0.34rem;
            border-radius: 999px;
            background: rgba(193, 198, 219, 0.14);
            overflow: hidden;
            margin-top: 0.75rem;
        }}

        .ids-progress > span {{
            display: block;
            height: 100%;
            border-radius: 999px;
        }}

        .ids-pill-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
            margin-top: 0.45rem;
        }}

        .ids-steps {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
            gap: 0.85rem;
            margin: 0.5rem 0 1.1rem 0;
        }}

        .ids-step {{
            border: 1px solid var(--ids-border);
            border-radius: 8px;
            background: rgba(16, 32, 52, 0.78);
            padding: 0.95rem;
        }}

        .ids-step[data-state="done"] {{
            border-left: 4px solid var(--ids-green);
        }}

        .ids-step[data-state="active"] {{
            border-left: 4px solid var(--ids-blue);
            box-shadow: 0 0 0 1px rgba(123, 208, 255, 0.18);
        }}

        .ids-step[data-state="pending"] {{
            border-left: 4px solid rgba(193, 198, 219, 0.38);
        }}

        .ids-step-name {{
            color: var(--ids-text);
            font-weight: 800;
            margin: 0.45rem 0 0.2rem 0;
        }}

        .ids-step-copy {{
            color: var(--ids-muted);
            font-size: 0.82rem;
            line-height: 1.25rem;
        }}

        .ids-login-wrap {{
            min-height: 74vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .ids-login-card {{
            width: min(100%, 540px);
            margin: 0 auto;
        }}

        .ids-sidebar-brand {{
            border-bottom: 1px solid var(--ids-border);
            padding-bottom: 1rem;
            margin-bottom: 1rem;
        }}

        .ids-brand {{
            color: var(--ids-text);
            font-size: 1.25rem;
            font-weight: 850;
        }}

        .ids-sidebar-meta {{
            color: var(--ids-muted);
            font-size: 0.82rem;
            margin-top: 0.35rem;
        }}

        @media (max-width: 900px) {{
            .ids-page-head {{
                display: block;
            }}

            .ids-title {{
                font-size: 1.45rem;
                line-height: 1.9rem;
            }}

            .ids-metric-value {{
                font-size: 1.65rem;
                line-height: 1.95rem;
            }}
        }}
        </style>
        """
    )


def page_header(title: str, subtitle: str = "", kicker: str = "IDS-ML Core", tag: str | None = None) -> None:
    tag_html = f'<span class="ids-top-tag">{escape(tag)}</span>' if tag else ""
    _html(
        f"""
        <div class="ids-page-head">
            <div>
                <div class="ids-kicker">{escape(kicker)}</div>
                <div class="ids-title">{escape(title)}</div>
                <div class="ids-subtitle">{escape(subtitle)}</div>
            </div>
            <div>{tag_html}</div>
        </div>
        """
    )


def section_title(title: str, subtitle: str = "") -> None:
    _html(
        f"""
        <div style="margin: 1.1rem 0 0.65rem 0;">
            <div class="ids-card-title">{escape(title)}</div>
            <div class="ids-card-subtitle">{escape(subtitle)}</div>
        </div>
        """
    )


def render_card(title: str, body: str = "", tone: str = "blue") -> None:
    color = TONE_COLORS.get(tone, PALETTE["blue"])
    _html(
        f"""
        <div class="ids-card" style="border-top: 3px solid {color};">
            <div class="ids-card-title">{escape(title)}</div>
            <div class="ids-card-subtitle">{escape(body)}</div>
        </div>
        """
    )


def metric_card(
    title: str,
    value: Any,
    caption: str = "",
    *,
    tone: str = "blue",
    progress: float | None = None,
) -> None:
    color = TONE_COLORS.get(tone, PALETTE["blue"])
    progress_html = ""
    if progress is not None:
        pct = max(0.0, min(100.0, float(progress)))
        progress_html = (
            f'<div class="ids-progress"><span style="width: {pct:.2f}%; background: {color};"></span></div>'
        )
    _html(
        '<div class="ids-card">'
        f'<div class="ids-metric-title">{escape(title)}</div>'
        f'<div class="ids-metric-value" style="color: {color};">{escape(str(value))}</div>'
        f"{progress_html}"
        f'<div class="ids-metric-caption">{escape(caption)}</div>'
        "</div>"
    )


def chip(label: str, tone: str = "blue") -> str:
    color = TONE_COLORS.get(tone, PALETTE["blue"])
    return (
        f'<span class="ids-chip" style="border-color: {color}55; color: {color}; '
        f'background: {color}1a;">{escape(label)}</span>'
    )


def chip_row(items: list[tuple[str, str]]) -> None:
    html = "".join(chip(label, tone) for label, tone in items)
    _html(f'<div class="ids-pill-row">{html}</div>')


def pipeline_steps(steps: list[dict[str, str]]) -> None:
    html_parts = []
    for step in steps:
        state = step.get("state", "pending")
        badge_tone = {"done": "green", "active": "blue", "pending": "slate", "blocked": "red"}.get(state, "slate")
        html_parts.append(
            dedent(
                f"""
            <div class="ids-step" data-state="{escape(state)}">
                {chip(step.get("status", state).upper(), badge_tone)}
                <div class="ids-step-name">{escape(step.get("name", ""))}</div>
                <div class="ids-step-copy">{escape(step.get("description", ""))}</div>
            </div>
            """
            ).strip()
        )
    _html(f'<div class="ids-steps">{"".join(html_parts)}</div>')


def empty_state(message: str) -> None:
    _html(
        f"""
        <div class="ids-card">
            <div class="ids-card-title">Sin datos todavía</div>
            <div class="ids-card-subtitle">{escape(message)}</div>
        </div>
        """
    )


def format_int(value: Any) -> str:
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return "0"


def format_percent(value: Any, digits: int = 1) -> str:
    if value is None:
        return "0.0%"
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "0.0%"
    if number <= 1:
        number *= 100
    return f"{number:.{digits}f}%"


def severity_tone(value: Any) -> str:
    normalized = str(value or "").strip().lower()
    if normalized in {"critica", "crítica", "critical", "alta", "high"}:
        return "red"
    if normalized in {"media", "medium", "moderada"}:
        return "amber"
    if normalized in {"baja", "low", "normal"}:
        return "green"
    return "blue"


def threat_mask(labels: pd.Series) -> pd.Series:
    normal_labels = {"normal", "0", "benign", "benigno", "baja"}
    return ~labels.astype(str).str.strip().str.lower().isin(normal_labels)


def themed_plotly(fig: go.Figure, *, height: int = 340) -> go.Figure:
    fig.update_layout(
        height=height,
        margin=dict(l=24, r=24, t=48, b=28),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=PALETTE["text"], family='Inter, "Segoe UI", Arial, sans-serif'),
        legend=dict(font=dict(color=PALETTE["text"]), bgcolor="rgba(0,0,0,0)"),
        title=dict(font=dict(color=PALETTE["text"], size=16)),
    )
    fig.update_xaxes(gridcolor=PALETTE["border_soft"], zerolinecolor=PALETTE["border"], color=PALETTE["text"])
    fig.update_yaxes(gridcolor=PALETTE["border_soft"], zerolinecolor=PALETTE["border"], color=PALETTE["text"])
    return fig
