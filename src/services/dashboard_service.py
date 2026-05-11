"""Métricas agregadas para el dashboard operativo."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pandas as pd

if TYPE_CHECKING:
    from src.storage.base_repository import IDSMLRepository


def build_dashboard_context(repo: IDSMLRepository) -> dict[str, Any]:
    counts = repo.get_dashboard_counts()
    experiments = repo.list_experiments(limit=50)
    alerts = repo.list_alerts(limit=200)
    active = repo.get_active_model_version()
    audit = repo.list_audit_events(limit=20)

    sev_counts: dict[str, int] = {}
    for a in alerts:
        s = str(a.get("severidad") or "—")
        sev_counts[s] = sev_counts.get(s, 0) + 1

    tipo_counts: dict[str, int] = {}
    for a in alerts:
        t = str(a.get("tipo_amenaza") or a.get("amenaza") or "—")
        tipo_counts[t] = tipo_counts.get(t, 0) + 1

    best_f1 = None
    best_name = None
    if experiments:
        df = pd.DataFrame(experiments)
        if not df.empty and "f1_score" in df.columns and df["f1_score"].notna().any():
            i = int(df["f1_score"].idxmax())
            best_f1 = float(df.loc[i, "f1_score"])
            best_name = str(df.loc[i, "model_name"])

    runs = repo.list_prediction_runs(limit=1)
    last_pred = runs[0]["created_at"] if runs else None

    return {
        "counts": counts,
        "severity_distribution": sev_counts,
        "threat_type_distribution": tipo_counts,
        "experiments_sample": experiments[:10],
        "recent_alerts": alerts[:15],
        "active_model": active,
        "best_f1_session": best_f1,
        "best_name_session": best_name,
        "recent_audit": audit,
        "last_prediction_at": last_pred,
    }
