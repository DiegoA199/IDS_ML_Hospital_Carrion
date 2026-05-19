"""Entidad de evento o flujo de red evaluable por IDS-ML."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class NetworkEvent:
    source_ip: str | None
    destination_ip: str | None
    protocol: str | None
    features: dict[str, Any]

