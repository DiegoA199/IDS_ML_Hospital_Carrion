"""Helpers para inspeccionar el modelo relacional documentado del IDS-ML."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SQLITE_SCHEMA_PATH = PROJECT_ROOT / "database" / "schema.sql"
POSTGRES_SCHEMA_PATH = PROJECT_ROOT / "database" / "postgresql" / "schema.sql"
DBML_PATH = PROJECT_ROOT / "docs" / "base_datos" / "modelo_er_ids_ml.dbml"

TABLE_MODULES: dict[str, str] = {
    "usuarios": "Seguridad y usuarios",
    "roles": "Seguridad y usuarios",
    "permisos": "Seguridad y usuarios",
    "usuarios_roles": "Seguridad y usuarios",
    "roles_permisos": "Seguridad y usuarios",
    "sesiones_usuario": "Seguridad y usuarios",
    "bitacora_accesos": "Seguridad y usuarios",
    "auditoria_sistema": "Seguridad y usuarios",
    "instituciones": "Institucion hospitalaria",
    "sedes": "Institucion hospitalaria",
    "areas_hospitalarias": "Areas y responsables TI",
    "responsables_ti": "Areas y responsables TI",
    "cargos": "Areas y responsables TI",
    "activos_red": "Activos de red",
    "tipos_activo": "Activos de red",
    "dispositivos_red": "Activos de red",
    "segmentos_red": "Segmentos, IP, protocolos y servicios",
    "direcciones_ip": "Segmentos, IP, protocolos y servicios",
    "protocolos_red": "Segmentos, IP, protocolos y servicios",
    "servicios_red": "Segmentos, IP, protocolos y servicios",
    "datasets": "Datasets",
    "versiones_dataset": "Datasets",
    "columnas_dataset": "Datasets",
    "perfilado_dataset": "Perfilado y calidad de datos",
    "calidad_dataset": "Perfilado y calidad de datos",
    "clases_trafico": "Datasets",
    "particiones_dataset": "Datasets",
    "preprocesamientos": "Preprocesamiento",
    "pasos_preprocesamiento": "Preprocesamiento",
    "transformaciones_datos": "Preprocesamiento",
    "seleccion_caracteristicas": "Preprocesamiento",
    "modelos_ml": "Modelos de machine learning",
    "tipos_modelo_ml": "Modelos de machine learning",
    "parametros_modelo": "Modelos de machine learning",
    "entrenamientos": "Entrenamientos",
    "metricas_entrenamiento": "Metricas y comparacion",
    "comparaciones_modelo": "Metricas y comparacion",
    "modelos_seleccionados": "Metricas y comparacion",
    "predicciones": "Predicciones",
    "eventos_red": "Eventos de red",
    "flujos_trafico": "Eventos de red",
    "tipos_amenaza": "Amenazas detectadas",
    "amenazas_detectadas": "Amenazas detectadas",
    "niveles_severidad": "Alertas IDS",
    "alertas": "Alertas IDS",
    "estados_alerta": "Alertas IDS",
    "evidencias_alerta": "Alertas IDS",
    "acciones_recomendadas": "Alertas IDS",
    "incidentes_seguridad": "Incidentes de seguridad",
    "atencion_incidente": "Atencion y escalamiento",
    "escalamiento_incidente": "Atencion y escalamiento",
    "historial_alerta": "Alertas IDS",
    "reportes": "Reportes",
    "tipos_reporte": "Reportes",
    "reportes_generados": "Reportes",
    "exportaciones_reporte": "Reportes",
    "configuracion_sistema": "Mejora continua",
    "umbrales_alerta": "Mejora continua",
    "normas_referencia": "Normas ISO/NIST y controles",
    "controles_cumplimiento": "Normas ISO/NIST y controles",
}


@dataclass(frozen=True)
class ForeignKeyInfo:
    source_table: str
    source_column: str
    target_table: str
    target_column: str


@dataclass(frozen=True)
class TableInfo:
    name: str
    module: str
    columns: tuple[str, ...]
    foreign_keys: tuple[ForeignKeyInfo, ...]


def read_schema(path: Path = SQLITE_SCHEMA_PATH) -> str:
    """Return the SQL schema used for documentation and local initialization."""

    return path.read_text(encoding="utf-8")


def parse_tables(sql_text: str) -> list[TableInfo]:
    """Parse CREATE TABLE blocks from the IDS-ML SQL schema."""

    pattern = re.compile(
        r"CREATE\s+TABLE\s+IF\s+NOT\s+EXISTS\s+([a-zA-Z_][\w]*)\s*\((.*?)\);",
        re.IGNORECASE | re.DOTALL,
    )
    tables: list[TableInfo] = []
    for match in pattern.finditer(sql_text):
        table_name = match.group(1)
        body = match.group(2)
        columns = _parse_columns(body)
        foreign_keys = _parse_foreign_keys(table_name, body)
        tables.append(
            TableInfo(
                name=table_name,
                module=TABLE_MODULES.get(table_name, "Sin modulo asignado"),
                columns=tuple(columns),
                foreign_keys=tuple(foreign_keys),
            )
        )
    return tables


def summarize_tables(tables: list[TableInfo]) -> pd.DataFrame:
    """Build a UI-friendly table summary grouped by functional module."""

    rows = [
        {
            "modulo": table.module,
            "tabla": table.name,
            "columnas": len(table.columns),
            "relaciones_fk": len(table.foreign_keys),
        }
        for table in tables
    ]
    return pd.DataFrame(rows).sort_values(["modulo", "tabla"]).reset_index(drop=True)


def summarize_modules(tables: list[TableInfo]) -> pd.DataFrame:
    """Aggregate table and relationship counts by module."""

    summary = summarize_tables(tables)
    if summary.empty:
        return summary
    return (
        summary.groupby("modulo", as_index=False)
        .agg(tablas=("tabla", "count"), columnas=("columnas", "sum"), relaciones_fk=("relaciones_fk", "sum"))
        .sort_values("modulo")
        .reset_index(drop=True)
    )


def build_relationship_dot(tables: list[TableInfo], module: str | None = None) -> str:
    """Return a Graphviz DOT diagram for the selected module and direct relations."""

    selected_names = {table.name for table in tables if module in (None, "Todos", table.module)}
    if module not in (None, "Todos"):
        selected_names.update(
            fk.target_table
            for table in tables
            if table.name in selected_names
            for fk in table.foreign_keys
        )

    nodes = [table for table in tables if table.name in selected_names]
    edges = [
        fk
        for table in nodes
        for fk in table.foreign_keys
        if fk.source_table in selected_names and fk.target_table in selected_names
    ]

    lines = [
        "digraph idsml_db {",
        "  graph [rankdir=LR, bgcolor=\"transparent\", pad=0.2, nodesep=0.45, ranksep=0.7];",
        "  node [shape=box, style=\"rounded,filled\", color=\"#1d4ed8\", fillcolor=\"#eff6ff\", fontname=\"Inter\", fontsize=10];",
        "  edge [color=\"#64748b\", arrowsize=0.7, fontname=\"Inter\", fontsize=8];",
    ]
    for table in nodes:
        label = f"{table.name}\\n{len(table.columns)} campos"
        lines.append(f'  "{table.name}" [label="{label}"];')
    for fk in edges:
        label = f"{fk.source_column} -> {fk.target_column}"
        lines.append(f'  "{fk.source_table}" -> "{fk.target_table}" [label="{label}"];')
    lines.append("}")
    return "\n".join(lines)


def _parse_columns(body: str) -> list[str]:
    columns: list[str] = []
    for raw_line in body.splitlines():
        line = raw_line.strip().rstrip(",")
        upper_line = line.upper()
        if not line or upper_line.startswith(("FOREIGN KEY", "UNIQUE", "CHECK", "PRIMARY KEY", "CONSTRAINT")):
            continue
        column_name = line.split()[0].strip('"')
        if column_name:
            columns.append(column_name)
    return columns


def _parse_foreign_keys(table_name: str, body: str) -> list[ForeignKeyInfo]:
    fk_pattern = re.compile(
        r"FOREIGN\s+KEY\s*\(([^)]+)\)\s+REFERENCES\s+([a-zA-Z_][\w]*)\s*\(([^)]+)\)",
        re.IGNORECASE,
    )
    return [
        ForeignKeyInfo(
            source_table=table_name,
            source_column=match.group(1).strip().strip('"'),
            target_table=match.group(2).strip(),
            target_column=match.group(3).strip().strip('"'),
        )
        for match in fk_pattern.finditer(body)
    ]
