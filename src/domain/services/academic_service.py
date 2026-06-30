"""Reglas de dominio para el plan de pruebas y la matriz de literatura."""

from __future__ import annotations

import re
from datetime import date
from typing import Any, Iterable


TEST_MODULES = (
    "Login",
    "Dashboard",
    "Carga de Dataset",
    "Preprocesamiento",
    "Entrenamiento",
    "Predicción",
    "Alertas",
    "Base de Datos",
    "Reportes",
)
TEST_TYPES = ("Funcional", "Integración", "Rendimiento", "Seguridad", "Usabilidad")
TEST_STANDARDS = ("ISO/IEC 29119", "ISO/IEC 25010", "ISO 9001", "ISO/IEC 27001")
TEST_STATUSES = ("Pendiente", "Aprobado", "Observado", "Fallido")

CONTRIBUTION_TYPES = (
    "Arquitectura",
    "Implementación",
    "Pruebas",
    "Despliegue",
    "Base de datos",
    "Calidad de software",
    "Seguridad",
    "Dashboard",
    "Machine learning",
)
RELATED_DIMENSIONS = (
    "Gestión y preparación del dataset",
    "Selección y reducción de características",
    "Entrenamiento y comparación de modelos",
    "Evaluación integral del desempeño",
    "Implementación del prototipo software",
    "Interpretabilidad, trazabilidad y utilidad institucional",
    "Calidad y pruebas de software",
    "Despliegue y persistencia en la nube",
)


EXAMPLE_TEST_CASES: tuple[dict[str, Any], ...] = (
    {"code": "CP-01", "module": "Carga de Dataset", "description": "Validar carga correcta del dataset.", "test_type": "Funcional", "standard": "ISO/IEC 29119", "input_data": "CSV válido de tráfico de red", "expected_result": "El dataset se carga y muestra su perfil.", "obtained_result": "", "status": "Pendiente", "responsible": "Analista TI", "execution_date": "2026-06-30", "evidence": "Caso base de validación."},
    {"code": "CP-02", "module": "Preprocesamiento", "description": "Validar limpieza y preprocesamiento.", "test_type": "Funcional", "standard": "ISO/IEC 25010", "input_data": "Dataset con nulos y variables categóricas", "expected_result": "Los datos quedan listos sin fuga de información.", "obtained_result": "", "status": "Pendiente", "responsible": "Analista TI", "execution_date": "2026-06-30", "evidence": "Revisar trazabilidad del pipeline."},
    {"code": "CP-03", "module": "Entrenamiento", "description": "Validar entrenamiento de Random Forest.", "test_type": "Integración", "standard": "ISO/IEC 29119", "input_data": "Particiones de entrenamiento y prueba", "expected_result": "Se generan modelo y métricas válidas.", "obtained_result": "", "status": "Pendiente", "responsible": "Analista TI", "execution_date": "2026-06-30", "evidence": "Modelo candidato."},
    {"code": "CP-04", "module": "Entrenamiento", "description": "Validar entrenamiento de SVM.", "test_type": "Rendimiento", "standard": "ISO/IEC 25010", "input_data": "Dataset preprocesado y escalado", "expected_result": "SVM finaliza y reporta métricas.", "obtained_result": "", "status": "Pendiente", "responsible": "Analista TI", "execution_date": "2026-06-30", "evidence": "Comparar tiempo de ejecución."},
    {"code": "CP-05", "module": "Entrenamiento", "description": "Validar cálculo de Accuracy, Precision, Recall y F1-score.", "test_type": "Funcional", "standard": "ISO/IEC 25010", "input_data": "Etiquetas reales y predichas", "expected_result": "Las cuatro métricas se calculan correctamente.", "obtained_result": "", "status": "Pendiente", "responsible": "Analista TI", "execution_date": "2026-06-30", "evidence": "Contrastar con scikit-learn."},
    {"code": "CP-06", "module": "Entrenamiento", "description": "Validar generación de matriz de confusión.", "test_type": "Funcional", "standard": "ISO/IEC 29119", "input_data": "Resultados de evaluación", "expected_result": "La matriz representa todas las clases.", "obtained_result": "", "status": "Pendiente", "responsible": "Analista TI", "execution_date": "2026-06-30", "evidence": "Validación visual."},
    {"code": "CP-07", "module": "Predicción", "description": "Validar predicción de nuevo tráfico.", "test_type": "Integración", "standard": "ISO/IEC 25010", "input_data": "CSV compatible con el modelo activo", "expected_result": "Cada fila obtiene etiqueta y confianza.", "obtained_result": "", "status": "Pendiente", "responsible": "Analista TI", "execution_date": "2026-06-30", "evidence": "Usar fixture de inferencia."},
    {"code": "CP-08", "module": "Alertas", "description": "Validar generación de alerta IDS-ML.", "test_type": "Seguridad", "standard": "ISO/IEC 27001", "input_data": "Predicción de tráfico malicioso", "expected_result": "Se registra alerta con severidad y recomendación.", "obtained_result": "", "status": "Pendiente", "responsible": "Administrador TI", "execution_date": "2026-06-30", "evidence": "Revisar centro de alertas."},
    {"code": "CP-09", "module": "Base de Datos", "description": "Validar almacenamiento en PostgreSQL/Neon.", "test_type": "Integración", "standard": "ISO/IEC 27001", "input_data": "Registro operativo de prueba", "expected_result": "El registro persiste y puede consultarse.", "obtained_result": "", "status": "Pendiente", "responsible": "Administrador TI", "execution_date": "2026-06-30", "evidence": "Fallback SQLite permitido."},
    {"code": "CP-10", "module": "Reportes", "description": "Validar exportación de reporte.", "test_type": "Usabilidad", "standard": "ISO 9001", "input_data": "Registros y métricas existentes", "expected_result": "Se descarga un archivo CSV legible.", "obtained_result": "", "status": "Pendiente", "responsible": "Analista TI", "execution_date": "2026-06-30", "evidence": "Abrir archivo exportado."},
)


