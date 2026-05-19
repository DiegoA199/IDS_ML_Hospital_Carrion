"""Servicio básico para mapear alertas a incidentes de seguridad."""

from __future__ import annotations


def classify_incident_priority(severity: str) -> str:
    """Convierte severidad de alerta en prioridad de incidente."""
    normalized = severity.strip().lower()
    if normalized in {"alta", "crítica", "critica", "critical"}:
        return "alta"
    if normalized in {"media", "moderada"}:
        return "media"
    return "baja"

