"""Entidad de alerta IDS generada por predicción."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Alert:
    threat_type: str
    severity: str
    probability: float | None
    status: str = "nueva"