EXAMPLE_ARTICLES: tuple[dict[str, Any], ...] = (
    {
        "article_code": "A01", "authors": "Buczak, A. L.; Guven, E.", "year": 2016,
        "title": "A Survey of Data Mining and Machine Learning Methods for Cyber Security Intrusion Detection",
        "source": "IEEE Communications Surveys & Tutorials", "contribution_type": "Machine learning",
        "problem": "Selección de métodos de ML y minería de datos para detección de intrusiones.",
        "method": "Revisión sistematizada y taxonomía de métodos.", "technologies": "Machine learning, IDS, minería de datos",
        "main_results": "Compara familias de algoritmos y sus aplicaciones en ciberseguridad.",
        "relation_with_project": "Sustenta la selección y comparación de clasificadores del IDS-ML.",
        "related_dimension": "Entrenamiento y comparación de modelos",
        "citation_format": "A. L. Buczak and E. Guven, IEEE Commun. Surveys Tuts., vol. 18, no. 2, 2016.",
        "link_or_doi": "https://doi.org/10.1109/COMST.2015.2494502", "observations": "Artículo de revisión de referencia.",
    },
    {
        "article_code": "A02", "authors": "Sommer, R.; Paxson, V.", "year": 2010,
        "title": "Outside the Closed World: On Using Machine Learning for Network Intrusion Detection",
        "source": "IEEE Symposium on Security and Privacy", "contribution_type": "Seguridad",
        "problem": "Limitaciones al trasladar modelos de ML desde laboratorio a redes reales.",
        "method": "Análisis crítico basado en experiencia operacional.", "technologies": "Network IDS, machine learning, monitoreo de red",
        "main_results": "Identifica brechas de evaluación, contexto y adaptación operacional.",
        "relation_with_project": "Justifica trazabilidad, validación contextual y supervisión humana.",
        "related_dimension": "Interpretabilidad, trazabilidad y utilidad institucional",
        "citation_format": "R. Sommer and V. Paxson, Proc. IEEE S&P, pp. 305–316, 2010.",
        "link_or_doi": "https://doi.org/10.1109/SP.2010.25", "observations": "Clave para discutir validez externa.",
    },
    {
        "article_code": "A03", "authors": "Khraisat, A.; Gondal, I.; Vamplew, P.; Kamruzzaman, J.", "year": 2019,
        "title": "Survey of Intrusion Detection Systems: Techniques, Datasets and Challenges",
        "source": "Cybersecurity", "contribution_type": "Arquitectura",
        "problem": "Cobertura fragmentada de técnicas, datasets y desafíos de los IDS.",
        "method": "Revisión comparativa de IDS y conjuntos de datos.", "technologies": "IDS, datasets, detección por anomalías, ML",
        "main_results": "Integra taxonomía de técnicas, datasets y criterios de evaluación.",
        "relation_with_project": "Sustenta arquitectura, preparación de datos y evaluación del prototipo.",
        "related_dimension": "Gestión y preparación del dataset",
        "citation_format": "A. Khraisat et al., Cybersecurity, vol. 2, art. 20, 2019.",
        "link_or_doi": "https://doi.org/10.1186/s42400-019-0038-7", "observations": "Acceso abierto.",
    },
    {
        "article_code": "A04", "authors": "Amershi, S. et al.", "year": 2019,
        "title": "Software Engineering for Machine Learning: A Case Study",
        "source": "IEEE/ACM ICSE-SEIP", "contribution_type": "Calidad de software",
        "problem": "Diferencias entre desarrollar software convencional y sistemas con ML.",
        "method": "Estudio de caso con equipos de software de Microsoft.", "technologies": "MLOps, pruebas, pipelines ML, telemetría",
        "main_results": "Describe desafíos y prácticas de ingeniería para sistemas de ML.",
        "relation_with_project": "Sustenta modularidad, pruebas, versionado y monitoreo del IDS-ML.",
        "related_dimension": "Calidad y pruebas de software",
        "citation_format": "S. Amershi et al., Proc. ICSE-SEIP, pp. 291–300, 2019.",
        "link_or_doi": "https://doi.org/10.1109/ICSE-SEIP.2019.00042", "observations": "Base para prácticas de implementación.",
    },
    {
        "article_code": "A05", "authors": "Sculley, D. et al.", "year": 2015,
        "title": "Hidden Technical Debt in Machine Learning Systems",
        "source": "Advances in Neural Information Processing Systems", "contribution_type": "Implementación",
        "problem": "Deuda técnica oculta producida por dependencias y cambios en sistemas ML.",
        "method": "Análisis de patrones de riesgo en sistemas ML de producción.", "technologies": "ML systems, pipelines, monitoreo, configuración",
        "main_results": "Expone riesgos de acoplamiento, bucles de retroalimentación y deuda de datos.",
        "relation_with_project": "Justifica persistencia desacoplada, auditoría y control de versiones.",
        "related_dimension": "Implementación del prototipo software",
        "citation_format": "D. Sculley et al., Advances in NIPS 28, 2015.",
        "link_or_doi": "https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems", "observations": "Aplicable al mantenimiento del prototipo.",
    },
)


