"""Visor HTTP local para revisar el modelo de base de datos IDS-ML."""

from __future__ import annotations

import argparse
import html
import sqlite3
import sys
from collections import defaultdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.services.database_model_service import (
    DBML_PATH,
    POSTGRES_SCHEMA_PATH,
    SQLITE_SCHEMA_PATH,
    parse_tables,
    read_schema,
)
from database.init_db import initialize_database


RELATIONAL_DB_PATH = PROJECT_ROOT / "data" / "processed" / "idsml_relational_test.db"


def _database_status() -> tuple[str, int]:
    if not RELATIONAL_DB_PATH.exists():
        initialize_database(RELATIONAL_DB_PATH)
    with sqlite3.connect(RELATIONAL_DB_PATH) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        ).fetchone()[0]
    return str(RELATIONAL_DB_PATH), int(count)


def _group_tables():
    tables = parse_tables(read_schema(SQLITE_SCHEMA_PATH))
    groups = defaultdict(list)
    for table in tables:
        groups[table.module].append(table)
    return tables, dict(sorted(groups.items()))


def _render_table_cards(groups) -> str:
    sections = []
    for module, tables in groups.items():
        cards = []
        for table in sorted(tables, key=lambda item: item.name):
            columns = ", ".join(table.columns[:6])
            if len(table.columns) > 6:
                columns += ", ..."
            cards.append(
                f"""
                <article class="table-card">
                    <div class="table-name">{html.escape(table.name)}</div>
                    <div class="table-meta">{len(table.columns)} campos · {len(table.foreign_keys)} FK</div>
                    <p>{html.escape(columns)}</p>
                </article>
                """
            )
        sections.append(
            f"""
            <section class="module">
                <h2>{html.escape(module)} <span>{len(tables)} tablas</span></h2>
                <div class="table-grid">{''.join(cards)}</div>
            </section>
            """
        )
    return "\n".join(sections)


def _render_relationship_rows(tables) -> str:
    rows = []
    for table in tables:
        for foreign_key in table.foreign_keys:
            rows.append(
                f"""
                <tr>
                    <td>{html.escape(foreign_key.source_table)}</td>
                    <td>{html.escape(foreign_key.source_column)}</td>
                    <td>{html.escape(foreign_key.target_table)}</td>
                    <td>{html.escape(foreign_key.target_column)}</td>
                </tr>
                """
            )
    return "".join(rows)


