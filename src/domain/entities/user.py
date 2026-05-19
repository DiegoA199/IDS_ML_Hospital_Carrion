"""Entidad de usuario institucional."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    username: str
    role: str
    is_active: bool = True

