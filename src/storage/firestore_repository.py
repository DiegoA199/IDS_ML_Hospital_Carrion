"""
Persistencia Firestore para IDS-ML (producción controlada / nube).
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import firebase_admin
from firebase_admin import credentials, firestore

from src.storage.base_repository import IDSMLRepository

try:
    from google.cloud.firestore import Query
except ImportError:  # pragma: no cover
    from google.cloud.firestore_v1 import Query  # type: ignore

COL_ALERTS = "idsml_alerts"
COL_EXPERIMENTS = "idsml_experiments"
COL_PREDICTIONS = "idsml_prediction_runs"
COL_PRED_ROWS = "idsml_prediction_rows"
COL_AUDIT_EVENTS = "idsml_audit_events"
COL_ERRORS = "idsml_system_errors"
COL_REPORTS = "idsml_reports"
COL_MODELS = "idsml_model_versions"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _row_id_from_uid(uid: str) -> int:
    return abs(hash(uid)) % (2**31 - 1) or 1


def _count_stream(db, col: str, cap: int = 10000) -> int:
    return sum(1 for _ in db.collection(col).limit(cap).stream())


class FirestoreRepository(IDSMLRepository):
    def __init__(self, project_id: str, credentials_path: str) -> None:
        self._project_id = project_id
        self._credentials_path = str(Path(credentials_path))
        self._db = self._init_client()

    @classmethod
    def from_settings(cls, settings: dict[str, Any]) -> FirestoreRepository:
        pid = settings.get("firebase_project_id")
        cp = settings.get("firebase_credentials_path")
        if not pid or not cp:
            raise ValueError("Firestore requiere firebase_project_id y ruta de credenciales.")
        path = Path(cp)
        if not path.is_file():
            raise FileNotFoundError(f"Credenciales Firebase no encontradas: {path}")
        return cls(str(pid), str(path))

    def _init_client(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate(self._credentials_path)
            firebase_admin.initialize_app(cred, {"projectId": self._project_id})
        return firestore.client()

    @property
    def backend_name(self) -> str:
        return "firestore"

    def save_alert(self, alert: dict) -> str:
        aid = str(alert.get("alert_uuid") or uuid.uuid4())
        doc = {
            "alert_uuid": aid,
            "created_at": _utc_now_iso(),
            "amenaza": alert.get("amenaza"),
            "tipo_amenaza": alert.get("tipo_amenaza") or alert.get("amenaza"),
            "severidad": alert.get("severidad"),
            "impacto": alert.get("impacto"),
            "accion_recomendada": alert.get("accion_recomendada"),
            "probabilidad": alert.get("probabilidad"),
            "modelo_usado": alert.get("modelo_usado"),
            "estado": alert.get("estado") or "nueva",
            "revisado_por": alert.get("revisado_por"),
            "backend": alert.get("backend") or self.backend_name,
        }
        self._db.collection(COL_ALERTS).document(aid).set(doc)
        return aid

    def list_alerts(self, limit: int = 200) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        q = self._db.collection(COL_ALERTS).order_by("created_at", direction=Query.DESCENDING).limit(limit)
        for snap in q.stream():
            d = snap.to_dict() or {}
            d["id"] = d.get("alert_uuid", snap.id)
            out.append(d)
        return out

    def update_alert_status(self, alert_id: str, status: str, reviewer_role: str) -> bool:
        ref = self._db.collection(COL_ALERTS).document(alert_id)
        doc = ref.get()
        if not doc.exists:
            return False
        ref.update({"estado": status, "revisado_por": reviewer_role})
        return True

    def save_experiment(self, model_name: str, metrics: dict) -> int:
        uid = str(uuid.uuid4())
        rid = _row_id_from_uid(uid)
        doc = {
            "id": rid,
            "created_at": _utc_now_iso(),
            "model_name": model_name,
            "accuracy": metrics.get("accuracy"),
            "precision": metrics.get("precision"),
            "recall": metrics.get("recall"),
            "f1_score": metrics.get("f1_score"),
        }
        self._db.collection(COL_EXPERIMENTS).document(uid).set(doc)
        return rid

    def list_experiments(self, limit: int = 200) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        q = self._db.collection(COL_EXPERIMENTS).order_by("created_at", direction=Query.DESCENDING).limit(limit)
        for snap in q.stream():
            d = snap.to_dict() or {}
            d["id"] = d.get("id", snap.id)
            out.append(d)
        return out

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
        uid = str(uuid.uuid4())
        row_id = _row_id_from_uid(uid)
        doc = {
            "id": row_id,
            "created_at": _utc_now_iso(),
            "model_name": model_name,
            "f1_score": float(f1_score),
            "n_rows": int(n_rows),
            "trained_at_model": trained_at_model,
            "details_json": payload,
            "doc_uid": uid,
        }
        self._db.collection(COL_PREDICTIONS).document(uid).set(doc)
        return row_id

    def list_prediction_runs(self, limit: int = 50) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        q = self._db.collection(COL_PREDICTIONS).order_by("created_at", direction=Query.DESCENDING).limit(limit)
        for snap in q.stream():
            d = snap.to_dict() or {}
            d["id"] = d.get("id", snap.id)
            out.append(d)
        return out

    def save_prediction_rows(self, run_id: int, rows: list[dict[str, Any]]) -> None:
        batch = self._db.batch()
        for r in rows:
            doc_ref = self._db.collection(COL_PRED_ROWS).document()
            batch.set(
                doc_ref,
                {
                    "run_id": run_id,
                    "row_index": int(r.get("row_index", 0)),
                    "label": str(r.get("label", "")),
                    "confidence": r.get("confidence"),
                    "created_at": _utc_now_iso(),
                },
            )
        batch.commit()

    def list_prediction_rows(self, run_id: int, limit: int = 500) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        q = self._db.collection(COL_PRED_ROWS).where("run_id", "==", run_id).limit(limit)
        for snap in q.stream():
            d = snap.to_dict() or {}
            d["id"] = snap.id
            out.append(d)
        return out

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
        uid = str(uuid.uuid4())
        rid = _row_id_from_uid(uid)
        doc = {
            "id": rid,
            "created_at": _utc_now_iso(),
            "username": username,
            "role": role,
            "action": action,
            "module": module,
            "result": result,
            "observation": observation,
            "level": level,
            "extra_json": json.dumps(extra or {}, ensure_ascii=False),
        }
        self._db.collection(COL_AUDIT_EVENTS).document(uid).set(doc)
        return rid

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
        out: list[dict[str, Any]] = []
        q = self._db.collection(COL_AUDIT_EVENTS).order_by("created_at", direction=Query.DESCENDING).limit(limit)
        for snap in q.stream():
            d = snap.to_dict() or {}
            d["id"] = d.get("id", snap.id)
            out.append(d)
        return out

    def list_audit_log(self, limit: int = 100) -> list[tuple[Any, ...]]:
        ev = self.list_audit_events(limit)
        return [(e["created_at"], e.get("level", "INFO"), e.get("action", ""), e.get("extra_json", "{}")) for e in ev]

    def save_system_error(self, source: str, message: str, extra: dict | None = None) -> int:
        uid = str(uuid.uuid4())
        rid = _row_id_from_uid(uid)
        doc = {
            "id": rid,
            "created_at": _utc_now_iso(),
            "source": source,
            "message": message,
            "extra_json": json.dumps(extra or {}, ensure_ascii=False),
        }
        self._db.collection(COL_ERRORS).document(uid).set(doc)
        return rid

    def list_system_errors(self, limit: int = 50) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        q = self._db.collection(COL_ERRORS).order_by("created_at", direction=Query.DESCENDING).limit(limit)
        for snap in q.stream():
            d = snap.to_dict() or {}
            d["id"] = d.get("id", snap.id)
            out.append(d)
        return out

    def save_report_record(
        self,
        *,
        title: str,
        report_format: str,
        file_path: str,
        summary_json: str,
        username: str,
    ) -> int:
        uid = str(uuid.uuid4())
        rid = _row_id_from_uid(uid)
        doc = {
            "id": rid,
            "created_at": _utc_now_iso(),
            "title": title,
            "report_format": report_format,
            "file_path": file_path,
            "summary_json": summary_json,
            "username": username,
        }
        self._db.collection(COL_REPORTS).document(uid).set(doc)
        return rid

    def list_reports(self, limit: int = 30) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        q = self._db.collection(COL_REPORTS).order_by("created_at", direction=Query.DESCENDING).limit(limit)
        for snap in q.stream():
            d = snap.to_dict() or {}
            d["id"] = d.get("id", snap.id)
            out.append(d)
        return out

    def register_model_version(
        self,
        *,
        model_name: str,
        f1_score: float,
        bundle_path: str,
        version_label: str,
    ) -> int:
        for snap in self._db.collection(COL_MODELS).where("is_active", "==", 1).stream():
            snap.reference.update({"is_active": 0})
        uid = str(uuid.uuid4())
        rid = _row_id_from_uid(uid)
        doc = {
            "id": rid,
            "registered_at": _utc_now_iso(),
            "model_name": model_name,
            "f1_score": float(f1_score),
            "bundle_path": bundle_path,
            "version_label": version_label,
            "is_active": 1,
        }
        self._db.collection(COL_MODELS).document(uid).set(doc)
        return rid

    def get_active_model_version(self) -> dict[str, Any] | None:
        q = self._db.collection(COL_MODELS).where("is_active", "==", 1).limit(1)
        for snap in q.stream():
            d = snap.to_dict() or {}
            d["id"] = d.get("id", snap.id)
            return d
        return None

    def get_dashboard_counts(self) -> dict[str, int]:
        db = self._db
        rows_n = _count_stream(db, COL_PRED_ROWS)
        threats = 0
        for s in db.collection(COL_PRED_ROWS).limit(5000).stream():
            d = s.to_dict() or {}
            lab = str(d.get("label", "")).lower()
            if lab and lab not in ("normal", "0", "benign"):
                threats += 1
        return {
            "experiments": _count_stream(db, COL_EXPERIMENTS),
            "alerts": _count_stream(db, COL_ALERTS),
            "prediction_runs": _count_stream(db, COL_PREDICTIONS),
            "prediction_rows": rows_n,
            "amenazas_detectadas": threats,
            "audit_events": _count_stream(db, COL_AUDIT_EVENTS),
            "system_errors": _count_stream(db, COL_ERRORS),
            "reports": _count_stream(db, COL_REPORTS),
        }
