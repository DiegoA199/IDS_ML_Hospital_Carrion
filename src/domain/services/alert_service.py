"""Servicio de alertas IDS a partir de predicciones."""

from __future__ import annotations

import pandas as pd

from src.alerts.engine import build_alert
from src.core.constants import NORMAL_TRAFFIC_LABELS


def severity_from_label(label: str) -> str:
    """Calcula severidad básica según etiqueta predicha."""
    return "Baja" if str(label).strip().lower() in NORMAL_TRAFFIC_LABELS else "Alta"


def is_threat_label(label: str) -> bool:
    """Indica si una etiqueta representa amenaza."""
    return severity_from_label(label) != "Baja"


def build_alerts_from_predictions(
    pred_df: pd.DataFrame,
    *,
    model_name: str,
    backend: str,
    max_alerts: int = 100,
) -> list[dict]:
    """Convierte predicciones de un lote en alertas persistibles."""
    alerts: list[dict] = []
    for _, row in pred_df.head(max_alerts).iterrows():
        probability = None
        if "confianza" in pred_df.columns and pd.notna(row.get("confianza")):
            probability = float(row["confianza"])
        alerts.append(
            build_alert(
                str(row["prediccion_etiqueta"]),
                probability,
                modelo_usado=model_name,
                backend=backend,
            )
        )
    return alerts