def _clean_text(value: Any) -> str:
    return str(value or "").strip()


def validate_test_case(payload: dict[str, Any]) -> dict[str, Any]:
    """Normaliza y valida un caso de prueba antes de persistirlo."""
    data = {key: _clean_text(value) for key, value in payload.items()}
    data["code"] = data.get("code", "").upper()
    required = ("code", "module", "description", "test_type", "standard", "expected_result", "responsible")
    missing = [field for field in required if not data.get(field)]
    if missing:
        raise ValueError(f"Complete los campos obligatorios: {', '.join(missing)}.")
    if not re.fullmatch(r"CP-\d{2,3}", data["code"]):
        raise ValueError("El código debe usar el formato CP-01.")
    if data["test_type"] not in TEST_TYPES:
        raise ValueError("Tipo de prueba no válido.")
    if data["standard"] not in TEST_STANDARDS:
        raise ValueError("Norma relacionada no válida.")
    if data.get("status", "Pendiente") not in TEST_STATUSES:
        raise ValueError("Estado no válido.")
    data["status"] = data.get("status") or "Pendiente"
    execution_date = data.get("execution_date") or date.today().isoformat()
    try:
        data["execution_date"] = date.fromisoformat(execution_date).isoformat()
    except ValueError as exc:
        raise ValueError("La fecha de ejecución debe tener formato AAAA-MM-DD.") from exc
    return data


