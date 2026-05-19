"""Constantes centralizadas para evitar valores quemados dispersos."""

from __future__ import annotations

ROLE_ADMIN = "Administrador TI"
ROLE_ANALYST = "Analista TI"
ROLE_GUEST = "Invitado/demo"

SUPPORTED_ROLES = (ROLE_ADMIN, ROLE_ANALYST, ROLE_GUEST)
NORMAL_TRAFFIC_LABELS = {"normal", "0", "benign", "benigno", "baja"}

DEFAULT_RANDOM_STATE = 42
DEFAULT_TEST_SIZE = 0.25
DEFAULT_MAX_ALERTS_PER_BATCH = 100

