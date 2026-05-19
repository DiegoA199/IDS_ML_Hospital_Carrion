"""Formateadores de valores usados por UI, reportes y pruebas."""

from __future__ import annotations


def as_percent(value: float | None, digits: int = 2) -> str:
    """Formatea un valor 0..1 o 0..100 como porcentaje."""
    if value is None:
        return "0.00%"
    number = float(value)
    if number <= 1:
        number *= 100
    return f"{number:.{digits}f}%"


def compact_int(value: int | float | None) -> str:
    """Formatea enteros con separador de miles."""
    if value is None:
        return "0"
    return f"{int(value):,}"