def validate_literature_article(payload: dict[str, Any]) -> dict[str, Any]:
    """Normaliza y valida una fila de la matriz académica."""
    data = {key: _clean_text(value) for key, value in payload.items()}
    data["article_code"] = data.get("article_code", "").upper()
    required = (
        "article_code", "authors", "year", "title", "source", "contribution_type",
        "problem", "method", "technologies", "main_results", "relation_with_project",
        "related_dimension", "citation_format",
    )
    missing = [field for field in required if not data.get(field)]
    if missing:
        raise ValueError(f"Complete los campos obligatorios: {', '.join(missing)}.")
    if not re.fullmatch(r"A\d{2,3}", data["article_code"]):
        raise ValueError("El código debe usar el formato A01.")
    try:
        year = int(data["year"])
    except ValueError as exc:
        raise ValueError("El año debe ser numérico.") from exc
    if not 1900 <= year <= date.today().year + 1:
        raise ValueError("El año del artículo está fuera del rango permitido.")
    if data["contribution_type"] not in CONTRIBUTION_TYPES:
        raise ValueError("Tipo de aporte no válido.")
    if data["related_dimension"] not in RELATED_DIMENSIONS:
        raise ValueError("Dimensión relacionada no válida.")
    data["year"] = year
    return data


def build_test_plan_summary(rows: Iterable[dict[str, Any]]) -> dict[str, float | int]:
    items = list(rows)
    total = len(items)
    approved = sum(row.get("status") == "Aprobado" for row in items)
    failed = sum(row.get("status") == "Fallido" for row in items)
    pending = sum(row.get("status") == "Pendiente" for row in items)
    return {
        "total": total,
        "approved": approved,
        "failed": failed,
        "pending": pending,
        "compliance": (approved / total * 100.0) if total else 0.0,
    }


def filter_test_cases(
    rows: Iterable[dict[str, Any]], *, status: str = "Todos", test_type: str = "Todos", module: str = "Todos"
) -> list[dict[str, Any]]:
    return [
        row for row in rows
        if (status == "Todos" or row.get("status") == status)
        and (test_type == "Todos" or row.get("test_type") == test_type)
        and (module == "Todos" or row.get("module") == module)
    ]


def filter_literature(
    rows: Iterable[dict[str, Any]], *, years: Iterable[int] = (), dimension: str = "Todas",
    contribution_type: str = "Todos", technology: str = "", query: str = ""
) -> list[dict[str, Any]]:
    selected_years = {int(year) for year in years}
    tech = technology.casefold().strip()
    term = query.casefold().strip()
    filtered: list[dict[str, Any]] = []
    for row in rows:
        haystack = " ".join(str(row.get(key, "")) for key in ("authors", "title", "problem", "method", "technologies", "main_results")).casefold()
        if selected_years and int(row.get("year", 0)) not in selected_years:
            continue
        if dimension != "Todas" and row.get("related_dimension") != dimension:
            continue
        if contribution_type != "Todos" and row.get("contribution_type") != contribution_type:
            continue
        if tech and tech not in str(row.get("technologies", "")).casefold():
            continue
        if term and term not in haystack:
            continue
        filtered.append(row)
    return filtered


def ensure_test_examples(repo: Any) -> None:
    """Carga los casos iniciales una sola vez en el backend activo."""
    if repo.list_test_cases(limit=1):
        return
    for example in EXAMPLE_TEST_CASES:
        repo.save_test_case(validate_test_case(dict(example)))


def ensure_literature_examples(repo: Any) -> None:
    """Carga artículos académicos iniciales una sola vez en el backend activo."""
    if repo.list_literature_articles(limit=1):
        return
    for example in EXAMPLE_ARTICLES:
        repo.save_literature_article(validate_literature_article(dict(example)))
