"""Generación de reportes exportables (CSV y PDF simple con Matplotlib)."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pandas as pd

if TYPE_CHECKING:
    from src.storage.base_repository import IDSMLRepository

REPORTS_DIR = Path("data/reports")


def ensure_reports_dir() -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    return REPORTS_DIR


def build_summary_dataframe(repo: IDSMLRepository) -> pd.DataFrame:
    experiments = repo.list_experiments(limit=500)
    if not experiments:
        return pd.DataFrame({"mensaje": ["Sin experimentos registrados"]})
    return pd.DataFrame(experiments)


def export_summary_csv(repo: IDSMLRepository, username: str) -> Path:
    """Exporta CSV con experimentos y registra metadatos en el repositorio."""
    ensure_reports_dir()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = REPORTS_DIR / f"idsml_reporte_experimentos_{ts}.csv"
    df = build_summary_dataframe(repo)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    summary = {
        "filas": len(df),
        "columnas": list(df.columns),
    }
    repo.save_report_record(
        title="Resumen de experimentos",
        report_format="csv",
        file_path=str(path.resolve()),
        summary_json=json.dumps(summary, ensure_ascii=False),
        username=username,
    )
    return path


def export_summary_pdf(repo: IDSMLRepository, username: str) -> Path | None:
    """PDF de una página con texto (Matplotlib). Si falla, devuelve ``None``."""
    try:
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_pdf import PdfPages
    except Exception:
        return None

    ensure_reports_dir()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = REPORTS_DIR / f"idsml_reporte_resumen_{ts}.pdf"
    lines = [
        "IDS-ML — Reporte resumen",
        f"Generado: {datetime.now().isoformat()}",
        f"Usuario: {username}",
        "",
        "Conteos:",
        json.dumps(repo.get_dashboard_counts(), indent=2, ensure_ascii=False),
    ]
    fig = plt.figure(figsize=(8.27, 11.69))
    plt.axis("off")
    plt.text(0.05, 0.95, "\n".join(lines), va="top", family="monospace", fontsize=8)
    with PdfPages(path) as pdf:
        pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)
    repo.save_report_record(
        title="Resumen operativo PDF",
        report_format="pdf",
        file_path=str(path.resolve()),
        summary_json=json.dumps({"tipo": "pdf"}, ensure_ascii=False),
        username=username,
    )
    return path
