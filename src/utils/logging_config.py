"""Configuración de logging del proyecto."""

from __future__ import annotations

import logging


def configure_logging(level: int = logging.INFO) -> None:
    """Configura logging básico idempotente para ejecución local y pruebas."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

