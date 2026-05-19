"""Inicializa la base relacional academica del sistema IDS-ML."""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

DEFAULT_DB_PATH = Path("idsml_relational.db")
SCHEMA_PATH = Path(__file__).with_name("schema.sql")
SEED_PATH = Path(__file__).with_name("seed_demo.sql")


def execute_script(connection: sqlite3.Connection, script_path: Path) -> None:
    """Ejecuta un script SQL completo en una conexión SQLite."""
    connection.executescript(script_path.read_text(encoding="utf-8"))


def initialize_database(db_path: Path, *, with_seed: bool = True) -> Path:
    """Crea estructura relacional y, opcionalmente, datos demo."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        execute_script(connection, SCHEMA_PATH)
        if with_seed:
            execute_script(connection, SEED_PATH)
    return db_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inicializa la base relacional IDS-ML.")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="Ruta del archivo SQLite a crear.")
    parser.add_argument("--no-seed", action="store_true", help="Crea solo estructura, sin datos demo.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    path = initialize_database(Path(args.db), with_seed=not args.no_seed)
    print(f"Base de datos inicializada: {path.resolve()}")


if __name__ == "__main__":
    main()

