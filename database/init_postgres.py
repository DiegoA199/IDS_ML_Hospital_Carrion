"""Inicializa el modelo relacional PostgreSQL para Docker y Render."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import psycopg2


BASE_DIR = Path(__file__).resolve().parent
POSTGRES_DIR = BASE_DIR / "postgresql"
SCHEMA_PATH = POSTGRES_DIR / "schema.sql"
SEED_PATH = POSTGRES_DIR / "seed_demo.sql"


def _resolve_dsn(explicit_dsn: str | None = None) -> str:
    """Devuelve el DSN PostgreSQL desde argumentos o variables de entorno."""
    dsn = explicit_dsn or os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_DSN")
    if not dsn:
        raise RuntimeError("Defina DATABASE_URL o POSTGRES_DSN para inicializar PostgreSQL.")
    return dsn


def _read_sql(path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"No se encontro el archivo SQL: {path}")
    return path.read_text(encoding="utf-8")


def _seed_exists(cursor) -> bool:
    """Evita duplicar datos demo en reinicios o redeploys."""
    cursor.execute("SELECT EXISTS (SELECT 1 FROM roles LIMIT 1)")
    row = cursor.fetchone()
    return bool(row and row[0])


def initialize_postgres(explicit_dsn: str | None = None, with_seed: bool = True) -> None:
    """Crea las tablas formales y carga datos demo solo si la base esta vacia."""
    dsn = _resolve_dsn(explicit_dsn)
    schema_sql = _read_sql(SCHEMA_PATH)
    seed_sql = _read_sql(SEED_PATH) if with_seed else ""

    with psycopg2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            cursor.execute(schema_sql)
            if with_seed and not _seed_exists(cursor):
                cursor.execute(seed_sql)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inicializa PostgreSQL con el modelo IDS-ML de 62 tablas."
    )
    parser.add_argument("--dsn", help="DSN PostgreSQL. Si se omite usa DATABASE_URL/POSTGRES_DSN.")
    parser.add_argument("--no-seed", action="store_true", help="No carga datos demo.")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    initialize_postgres(args.dsn, with_seed=not args.no_seed)
    print("Base PostgreSQL inicializada correctamente.")


if __name__ == "__main__":
    main()
