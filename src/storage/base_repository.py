"""
Interfaz común de persistencia IDS-ML (Repository Pattern).

Soporta SQLite (desarrollo / respaldo) y Firestore (producción controlada).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class IDSMLRepository(ABC):
    """Contrato unificado para experimentos, alertas, inferencias, bitácora y reportes."""

    @property
    @abstractmethod
    def backend_name(self) -> str:
        """``sqlite`` o ``firestore``."""

    # --- Alertas ---
    @abstractmethod
    def save_alert(self, alert: dict) -> str:
        """Persiste alerta enriquecida; devuelve identificador público (UUID o id lógico)."""

    @abstractmethod
    def list_alerts(self, limit: int = 200) -> list[dict[str, Any]]:
        """Lista alertas como diccionarios homogéneos para UI y reportes."""

    @abstractmethod
    def update_alert_status(self, alert_id: str, status: str, reviewer_role: str) -> bool:
        """Actualiza estado (nueva|revisada|cerrada) y rol que revisa."""

    # --- Experimentos ---
    @abstractmethod
    def save_experiment(self, model_name: str, metrics: dict) -> int:
        """Guarda métricas de un experimento; devuelve id interno."""

    @abstractmethod
    def list_experiments(self, limit: int = 200) -> list[dict[str, Any]]:
        """Historial de experimentos."""

    # --- Inferencias ---
    @abstractmethod
    def save_prediction_run(
        self,
        *,
        model_name: str,
        f1_score: float,
        n_rows: int,
        trained_at_model: str,
        details: list[dict] | str,
    ) -> int:
        """Registra un lote de inferencia; devuelve ``run_id``."""

    @abstractmethod
    def list_prediction_runs(self, limit: int = 50) -> list[dict[str, Any]]:
        """Historial de ejecuciones de inferencia."""

    @abstractmethod
    def save_prediction_rows(self, run_id: int, rows: list[dict[str, Any]]) -> None:
        """Detalle por fila (etiqueta, confianza, índice) asociado a ``run_id``."""

    @abstractmethod
    def list_prediction_rows(self, run_id: int, limit: int = 500) -> list[dict[str, Any]]:
        """Filas de predicción para un lote."""

    # --- Bitácora estructurada ---
    @abstractmethod
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
        """Evento de auditoría con usuario, módulo y resultado."""

    @abstractmethod
    def list_audit_events(self, limit: int = 150) -> list[dict[str, Any]]:
        """Bitácora estructurada reciente."""

    @abstractmethod
    def save_audit_log(self, level: str, message: str, extra: dict | None = None) -> int:
        """Compatibilidad: registra mensaje libre mapeado a bitácora estructurada."""

    @abstractmethod
    def list_audit_log(self, limit: int = 100) -> list[tuple[Any, ...]]:
        """Vista legada (fecha, nivel, mensaje, extra_json) para compatibilidad."""

    # --- Errores ---
    @abstractmethod
    def save_system_error(self, source: str, message: str, extra: dict | None = None) -> int:
        """Errores importantes (p. ej. fallo Firestore, pipeline)."""

    @abstractmethod
    def list_system_errors(self, limit: int = 50) -> list[dict[str, Any]]:
        """Últimos errores registrados."""

    # --- Reportes ---
    @abstractmethod
    def save_report_record(
        self,
        *,
        title: str,
        report_format: str,
        file_path: str,
        summary_json: str,
        username: str,
    ) -> int:
        """Metadatos de reporte generado (CSV/PDF)."""

    @abstractmethod
    def list_reports(self, limit: int = 30) -> list[dict[str, Any]]:
        """Reportes generados."""

    # --- Registro de modelo activo ---
    @abstractmethod
    def register_model_version(
        self,
        *,
        model_name: str,
        f1_score: float,
        bundle_path: str,
        version_label: str,
    ) -> int:
        """Marca una nueva versión como activa y desactiva las anteriores."""

    @abstractmethod
    def get_active_model_version(self) -> dict[str, Any] | None:
        """Metadatos del modelo activo o ``None``."""

    # --- Plan de pruebas ---
    @abstractmethod
    def save_test_case(self, test_case: dict[str, Any]) -> int:
        """Registra un caso de prueba y devuelve su identificador."""

    @abstractmethod
    def list_test_cases(self, limit: int = 1000) -> list[dict[str, Any]]:
        """Lista los casos de prueba más recientes."""

    @abstractmethod
    def update_test_case_status(
        self, code: str, status: str, obtained_result: str = "", evidence: str = ""
    ) -> bool:
        """Actualiza la ejecución de un caso identificado por su código."""

    # --- Estado del arte ---
    @abstractmethod
    def save_literature_article(self, article: dict[str, Any]) -> int:
        """Registra un artículo en la matriz académica."""

    @abstractmethod
    def list_literature_articles(self, limit: int = 1000) -> list[dict[str, Any]]:
        """Lista los artículos de la matriz académica."""

    # --- Agregados dashboard / estado ---
    @abstractmethod
    def get_dashboard_counts(self) -> dict[str, int]:
        """Conteos: experimentos, alertas, runs de predicción, filas predichas, eventos bitácora, errores, reportes."""
