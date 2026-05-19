"""Carga de datasets para flujos ML."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_csv_dataset(path: str | Path) -> pd.DataFrame:
    """Carga un CSV desde disco para pruebas o ejecución batch."""
    return pd.read_csv(path)

