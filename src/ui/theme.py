"""Reusable visual layer for the IDS-ML Streamlit interface."""

from __future__ import annotations

from html import escape
from textwrap import dedent
from typing import Any

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

PALETTE = {
    "background": "#f6f8fd",
    "surface": "#ffffff",
    "surface_high": "#eef4ff",
    "surface_higher": "#e2ecff",
    "border": "#c9d0dc",
    "border_soft": "#e2e8f0",
    "text": "#0b1c30",
    "muted": "#687080",
    "blue": "#075fc7",
    "blue_deep": "#004ba8",
    "green": "#07885f",
    "amber": "#a85d00",
    "red": "#ba1a1a",
    "slate": "#526071",
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
    """Apply the clinical monitoring visual system used across pages."""
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
            background: var(--ids-bg);
            color: var(--ids-text);
        }}

        [data-testid="stHeader"] {{
            height: 0;
            min-height: 0;
            background: transparent;
        }}

        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"] {{
            visibility: hidden;
            height: 0;
            position: fixed;
        }}

        [data-testid="stSidebar"] {{
            background: #111b2f;
            border-right: 0;
            min-width: 260px;
            max-width: 260px;
        }}

        [data-testid="stSidebarHeader"] {{
            display: none;
        }}

        [data-testid="stSidebarContent"] {{
            padding: 0 !important;
        }}

        [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] {{
            gap: 0 !important;
        }}

        [data-testid="stSidebar"] * {{
            color: #dce6f7;
        }}

        [data-testid="stSidebar"] .stButton > button {{
            width: 100%;
            justify-content: flex-start;
            text-align: left;
            min-height: 3.75rem;
            border-radius: 0;
            border: 0;
            background: transparent;
            color: #8490a6;
            font-weight: 700;
            padding: 0 1.45rem;
            letter-spacing: 0.01em;
        }}

        [data-testid="stSidebar"] .stButton > button:hover {{
            background: #17243c;
            color: #ffffff;
        }}

        [data-testid="stSidebar"] .stButton > button[kind="primary"] {{
            background: #0864ca;
            border-left: 4px solid #b8d2ff;
            color: #ffffff;
            box-shadow: none;
            padding-left: calc(1.45rem - 4px);
        }}

        [data-testid="stSidebar"] .stButton > button p {{
            white-space: normal;
            line-height: 1.1rem;
        }}

        [data-testid="stSidebar"] [role="radiogroup"] label {{
            border-radius: 8px;
            padding: 0.55rem 0.7rem;
            margin: 0.18rem 0;
            border: 1px solid transparent;
        }}

        [data-testid="stSidebar"] [role="radiogroup"] label:hover {{
            background: rgba(33, 112, 228, 0.14);
            border-color: rgba(173, 198, 255, 0.26);
        }}

        [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {{
            background: #0864ca;
            border-color: #2170e4;
            box-shadow: none;
        }}

        .main .block-container {{
            max-width: none;
            padding: 0 2rem 3rem 2rem;
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
            border-radius: 6px;
            border: 1px solid #0058be;
            background: #0058be;
            color: #ffffff;
            font-weight: 700;
            min-height: 2.7rem;
        }}

        button[kind="secondary"] {{
            background: #ffffff;
            color: #0058be;
            border-color: #9aabc2;
        }}

        .stButton > button:hover,
        .stDownloadButton > button:hover {{
            border-color: #004395;
            background: #004395;
            color: #ffffff;
        }}

        div[data-testid="stFileUploader"] section {{
            background: #ffffff;
            border: 1px dashed #9aabc2;
            border-radius: 10px;
            min-height: 190px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        div[data-testid="stFileUploader"] section:hover {{
            border-color: var(--ids-blue);
            box-shadow: 0 0 0 2px rgba(0, 88, 190, 0.10);
        }}

        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        div[data-baseweb="textarea"] > div,
        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input {{
            background: #f3f6fc;
            border-color: #9aabc2;
            color: var(--ids-text);
            border-radius: 6px;
        }}

        .stDataFrame,
        [data-testid="stTable"] {{
            border: 1px solid var(--ids-border);
            border-radius: 8px;
            overflow: hidden;
        }}

        .stAlert {{
            border-radius: 6px;
            border: 1px solid #c8d7ed;
            background: #eff4ff;
        }}

        .ids-page-head {{
            display: flex;
            justify-content: space-between;
            gap: 1.5rem;
            align-items: center;
            min-height: 5rem;
            border-bottom: 1px solid var(--ids-border);
            padding: 0.8rem 2rem;
            margin: 0 -2rem 1.5rem -2rem;
            background: #ffffff;
        }}

        .ids-head-actions {{
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: 0.85rem;
        }}

        .ids-search-box {{
            min-width: 300px;
            padding: 0.72rem 1rem;
            border: 1px solid #b9c3d2;
            border-radius: 12px;
            background: #eef4ff;
            color: #6d7481;
            font-size: 0.92rem;
        }}

        .ids-head-icon {{
            width: 2.2rem;
            height: 2.2rem;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            color: #111827;
            font-weight: 800;
            font-size: 1.1rem;
        }}

        .ids-user-avatar {{
            width: 2.3rem;
            height: 2.3rem;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            background: #d8e7ff;
            color: var(--ids-blue);
            border: 1px solid #a9c4ee;
            font-weight: 850;
        }}

        .ids-title {{
            font-size: 1.35rem;
            line-height: 1.7rem;
            font-weight: 800;
            color: var(--ids-blue);
            margin: 0;
        }}

        .ids-kicker {{
            display: none;
        }}

        .ids-subtitle {{
            color: var(--ids-muted);
            font-size: 0.9rem;
            margin-top: 0.2rem;
            max-width: 820px;
        }}

        .ids-page-context {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin: -0.55rem 0 1.25rem 0;
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
            border: 1px solid rgba(0, 88, 190, 0.28);
            background: rgba(0, 88, 190, 0.08);
            color: var(--ids-blue);
            white-space: nowrap;
        }}

        .ids-card {{
            background: #ffffff;
            border: 1px solid var(--ids-border);
            border-radius: 10px;
            padding: 1.25rem;
            min-height: 100%;
            box-shadow: 0 2px 5px rgba(15, 23, 42, 0.025);
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

        .ids-recommendation {{
            min-height: 420px;
            padding: 1.55rem;
            border-radius: 10px;
            background: #111b2f;
            color: #eef4ff;
            border: 1px solid #26354f;
        }}

        .ids-recommendation-badge {{
            display: inline-block;
            padding: .32rem .65rem;
            border-radius: 999px;
            background: #173d78;
            color: #d9e8ff;
            font-size: .7rem;
            font-weight: 850;
            text-transform: uppercase;
        }}

        .ids-recommendation h3 {{
            color: #ffffff;
            font-size: 1.45rem;
            margin: 1.15rem 0 .65rem 0;
        }}

        .ids-recommendation p {{
            color: #c4d0e4;
            font-size: .9rem;
            line-height: 1.45rem;
        }}

        .ids-recommendation-metric {{
            margin-top: 1rem;
            padding: .85rem;
            background: #1b2943;
            border-radius: 7px;
            color: #ffffff;
            font-weight: 800;
        }}

        .ids-metric-title {{
            color: #45464d;
            font-size: 0.76rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em !important;
            margin-bottom: 0.8rem;
        }}

        .ids-metric-value {{
            color: var(--ids-text);
            font-size: 2rem;
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
            background: #d8e2ff;
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
            grid-template-columns: 1fr;
            gap: 0;
            margin: 0.5rem 0 1.1rem 0;
            padding: 0.6rem 1.3rem;
            background: #ffffff;
            border: 1px solid var(--ids-border);
            border-radius: 10px;
        }}

        .ids-step {{
            border: 0;
            border-bottom: 1px solid var(--ids-border-soft);
            border-radius: 0;
            background: #ffffff;
            padding: 1.15rem 1rem;
        }}

        .ids-step:last-child {{
            border-bottom: 0;
        }}

        .ids-step[data-state="done"] {{
            border-left: 4px solid var(--ids-green);
        }}

        .ids-step[data-state="active"] {{
            border-left: 4px solid var(--ids-blue);
            box-shadow: 0 0 0 1px rgba(0, 88, 190, 0.16);
        }}

        .ids-step[data-state="pending"] {{
            border-left: 4px solid #c6cbd5;
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

        .ids-login-hero {{
            max-width: 620px;
            margin: 4.5rem auto 1.6rem auto;
            text-align: center;
        }}

        .ids-login-hero .ids-title {{
            color: var(--ids-text);
            font-size: 2rem;
            line-height: 2.4rem;
        }}

        .ids-login-mark {{
            width: 72px;
            height: 72px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            background: #111b2f;
            color: #46a5c8;
            font-size: 1.75rem;
            font-weight: 850;
            margin-bottom: 1rem;
        }}

        .ids-sidebar-brand {{
            height: 7rem;
            display: flex;
            align-items: center;
            gap: 0.8rem;
            padding: 0 1.45rem;
            border-bottom: 1px solid #26354f;
            margin: 0 0 0.75rem 0;
        }}

        .ids-brand-mark {{
            width: 2.65rem;
            height: 2.65rem;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 5px;
            background: #0b4b68;
            color: #63c4df;
            font-size: 1.45rem;
            font-weight: 900;
        }}

        .ids-brand {{
            color: #ffffff;
            font-size: 1.35rem;
            font-weight: 850;
        }}

        .ids-sidebar-meta {{
            color: #8e9bb0;
            font-size: 0.78rem;
            margin-top: 0.2rem;
        }}

        [data-testid="stForm"] {{
            background: #ffffff;
            border: 1px solid var(--ids-border);
            border-radius: 12px;
            padding: 1.7rem 2rem 1.5rem 2rem;
            box-shadow: 0 8px 28px rgba(15, 23, 42, 0.06);
        }}

        .ids-login-form-head {{
            margin-bottom: 1rem;
        }}

        .ids-login-help {{
            color: var(--ids-blue);
            text-align: right;
            padding-top: 0.45rem;
            font-size: 0.86rem;
        }}

        .ids-login-secure {{
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid var(--ids-border);
            color: #6b7280;
            text-align: center;
            font-size: 0.72rem;
            font-weight: 750;
            letter-spacing: 0.08em !important;
        }}

        .ids-login-footer {{
            color: #858b96;
            text-align: center;
            font-size: 0.76rem;
            margin-top: 1.1rem;
        }}

        @media (max-width: 900px) {{
            .ids-page-head {{
                display: block;
            }}

            .ids-title {{
                font-size: 1.15rem;
                line-height: 1.5rem;
            }}

            .ids-search-box,
            .ids-user-meta {{
                display: none;
            }}

            .ids-metric-value {{
                font-size: 1.65rem;
                line-height: 1.95rem;
            }}
        }}
        </style>
        """
    )


def page_header(title: str, subtitle: str = "", kicker: str = "IDS-ML", tag: str | None = None) -> None:
    username = str(st.session_state.get("username", "usuario"))
    role = str(st.session_state.get("role", "Operador"))
    initial = username[:1].upper() if username else "U"
    tag_html = f'<span class="ids-top-tag">{escape(tag)}</span>' if tag else ""
    _html(
        f"""
        <div class="ids-page-head">
            <div>
                <div class="ids-kicker">{escape(kicker)}</div>
                <div class="ids-title">{escape(title)}</div>
            </div>
            <div class="ids-head-actions">
                <div class="ids-search-box">⌕ &nbsp; Buscar eventos, registros...</div>
                <div class="ids-head-icon">♟</div>
                <div class="ids-head-icon">?</div>
                <div class="ids-user-avatar">{escape(initial)}</div>
                <div class="ids-user-meta">
                    <div style="font-weight:800; color:var(--ids-text);">{escape(username)}</div>
                    <div style="font-size:.72rem; color:var(--ids-muted);">{escape(role)}</div>
                </div>
            </div>
        </div>
        <div class="ids-page-context">
            <div class="ids-subtitle">{escape(subtitle)}</div>
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
    icon = {"blue": "▣", "green": "✓", "red": "!", "amber": "◇", "slate": "◷"}.get(tone, "▣")
    progress_html = ""
    if progress is not None:
        pct = max(0.0, min(100.0, float(progress)))
        progress_html = (
            f'<div class="ids-progress"><span style="width: {pct:.2f}%; background: {color};"></span></div>'
        )
    _html(
        '<div class="ids-card">'
        f'<div style="display:flex;justify-content:space-between;gap:.6rem;align-items:flex-start;">'
        f'<div class="ids-metric-title">{escape(title)}</div>'
        f'<div style="width:2.15rem;height:2.15rem;border-radius:6px;background:{color}18;color:{color};'
        f'display:flex;align-items:center;justify-content:center;font-weight:900;">{icon}</div>'
        '</div>'
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
