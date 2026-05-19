"""Entidades relacionadas con datasets IDS."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DatasetProfile:
    rows: int
    columns: int
    missing_total: int
    duplicated_rows: int

