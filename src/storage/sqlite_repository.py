from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from src.storage.base_repository import IDSMLRepository

DB_PATH = Path("idsml_local.db")


class SQLiteRepository(IDSMLRepository):
    def __init__(self, db_path: str | Path = DB_PATH):
        self.db_path = Path(db_path)
        self._init_db()

    @property
    def backend_name(self) -> str:
        return "sqlite"

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _ensure_column(self, conn, table: str, column: str, sql_type: str) -> None:
        info = conn.execute(f"PRAGMA table_info({table})").fetchall()
        names = {row[1] for row in info}
        if column not in names:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {sql_type}")

    def _init_db(self):
        with self._connect() as conn:
            conn.execute(
                """
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT,
                amenaza TEXT,
                severidad TEXT,
                impacto TEXT,
                accion_recomendada TEXT,
                probabilidad REAL
            )
            """
            )
            for col, typ in [
                ("probabilidad", "REAL"),
                ("alert_uuid", "TEXT"),
                ("tipo_amenaza", "TEXT"),
                ("modelo_usado", "TEXT"),
                ("estado", "TEXT"),
                ("revisado_por", "TEXT"),
                ("backend", "TEXT"),
            ]:
                self._ensure_column(conn, "alerts", col, typ)

            conn.execute(
                """
            CREATE TABLE IF NOT EXISTS experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT,
                model_name TEXT,
                accuracy REAL,
                precision REAL,
                recall REAL,
                f1_score REAL
            )
            """
            )
            conn.execute(
                """
            CREATE TABLE IF NOT EXISTS prediction_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT,
                model_name TEXT,
                f1_score REAL,
                n_rows INTEGER,
                trained_at_model TEXT,
                details_json TEXT
            )
            """
            )
            conn.execute(
                """
            CREATE TABLE IF NOT EXISTS prediction_rows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER NOT NULL,
                row_index INTEGER NOT NULL,
                label TEXT,
                confidence REAL,
                created_at TEXT
            )
            """
            )
            conn.execute(
                """
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT,
                level TEXT,
                message TEXT,
                extra_json TEXT
            )
            """
            )
            conn.execute(
                """
            CREATE TABLE IF NOT EXISTS audit_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                username TEXT,
                role TEXT,
                action TEXT NOT NULL,
                module TEXT NOT NULL,
                result TEXT NOT NULL,
                observation TEXT,
                level TEXT,
                extra_json TEXT
            )
            """
            )
            conn.execute(
                """
            CREATE TABLE IF NOT EXISTS system_errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT,
                source TEXT,
                message TEXT,
                extra_json TEXT
            )
            """
            )
            conn.execute(
                """
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT,
                title TEXT,
                report_format TEXT,
                file_path TEXT,
                summary_json TEXT,
                username TEXT
            )
            """
            )
            conn.execute(
                """
            CREATE TABLE IF NOT EXISTS model_versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                registered_at TEXT,
                model_name TEXT,
                f1_score REAL,
                bundle_path TEXT,
                version_label TEXT,
                is_active INTEGER DEFAULT 0
            )
            """
            )
            conn.execute(
                """
            CREATE TABLE IF NOT EXISTS test_plan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL UNIQUE,
                module TEXT NOT NULL,
                description TEXT NOT NULL,
                test_type TEXT NOT NULL,
                standard TEXT NOT NULL,
                input_data TEXT,
                expected_result TEXT NOT NULL,
                obtained_result TEXT,
                status TEXT NOT NULL DEFAULT 'Pendiente',
                responsible TEXT NOT NULL,
                execution_date TEXT NOT NULL,
                evidence TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
            )
            conn.execute(
                """
            CREATE TABLE IF NOT EXISTS literature_implementation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_code TEXT NOT NULL UNIQUE,
                authors TEXT NOT NULL,
                year INTEGER NOT NULL,
                title TEXT NOT NULL,
                source TEXT NOT NULL,
                contribution_type TEXT NOT NULL,
                problem TEXT NOT NULL,
                method TEXT NOT NULL,
                technologies TEXT NOT NULL,
                main_results TEXT NOT NULL,
                relation_with_project TEXT NOT NULL,
                related_dimension TEXT NOT NULL,
                citation_format TEXT NOT NULL,
                link_or_doi TEXT,
                observations TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
            )

    def save_alert(self, alert: dict) -> str:
        aid = str(alert.get("alert_uuid") or uuid.uuid4())
        now = datetime.now().isoformat()
        tipo = alert.get("tipo_amenaza") or alert.get("amenaza")
        with self._connect() as conn:
            conn.execute(
                """INSERT INTO alerts (
                    created_at, amenaza, severidad, impacto, accion_recomendada, probabilidad,
                    alert_uuid, tipo_amenaza, modelo_usado, estado, revisado_por, backend
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    now,
                    alert.get("amenaza"),
                    alert.get("severidad"),
                    alert.get("impacto"),
                    alert.get("accion_recomendada"),
                    alert.get("probabilidad"),
                    aid,
                    tipo,
                    alert.get("modelo_usado"),
                    alert.get("estado") or "nueva",
                    alert.get("revisado_por"),
                    alert.get("backend") or self.backend_name,
                ),
            )
        return aid

    def list_alerts(self, limit: int = 200) -> list[dict[str, Any]]:
        with self._connect() as conn:
            cur = conn.execute(
                """SELECT id, alert_uuid, created_at, COALESCE(tipo_amenaza, amenaza) AS tipo,
                          severidad, probabilidad, modelo_usado, impacto, accion_recomendada,
                          COALESCE(estado,'nueva') AS estado, revisado_por, COALESCE(backend,?) AS backend
                   FROM alerts ORDER BY id DESC LIMIT ?""",
                (self.backend_name, limit),
            )
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]

    def update_alert_status(self, alert_id: str, status: str, reviewer_role: str) -> bool:
        with self._connect() as conn:
            cur = conn.execute(
                """UPDATE alerts SET estado=?, revisado_por=? WHERE alert_uuid=? OR CAST(id AS TEXT)=?""",
                (status, reviewer_role, alert_id, alert_id),
            )
            return cur.rowcount > 0

    def save_experiment(self, model_name: str, metrics: dict) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO experiments (created_at, model_name, accuracy, precision, recall, f1_score) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    datetime.now().isoformat(),
                    model_name,
                    metrics.get("accuracy"),
                    metrics.get("precision"),
                    metrics.get("recall"),
                    metrics.get("f1_score"),
                ),
            )
            return int(cur.lastrowid)

    def list_experiments(self, limit: int = 200) -> list[dict[str, Any]]:
        with self._connect() as conn:
            cur = conn.execute(
                "SELECT id, created_at, model_name, accuracy, precision, recall, f1_score FROM experiments ORDER BY id DESC LIMIT ?",
                (limit,),
            )
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]

    def save_prediction_run(
        self,
        *,
        model_name: str,
        f1_score: float,
        n_rows: int,
        trained_at_model: str,
        details: list[dict] | str,
    ) -> int:
        if isinstance(details, str):
            payload = details
        else:
            payload = json.dumps(details, ensure_ascii=False)
        with self._connect() as conn:
            cur = conn.execute(
                """INSERT INTO prediction_runs
                   (created_at, model_name, f1_score, n_rows, trained_at_model, details_json)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    datetime.now().isoformat(),
                    model_name,
                    float(f1_score),
                    int(n_rows),
                    trained_at_model,
                    payload,
                ),
            )
            return int(cur.lastrowid)

    def list_prediction_runs(self, limit: int = 50) -> list[dict[str, Any]]:
        with self._connect() as conn:
            cur = conn.execute(
                """SELECT id, created_at, model_name, f1_score, n_rows, trained_at_model
                   FROM prediction_runs ORDER BY id DESC LIMIT ?""",
                (limit,),
            )
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]

    def save_prediction_rows(self, run_id: int, rows: list[dict[str, Any]]) -> None:
        if not rows:
            return
        now = datetime.now().isoformat()
        with self._connect() as conn:
            conn.executemany(
                """INSERT INTO prediction_rows (run_id, row_index, label, confidence, created_at)
                   VALUES (?,?,?,?,?)""",
                [
                    (
                        run_id,
                        int(r.get("row_index", 0)),
                        str(r.get("label", "")),
                        r.get("confidence"),
                        now,
                    )
                    for r in rows
                ],
            )

    def list_prediction_rows(self, run_id: int, limit: int = 500) -> list[dict[str, Any]]:
        with self._connect() as conn:
            cur = conn.execute(
                """SELECT id, run_id, row_index, label, confidence, created_at
                   FROM prediction_rows WHERE run_id=? ORDER BY id ASC LIMIT ?""",
                (run_id, limit),
            )
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]

    def save_audit_event(
        self,
        *,
        username: str,
        role: str,
        action: str,
        module: str,
        result: str,
        observation: str = "",
        level: str = "INFO",
        extra: dict | None = None,
    ) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                """INSERT INTO audit_events
                   (created_at, username, role, action, module, result, observation, level, extra_json)
                   VALUES (?,?,?,?,?,?,?,?,?)""",
                (
                    datetime.now().isoformat(),
                    username,
                    role,
                    action,
                    module,
                    result,
                    observation,
                    level,
                    json.dumps(extra or {}, ensure_ascii=False),
                ),
            )
            return int(cur.lastrowid)

    def save_audit_log(self, level: str, message: str, extra: dict | None = None) -> int:
        return self.save_audit_event(
            username="sistema",
            role="-",
            action=message,
            module="legacy",
            result="registrado",
            observation="",
            level=level,
            extra=extra,
        )

    def list_audit_events(self, limit: int = 150) -> list[dict[str, Any]]:
        with self._connect() as conn:
            cur = conn.execute(
                """SELECT id, created_at, username, role, action, module, result, observation, level, extra_json
                   FROM audit_events ORDER BY id DESC LIMIT ?""",
                (limit,),
            )
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]

    def list_audit_log(self, limit: int = 100) -> list[tuple[Any, ...]]:
        rows = self.list_audit_events(limit)
        return [
            (r["created_at"], r.get("level", "INFO"), r.get("action", ""), r.get("extra_json", "{}"))
            for r in rows
        ]

    def save_system_error(self, source: str, message: str, extra: dict | None = None) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO system_errors (created_at, source, message, extra_json) VALUES (?,?,?,?)",
                (datetime.now().isoformat(), source, message, json.dumps(extra or {}, ensure_ascii=False)),
            )
            return int(cur.lastrowid)

    def list_system_errors(self, limit: int = 50) -> list[dict[str, Any]]:
        with self._connect() as conn:
            cur = conn.execute(
                "SELECT id, created_at, source, message, extra_json FROM system_errors ORDER BY id DESC LIMIT ?",
                (limit,),
            )
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]

    def save_report_record(
        self,
        *,
        title: str,
        report_format: str,
        file_path: str,
        summary_json: str,
        username: str,
    ) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                """INSERT INTO reports (created_at, title, report_format, file_path, summary_json, username)
                   VALUES (?,?,?,?,?,?)""",
                (datetime.now().isoformat(), title, report_format, file_path, summary_json, username),
            )
            return int(cur.lastrowid)

    def list_reports(self, limit: int = 30) -> list[dict[str, Any]]:
        with self._connect() as conn:
            cur = conn.execute(
                "SELECT id, created_at, title, report_format, file_path, summary_json, username FROM reports ORDER BY id DESC LIMIT ?",
                (limit,),
            )
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]

    def register_model_version(
        self,
        *,
        model_name: str,
        f1_score: float,
        bundle_path: str,
        version_label: str,
    ) -> int:
        now = datetime.now().isoformat()
        with self._connect() as conn:
            conn.execute("UPDATE model_versions SET is_active=0")
            cur = conn.execute(
                """INSERT INTO model_versions (registered_at, model_name, f1_score, bundle_path, version_label, is_active)
                   VALUES (?,?,?,?,?,1)""",
                (now, model_name, float(f1_score), bundle_path, version_label),
            )
            return int(cur.lastrowid)

    def get_active_model_version(self) -> dict[str, Any] | None:
        with self._connect() as conn:
            row = conn.execute(
                """SELECT id, registered_at, model_name, f1_score, bundle_path, version_label
                   FROM model_versions WHERE is_active=1 ORDER BY id DESC LIMIT 1"""
            ).fetchone()
        if not row:
            return None
        cols = ["id", "registered_at", "model_name", "f1_score", "bundle_path", "version_label"]
        return dict(zip(cols, row))

    def save_test_case(self, test_case: dict[str, Any]) -> int:
        now = datetime.now().isoformat()
        with self._connect() as conn:
            cur = conn.execute(
                """INSERT INTO test_plan (
                    code, module, description, test_type, standard, input_data,
                    expected_result, obtained_result, status, responsible,
                    execution_date, evidence, created_at, updated_at
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    test_case["code"], test_case["module"], test_case["description"],
                    test_case["test_type"], test_case["standard"], test_case.get("input_data", ""),
                    test_case["expected_result"], test_case.get("obtained_result", ""),
                    test_case.get("status", "Pendiente"), test_case["responsible"],
                    test_case["execution_date"], test_case.get("evidence", ""), now, now,
                ),
            )
            return int(cur.lastrowid)

    def list_test_cases(self, limit: int = 1000) -> list[dict[str, Any]]:
        with self._connect() as conn:
            cur = conn.execute(
                """SELECT id, code, module, description, test_type, standard, input_data,
                          expected_result, obtained_result, status, responsible,
                          execution_date, evidence, created_at, updated_at
                   FROM test_plan ORDER BY code ASC LIMIT ?""",
                (limit,),
            )
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]

    def update_test_case_status(
        self, code: str, status: str, obtained_result: str = "", evidence: str = ""
    ) -> bool:
        with self._connect() as conn:
            cur = conn.execute(
                """UPDATE test_plan
                   SET status=?, obtained_result=?, evidence=?, updated_at=?
                   WHERE code=?""",
                (status, obtained_result, evidence, datetime.now().isoformat(), code),
            )
            return cur.rowcount > 0

    def save_literature_article(self, article: dict[str, Any]) -> int:
        now = datetime.now().isoformat()
        with self._connect() as conn:
            cur = conn.execute(
                """INSERT INTO literature_implementation (
                    article_code, authors, year, title, source, contribution_type,
                    problem, method, technologies, main_results, relation_with_project,
                    related_dimension, citation_format, link_or_doi, observations,
                    created_at, updated_at
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    article["article_code"], article["authors"], int(article["year"]),
                    article["title"], article["source"], article["contribution_type"],
                    article["problem"], article["method"], article["technologies"],
                    article["main_results"], article["relation_with_project"],
                    article["related_dimension"], article["citation_format"],
                    article.get("link_or_doi", ""), article.get("observations", ""), now, now,
                ),
            )
            return int(cur.lastrowid)

    def list_literature_articles(self, limit: int = 1000) -> list[dict[str, Any]]:
        with self._connect() as conn:
            cur = conn.execute(
                """SELECT id, article_code, authors, year, title, source, contribution_type,
                          problem, method, technologies, main_results, relation_with_project,
                          related_dimension, citation_format, link_or_doi, observations,
                          created_at, updated_at
                   FROM literature_implementation ORDER BY year DESC, article_code ASC LIMIT ?""",
                (limit,),
            )
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]

    def get_dashboard_counts(self) -> dict[str, int]:
        with self._connect() as conn:
            def c(sql: str) -> int:
                r = conn.execute(sql).fetchone()
                return int(r[0] or 0)

            amenazas = c(
                """SELECT COUNT(*) FROM prediction_rows WHERE label IS NOT NULL
                   AND lower(CAST(label AS TEXT)) NOT IN ('normal','0','benign')"""
            )
            out = {
                "experiments": c("SELECT COUNT(*) FROM experiments"),
                "alerts": c("SELECT COUNT(*) FROM alerts"),
                "prediction_runs": c("SELECT COUNT(*) FROM prediction_runs"),
                "prediction_rows": c("SELECT COUNT(*) FROM prediction_rows"),
                "amenazas_detectadas": amenazas,
                "audit_events": c("SELECT COUNT(*) FROM audit_events"),
                "system_errors": c("SELECT COUNT(*) FROM system_errors"),
                "reports": c("SELECT COUNT(*) FROM reports"),
            }
        return out
