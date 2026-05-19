"""Entidad de metadatos de reporte generado."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReportMetadata:
    title: str
    report_format: str
    file_path: str
    username: str

