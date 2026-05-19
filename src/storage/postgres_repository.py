"""Repositorio PostgreSQL para despliegue Docker/producción controlada."""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from typing import Any

import psycopg2
from psycopg2.extras import RealDictCursor, execute_batch

from src.storage.base_repository import IDSMLRepository


class PostgreSQLRepository(IDSMLRepository):
    """Implementación del contrato IDS-ML usando PostgreSQL."""

    def __init__(self, dsn: str):
        self.dsn = dsn
        self._init_db()

    @classmethod
    def from_settings(cls, settings: dict[str, Any]) -> "PostgreSQLRepository":
        dsn = settings.get("postgres_dsn")
        if not dsn:
            raise ValueError("No se configuró DATABASE_URL/POSTGRES_DSN para PostgreSQL.")
        return cls(str(dsn))

    @property
    def backend_name(self) -> str:
        return "postgres"

    def _connect(self):
        return psycopg2.connect(self.dsn)

    def _init_db(self) -> None:
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS alerts (
                    id BIGSERIAL PRIMARY KEY,
                    created_at TEXT,
                    amenaza TEXT,
                    severidad TEXT,
                    impacto TEXT,
                    accion_recomendada TEXT,
                    probabilidad DOUBLE PRECISION,
                    alert_uuid TEXT UNIQUE,
                    tipo_amenaza TEXT,
                    modelo_usado TEXT,
                    estado TEXT,
                    revisado_por TEXT,
                    backend TEXT
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS experiments (
                    id BIGSERIAL PRIMARY KEY,
                    created_at TEXT,
                    model_name TEXT,
                    accuracy DOUBLE PRECISION,
                    precision DOUBLE PRECISION,
                    recall DOUBLE PRECISION,
                    f1_score DOUBLE PRECISION
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS prediction_runs (
                    id BIGSERIAL PRIMARY KEY,
                    created_at TEXT,
                    model_name TEXT,
                    f1_score DOUBLE PRECISION,
                    n_rows INTEGER,
                    trained_at_model TEXT,
                    details_json TEXT
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS prediction_rows (
                    id BIGSERIAL PRIMARY KEY,
                    run_id INTEGER NOT NULL,
                    row_index INTEGER NOT NULL,
                    label TEXT,
                    confidence DOUBLE PRECISION,
                    created_at TEXT
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS audit_events (
                    id BIGSERIAL PRIMARY KEY,
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
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS system_errors (
                    id BIGSERIAL PRIMARY KEY,
                    created_at TEXT,
                    source TEXT,
                    message TEXT,
                    extra_json TEXT
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS reports (
                    id BIGSERIAL PRIMARY KEY,
                    created_at TEXT,
                    title TEXT,
                    report_format TEXT,
                    file_path TEXT,
                    summary_json TEXT,
                    username TEXT
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS model_versions (
                    id BIGSERIAL PRIMARY KEY,
                    registered_at TEXT,
                    model_name TEXT,
                    f1_score DOUBLE PRECISION,
                    bundle_path TEXT,
                    version_label TEXT,
                    is_active INTEGER DEFAULT 0
                )
                """
            )

    def save_alert(self, alert: dict) -> str:
        aid = str(alert.get("alert_uuid") or uuid.uuid4())
        now = datetime.now().isoformat()
        tipo = alert.get("tipo_amenaza") or alert.get("amenaza")
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO alerts (
                    created_at, amenaza, severidad, impacto, accion_recomendada, probabilidad,
                    alert_uuid, tipo_amenaza, modelo_usado, estado, revisado_por, backend
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,
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
        with self._connect() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT id, alert_uuid, created_at, COALESCE(tipo_amenaza, amenaza) AS tipo,
                       severidad, probabilidad, modelo_usado, impacto, accion_recomendada,
                       COALESCE(estado,'nueva') AS estado, revisado_por, COALESCE(backend,%s) AS backend
                FROM alerts ORDER BY id DESC LIMIT %s
                """,
                (self.backend_name, limit),
            )
            return [dict(row) for row in cur.fetchall()]

    def update_alert_status(self, alert_id: str, status: str, reviewer_role: str) -> bool:
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                "UPDATE alerts SET estado=%s, revisado_por=%s WHERE alert_uuid=%s OR CAST(id AS TEXT)=%s",
                (status, reviewer_role, alert_id, alert_id),
            )
            return bool(cur.rowcount)

    def save_experiment(self, model_name: str, metrics: dict) -> int:
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO experiments (created_at, model_name, accuracy, precision, recall, f1_score)
                VALUES (%s,%s,%s,%s,%s,%s) RETURNING id
                """,
                (
                    datetime.now().isoformat(),
                    model_name,
                    metrics.get("accuracy"),
                    metrics.get("precision"),
                    metrics.get("recall"),
                    metrics.get("f1_score"),
                ),
            )
            return int(cur.fetchone()[0])

    def list_experiments(self, limit: int = 200) -> list[dict[str, Any]]:
        with self._connect() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT id, created_at, model_name, accuracy, precision, recall, f1_score
                FROM experiments ORDER BY id DESC LIMIT %s
                """,
                (limit,),
            )
            return [dict(row) for row in cur.fetchall()]

    def save_prediction_run(
        self,
        *,
        model_name: str,
        f1_score: float,
        n_rows: int,
        trained_at_model: str,
        details: list[dict] | str,
    ) -> int:
        payload = details if isinstance(details, str) else json.dumps(details, ensure_ascii=False)
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO prediction_runs
                    (created_at, model_name, f1_score, n_rows, trained_at_model, details_json)
                VALUES (%s,%s,%s,%s,%s,%s) RETURNING id
                """,
                (datetime.now().isoformat(), model_name, float(f1_score), int(n_rows), trained_at_model, payload),
            )
            return int(cur.fetchone()[0])

    def list_prediction_runs(self, limit: int = 50) -> list[dict[str, Any]]:
        with self._connect() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT id, created_at, model_name, f1_score, n_rows, trained_at_model
                FROM prediction_runs ORDER BY id DESC LIMIT %s
                """,
                (limit,),
            )
            return [dict(row) for row in cur.fetchall()]

    def save_prediction_rows(self, run_id: int, rows: list[dict[str, Any]]) -> None:
        if not rows:
            return
        now = datetime.now().isoformat()
        payload = [
            (run_id, int(r.get("row_index", 0)), str(r.get("label", "")), r.get("confidence"), now)
            for r in rows
        ]
        with self._connect() as conn, conn.cursor() as cur:
            execute_batch(
                cur,
                """
                INSERT INTO prediction_rows (run_id, row_index, label, confidence, created_at)
                VALUES (%s,%s,%s,%s,%s)
                """,
                payload,
            )

    def list_prediction_rows(self, run_id: int, limit: int = 500) -> list[dict[str, Any]]:
        with self._connect() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT id, run_id, row_index, label, confidence, created_at
                FROM prediction_rows WHERE run_id=%s ORDER BY id ASC LIMIT %s
                """,
                (run_id, limit),
            )
            return [dict(row) for row in cur.fetchall()]

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
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO audit_events
                    (created_at, username, role, action, module, result, observation, level, extra_json)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id
                """,
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
            return int(cur.fetchone()[0])

    def list_audit_events(self, limit: int = 150) -> list[dict[str, Any]]:
        with self._connect() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT id, created_at, username, role, action, module, result, observation, level, extra_json
                FROM audit_events ORDER BY id DESC LIMIT %s
                """,
                (limit,),
            )
            return [dict(row) for row in cur.fetchall()]

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

    def list_audit_log(self, limit: int = 100) -> list[tuple[Any, ...]]:
        return [
            (row["created_at"], row.get("level", "INFO"), row.get("action", ""), row.get("extra_json", "{}"))
            for row in self.list_audit_events(limit)
        ]

    def save_system_error(self, source: str, message: str, extra: dict | None = None) -> int:
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO system_errors (created_at, source, message, extra_json)
                VALUES (%s,%s,%s,%s) RETURNING id
                """,
                (datetime.now().isoformat(), source, message, json.dumps(extra or {}, ensure_ascii=False)),
            )
            return int(cur.fetchone()[0])

    def list_system_errors(self, limit: int = 50) -> list[dict[str, Any]]:
        with self._connect() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT id, created_at, source, message, extra_json FROM system_errors ORDER BY id DESC LIMIT %s",
                (limit,),
            )
            return [dict(row) for row in cur.fetchall()]

    def save_report_record(
        self,
        *,
        title: str,
        report_format: str,
        file_path: str,
        summary_json: str,
        username: str,
    ) -> int:
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO reports (created_at, title, report_format, file_path, summary_json, username)
                VALUES (%s,%s,%s,%s,%s,%s) RETURNING id
                """,
                (datetime.now().isoformat(), title, report_format, file_path, summary_json, username),
            )
            return int(cur.fetchone()[0])

    def list_reports(self, limit: int = 30) -> list[dict[str, Any]]:
        with self._connect() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT id, created_at, title, report_format, file_path, summary_json, username
                FROM reports ORDER BY id DESC LIMIT %s
                """,
                (limit,),
            )
            return [dict(row) for row in cur.fetchall()]

    def register_model_version(
        self,
        *,
        model_name: str,
        f1_score: float,
        bundle_path: str,
        version_label: str,
    ) -> int:
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute("UPDATE model_versions SET is_active=0")
            cur.execute(
                """
                INSERT INTO model_versions
                    (registered_at, model_name, f1_score, bundle_path, version_label, is_active)
                VALUES (%s,%s,%s,%s,%s,1) RETURNING id
                """,
                (datetime.now().isoformat(), model_name, float(f1_score), bundle_path, version_label),
            )
            return int(cur.fetchone()[0])

    def get_active_model_version(self) -> dict[str, Any] | None:
        with self._connect() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT id, registered_at, model_name, f1_score, bundle_path, version_label
                FROM model_versions WHERE is_active=1 ORDER BY id DESC LIMIT 1
                """
            )
            row = cur.fetchone()
            return dict(row) if row else None

    def get_dashboard_counts(self) -> dict[str, int]:
        queries = {
            "experiments": "SELECT COUNT(*) FROM experiments",
            "alerts": "SELECT COUNT(*) FROM alerts",
            "prediction_runs": "SELECT COUNT(*) FROM prediction_runs",
            "prediction_rows": "SELECT COUNT(*) FROM prediction_rows",
            "amenazas_detectadas": """
                SELECT COUNT(*) FROM prediction_rows
                WHERE label IS NOT NULL AND lower(CAST(label AS TEXT)) NOT IN ('normal','0','benign')
            """,
            "audit_events": "SELECT COUNT(*) FROM audit_events",
            "system_errors": "SELECT COUNT(*) FROM system_errors",
            "reports": "SELECT COUNT(*) FROM reports",
        }
        with self._connect() as conn, conn.cursor() as cur:
            out: dict[str, int] = {}
            for key, query in queries.items():
                cur.execute(query)
                out[key] = int(cur.fetchone()[0] or 0)
            return out