def _build_home() -> bytes:
    tables, groups = _group_tables()
    db_path, db_table_count = _database_status()
    relationship_count = sum(len(table.foreign_keys) for table in tables)
    body = f"""
    <!doctype html>
    <html lang="es">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>IDS-ML | Visor de base de datos</title>
        <style>
            :root {{
                color-scheme: light;
                --bg: #f5f7fb;
                --panel: #ffffff;
                --line: #d9e2ef;
                --ink: #102033;
                --muted: #5f7288;
                --blue: #0f4c81;
                --cyan: #0ea5e9;
                --green: #15803d;
                --red: #b42318;
            }}
            * {{ box-sizing: border-box; }}
            body {{
                margin: 0;
                font-family: Inter, Segoe UI, Arial, sans-serif;
                color: var(--ink);
                background: var(--bg);
            }}
            header {{
                padding: 34px 46px 24px;
                color: #fff;
                background: linear-gradient(135deg, #0b1d35, #0f4c81);
                border-bottom: 4px solid var(--cyan);
            }}
            header p {{ max-width: 960px; color: #dceaf7; margin: 8px 0 0; }}
            main {{ padding: 28px 46px 42px; }}
            .kpis {{
                display: grid;
                grid-template-columns: repeat(4, minmax(160px, 1fr));
                gap: 14px;
                margin-bottom: 24px;
            }}
            .kpi, .module, .relations {{
                background: var(--panel);
                border: 1px solid var(--line);
                border-radius: 8px;
                box-shadow: 0 10px 30px rgba(15, 76, 129, 0.08);
            }}
            .kpi {{ padding: 18px; }}
            .kpi strong {{ display: block; font-size: 28px; color: var(--blue); }}
            .kpi span {{ color: var(--muted); font-size: 13px; }}
            .paths {{
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
                margin: 14px 0 26px;
            }}
            .paths a {{
                color: var(--blue);
                background: #e8f3fc;
                border: 1px solid #bdddf5;
                border-radius: 999px;
                padding: 8px 12px;
                text-decoration: none;
                font-weight: 600;
                font-size: 13px;
            }}
            .module {{ margin: 16px 0; padding: 18px; }}
            .module h2 {{ margin: 0 0 14px; font-size: 18px; }}
            .module h2 span {{ color: var(--muted); font-size: 13px; font-weight: 500; }}
            .table-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
                gap: 12px;
            }}
            .table-card {{
                min-height: 118px;
                padding: 14px;
                border: 1px solid var(--line);
                border-radius: 8px;
                background: #fbfdff;
            }}
            .table-name {{ font-weight: 800; color: var(--blue); }}
            .table-meta {{ margin-top: 4px; color: var(--green); font-size: 12px; font-weight: 700; }}
            .table-card p {{ color: var(--muted); font-size: 12px; line-height: 1.4; }}
            .relations {{ margin-top: 22px; padding: 18px; overflow-x: auto; }}
            table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
            th, td {{ padding: 10px; border-bottom: 1px solid var(--line); text-align: left; }}
            th {{ color: var(--muted); background: #f8fafc; }}
            .status {{ color: var(--muted); margin: 0 0 18px; }}
            @media (max-width: 900px) {{
                main, header {{ padding-left: 20px; padding-right: 20px; }}
                .kpis {{ grid-template-columns: repeat(2, 1fr); }}
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>Visor de base de datos IDS-ML</h1>
            <p>Modelo relacional formal para el prototipo IDS-ML hospitalario. Esta vista sirve para revisar graficamente las tablas, modulos y relaciones sin depender de Docker.</p>
        </header>
        <main>
            <div class="kpis">
                <div class="kpi"><strong>{len(tables)}</strong><span>tablas del esquema</span></div>
                <div class="kpi"><strong>{relationship_count}</strong><span>relaciones FK</span></div>
                <div class="kpi"><strong>{len(groups)}</strong><span>modulos funcionales</span></div>
                <div class="kpi"><strong>{db_table_count}</strong><span>tablas creadas en SQLite</span></div>
            </div>
            <p class="status"><strong>Base SQLite:</strong> {html.escape(db_path)}</p>
            <div class="paths">
                <a href="/schema.sql">Ver schema SQLite</a>
                <a href="/postgresql.sql">Ver schema PostgreSQL</a>
                <a href="/modelo.dbml">Ver DBML</a>
                <a href="http://localhost:8501/" target="_blank">Abrir app IDS-ML</a>
            </div>
            {_render_table_cards(groups)}
            <section class="relations">
                <h2>Relaciones principales</h2>
                <table>
                    <thead>
                        <tr><th>Tabla origen</th><th>Campo</th><th>Tabla destino</th><th>Campo destino</th></tr>
                    </thead>
                    <tbody>{_render_relationship_rows(tables)}</tbody>
                </table>
            </section>
        </main>
    </body>
    </html>
    """
    return body.encode("utf-8")


class DatabaseViewerHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/":
            self._send("text/html; charset=utf-8", _build_home())
            return
        if path == "/schema.sql":
            self._send("text/plain; charset=utf-8", SQLITE_SCHEMA_PATH.read_bytes())
            return
        if path == "/postgresql.sql":
            self._send("text/plain; charset=utf-8", POSTGRES_SCHEMA_PATH.read_bytes())
            return
        if path == "/modelo.dbml":
            self._send("text/plain; charset=utf-8", DBML_PATH.read_bytes())
            return
        self.send_error(404, "Ruta no encontrada")

    def log_message(self, format: str, *args) -> None:
        return

    def _send(self, content_type: str, payload: bytes) -> None:
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def main() -> None:
    parser = argparse.ArgumentParser(description="Visor local de la base IDS-ML.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), DatabaseViewerHandler)
    print(f"Visor de base de datos disponible en http://{args.host}:{args.port}/")
    server.serve_forever()


if __name__ == "__main__":
    main()
