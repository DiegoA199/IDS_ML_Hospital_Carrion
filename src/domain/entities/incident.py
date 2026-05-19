"""Entidad de incidente de seguridad asociado a alertas."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Incident:
    title: str
    priority: str
    status: str

