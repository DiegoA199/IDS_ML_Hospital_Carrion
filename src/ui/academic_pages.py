"""Páginas Streamlit para calidad de software y estado del arte."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Any

import pandas as pd
import plotly.express as px
import streamlit as st

from src.audit.service import log_action
from src.domain.services.academic_service import (
    CONTRIBUTION_TYPES,
    RELATED_DIMENSIONS,
    TEST_MODULES,
    TEST_STANDARDS,
    TEST_STATUSES,
    TEST_TYPES,
    ensure_literature_examples,
    ensure_test_examples,
    filter_literature,
    filter_test_cases,
    build_test_plan_summary,
    validate_literature_article,
    validate_test_case,
)
from src.ui.theme import (
    PALETTE,
    empty_state,
    format_int,
    metric_card,
    page_header,
    section_title,
    themed_plotly,
)

if TYPE_CHECKING:
    from src.storage.base_repository import IDSMLRepository


def _csv_bytes(rows: list[dict[str, Any]]) -> bytes:
    """Genera CSV compatible con Excel conservando caracteres en español."""
    return pd.DataFrame(rows).to_csv(index=False).encode("utf-8-sig")


def _show_flash() -> None:
    message = st.session_state.pop("academic_flash", None)
    if message:
        st.success(str(message))


def _register_test_case(repo: "IDSMLRepository") -> None:
    section_title("Registrar caso de prueba", "Los campos con asterisco son obligatorios; el código debe ser único.")
    with st.form("test_case_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            code = st.text_input("Código *", placeholder="CP-11")
            module = st.selectbox("Módulo evaluado *", TEST_MODULES)
            test_type = st.selectbox("Tipo de prueba *", TEST_TYPES)
        with col2:
            standard = st.selectbox("Norma relacionada *", TEST_STANDARDS)
            status = st.selectbox("Estado *", TEST_STATUSES)
            responsible = st.text_input("Responsable *", value=st.session_state.get("username", "Analista TI"))
        with col3:
            execution_date = st.date_input("Fecha de ejecución *", value=date.today())
            input_data = st.text_area("Datos de entrada", height=106)

        description = st.text_area("Descripción del caso *")
        expected_result = st.text_area("Resultado esperado *")
        obtained_result = st.text_area("Resultado obtenido")
        evidence = st.text_area("Evidencia o comentario")
        submitted = st.form_submit_button("Registrar caso", type="primary")

    if not submitted:
        return
    try:
        payload = validate_test_case(
            {
                "code": code,
                "module": module,
                "description": description,
                "test_type": test_type,
                "standard": standard,
                "input_data": input_data,
                "expected_result": expected_result,
                "obtained_result": obtained_result,
                "status": status,
                "responsible": responsible,
                "execution_date": execution_date.isoformat(),
                "evidence": evidence,
            }
        )
        repo.save_test_case(payload)
        log_action(repo, action="registro_caso_prueba", module="plan_pruebas", result="ok", observation=payload["code"])
        st.session_state["academic_flash"] = f"Caso {payload['code']} registrado correctamente."
        st.rerun()
    except ValueError as exc:
        st.error(str(exc))
    except Exception as exc:
        st.error(f"No se pudo registrar el caso. Verifique que el código no esté duplicado. Detalle: {exc}")


def _update_test_case(repo: "IDSMLRepository", rows: list[dict[str, Any]]) -> None:
    section_title("Actualizar ejecución", "Registre el estado, resultado real y evidencia del caso seleccionado.")
    if not rows:
        empty_state("No hay casos disponibles para actualizar.")
        return

    by_code = {str(row["code"]): row for row in rows}
    with st.form("test_status_form"):
        code = st.selectbox(
            "Caso de prueba",
            list(by_code),
            format_func=lambda value: f"{value} · {by_code[value]['description']}",
        )
        current = by_code[code]
        current_status = str(current.get("status", "Pendiente"))
        status_index = TEST_STATUSES.index(current_status) if current_status in TEST_STATUSES else 0
        status = st.selectbox("Nuevo estado", TEST_STATUSES, index=status_index)
        obtained_result = st.text_area("Resultado obtenido", value=str(current.get("obtained_result") or ""))
        evidence = st.text_area("Evidencia o comentario", value=str(current.get("evidence") or ""))
        submitted = st.form_submit_button("Guardar actualización", type="primary")

    if not submitted:
        return
    if repo.update_test_case_status(code, status, obtained_result.strip(), evidence.strip()):
        log_action(repo, action="actualizacion_caso_prueba", module="plan_pruebas", result="ok", observation=f"{code}: {status}")
        st.session_state["academic_flash"] = f"Caso {code} actualizado a {status}."
        st.rerun()
    else:
        st.error("El caso seleccionado ya no existe o no pudo actualizarse.")


def render_test_plan(repo: "IDSMLRepository") -> None:
    page_header(
        "Plan de Pruebas",
        "Gestión verificable de casos funcionales, de integración, rendimiento, seguridad y usabilidad.",
        tag=f"Persistencia: {repo.backend_name}",
    )
    _show_flash()
    try:
        ensure_test_examples(repo)
        rows = repo.list_test_cases(limit=1000)
    except Exception as exc:
        st.error(f"No fue posible cargar el plan de pruebas: {exc}")
        return

    summary = build_test_plan_summary(rows)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        metric_card("Total", format_int(summary["total"]), "Casos registrados", tone="blue")
    with c2:
        metric_card("Aprobados", format_int(summary["approved"]), "Ejecución conforme", tone="green")
    with c3:
        metric_card("Fallidos", format_int(summary["failed"]), "Requieren corrección", tone="red")
    with c4:
        metric_card("Pendientes", format_int(summary["pending"]), "Por ejecutar", tone="amber")
    with c5:
        metric_card(
            "Cumplimiento",
            f"{float(summary['compliance']):.1f}%",
            "Aprobados / total",
            tone="green",
            progress=float(summary["compliance"]),
        )

    list_tab, register_tab, update_tab = st.tabs(["Matriz y filtros", "Registrar caso", "Actualizar estado"])
    with list_tab:
        section_title("Filtros del plan", "Combine estado, tipo y módulo para preparar una revisión o exportación.")
        f1, f2, f3 = st.columns(3)
        with f1:
            selected_status = st.selectbox("Estado", ("Todos",) + TEST_STATUSES, key="test_filter_status")
        with f2:
            selected_type = st.selectbox("Tipo", ("Todos",) + TEST_TYPES, key="test_filter_type")
        with f3:
            available_modules = tuple(sorted({str(row.get("module", "")) for row in rows if row.get("module")}))
            selected_module = st.selectbox("Módulo", ("Todos",) + available_modules, key="test_filter_module")

        filtered = filter_test_cases(rows, status=selected_status, test_type=selected_type, module=selected_module)
        section_title("Casos de prueba", f"{len(filtered)} de {len(rows)} casos visibles.")
        if filtered:
            display_columns = [
                "code", "module", "description", "test_type", "standard", "input_data",
                "expected_result", "obtained_result", "status", "responsible", "execution_date", "evidence",
            ]
            st.dataframe(pd.DataFrame(filtered)[display_columns], width="stretch", hide_index=True)
        else:
            empty_state("No hay casos que coincidan con los filtros actuales.")
        st.download_button(
            "Exportar plan filtrado a CSV",
            data=_csv_bytes(filtered),
            file_name="plan_pruebas_ids_ml.csv",
            mime="text/csv",
            disabled=not filtered,
        )

    with register_tab:
        _register_test_case(repo)
    with update_tab:
        _update_test_case(repo, rows)


def _register_article(repo: "IDSMLRepository") -> None:
    section_title("Registrar artículo", "Cada fila debe explicar tanto el aporte científico como su uso concreto en IDS-ML.")
    with st.form("literature_form", clear_on_submit=True):
        c1, c2, c3 = st.columns([0.65, 1.55, 0.7])
        with c1:
            article_code = st.text_input("Código *", placeholder="A06")
        with c2:
            authors = st.text_input("Autor o autores *")
        with c3:
            year = st.number_input("Año *", min_value=1900, max_value=date.today().year + 1, value=date.today().year, step=1)
        title = st.text_input("Título del artículo *")
        c4, c5 = st.columns(2)
        with c4:
            source = st.text_input("Fuente o revista *")
            contribution_type = st.selectbox("Tipo de aporte *", CONTRIBUTION_TYPES)
        with c5:
            related_dimension = st.selectbox("Dimensión relacionada *", RELATED_DIMENSIONS)
            technologies = st.text_input("Tecnologías usadas *", placeholder="Python, Streamlit, PostgreSQL, ML")
        problem = st.text_area("Problema abordado *")
        method = st.text_area("Método usado *")
        main_results = st.text_area("Resultados principales *")
        relation = st.text_area("Relación con el proyecto IDS-ML *")
        citation = st.text_area("Cita en formato ISO 690 o IEEE *")
        link = st.text_input("Enlace o DOI")
        observations = st.text_area("Observaciones")
        submitted = st.form_submit_button("Registrar artículo", type="primary")

    if not submitted:
        return
    try:
        payload = validate_literature_article(
            {
                "article_code": article_code,
                "authors": authors,
                "year": year,
                "title": title,
                "source": source,
                "contribution_type": contribution_type,
                "problem": problem,
                "method": method,
                "technologies": technologies,
                "main_results": main_results,
                "relation_with_project": relation,
                "related_dimension": related_dimension,
                "citation_format": citation,
                "link_or_doi": link,
                "observations": observations,
            }
        )
        repo.save_literature_article(payload)
        log_action(repo, action="registro_articulo", module="estado_arte", result="ok", observation=payload["article_code"])
        st.session_state["academic_flash"] = f"Artículo {payload['article_code']} agregado a la matriz."
        st.rerun()
    except ValueError as exc:
        st.error(str(exc))
    except Exception as exc:
        st.error(f"No se pudo registrar el artículo. Verifique que el código no esté duplicado. Detalle: {exc}")


def _support_matrix(rows: list[dict[str, Any]]) -> pd.DataFrame:
    matrix: list[dict[str, Any]] = []
    for dimension in RELATED_DIMENSIONS:
        selected = [row for row in rows if row.get("related_dimension") == dimension]
        if not selected:
            continue
        matrix.append(
            {
                "dimensión": dimension,
                "artículos": ", ".join(str(row.get("article_code")) for row in selected),
                "tipos de aporte": ", ".join(sorted({str(row.get("contribution_type")) for row in selected})),
                "sustento para IDS-ML": " | ".join(str(row.get("relation_with_project")) for row in selected),
            }
        )
    return pd.DataFrame(matrix)


def render_literature_implementation(repo: "IDSMLRepository") -> None:
    page_header(
        "Estado del Arte - Implementación de Software",
        "Matriz académica que conecta evidencia científica con decisiones de arquitectura, calidad, seguridad y despliegue.",
        tag=f"Persistencia: {repo.backend_name}",
    )
    _show_flash()
    try:
        ensure_literature_examples(repo)
        rows = repo.list_literature_articles(limit=1000)
    except Exception as exc:
        st.error(f"No fue posible cargar la matriz del estado del arte: {exc}")
        return

    years = sorted({int(row["year"]) for row in rows if row.get("year")}, reverse=True)
    dimensions_covered = len({row.get("related_dimension") for row in rows if row.get("related_dimension")})
    contribution_count = len({row.get("contribution_type") for row in rows if row.get("contribution_type")})
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Artículos", format_int(len(rows)), "Matriz académica", tone="blue")
    with c2:
        metric_card("Dimensiones", format_int(dimensions_covered), f"de {len(RELATED_DIMENSIONS)} cubiertas", tone="green")
    with c3:
        metric_card("Tipos de aporte", format_int(contribution_count), "Perspectivas técnicas", tone="amber")
    with c4:
        period = f"{min(years)}–{max(years)}" if years else "Sin datos"
        metric_card("Periodo", period, "Cobertura temporal", tone="slate")

    matrix_tab, charts_tab, register_tab = st.tabs(["Matriz académica", "Resumen y gráficos", "Registrar artículo"])
    with matrix_tab:
        section_title("Búsqueda y filtros", "Busque por autor, título o palabra clave y combine criterios académicos.")
        query = st.text_input("Buscar", placeholder="autor, título, método o palabra clave", key="literature_query")
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            selected_years = st.multiselect("Año", years, key="literature_years")
        with f2:
            dimension = st.selectbox("Dimensión", ("Todas",) + RELATED_DIMENSIONS, key="literature_dimension")
        with f3:
            contribution = st.selectbox("Tipo de aporte", ("Todos",) + CONTRIBUTION_TYPES, key="literature_contribution")
        with f4:
            technology = st.text_input("Tecnología", placeholder="Streamlit, ML, cloud...", key="literature_technology")

        filtered = filter_literature(
            rows,
            years=selected_years,
            dimension=dimension,
            contribution_type=contribution,
            technology=technology,
            query=query,
        )
        section_title("Matriz de artículos", f"{len(filtered)} de {len(rows)} artículos visibles.")
        if filtered:
            matrix_columns = [
                "article_code", "authors", "year", "title", "source", "contribution_type",
                "problem", "method", "technologies", "main_results", "relation_with_project",
                "related_dimension", "citation_format", "link_or_doi", "observations",
            ]
            st.dataframe(pd.DataFrame(filtered)[matrix_columns], width="stretch", hide_index=True)
            section_title("Trazabilidad del sustento", "Qué evidencia respalda cada dimensión de implementación del prototipo.")
            st.dataframe(_support_matrix(filtered), width="stretch", hide_index=True)
        else:
            empty_state("No hay artículos que coincidan con la búsqueda y los filtros.")
        st.download_button(
            "Exportar matriz filtrada a CSV",
            data=_csv_bytes(filtered),
            file_name="estado_arte_implementacion_ids_ml.csv",
            mime="text/csv",
            disabled=not filtered,
        )

    with charts_tab:
        section_title("Cobertura por dimensión", "Cantidad de artículos que sustentan cada eje del proyecto.")
        if rows:
            df = pd.DataFrame(rows)
            dimension_df = df.groupby("related_dimension", as_index=False).size().rename(columns={"size": "artículos"})
            st.dataframe(dimension_df.sort_values("artículos", ascending=False), width="stretch", hide_index=True)
            left, right = st.columns(2)
            with left:
                year_df = df.groupby("year", as_index=False).size().rename(columns={"size": "artículos"}).sort_values("year")
                fig = px.bar(year_df, x="year", y="artículos", title="Artículos por año", color_discrete_sequence=[PALETTE["blue"]])
                st.plotly_chart(themed_plotly(fig, height=360), width="stretch")
            with right:
                type_df = df.groupby("contribution_type", as_index=False).size().rename(columns={"size": "artículos"})
                fig = px.bar(
                    type_df.sort_values("artículos"), x="artículos", y="contribution_type", orientation="h",
                    title="Artículos por tipo de aporte", color_discrete_sequence=[PALETTE["green"]],
                )
                st.plotly_chart(themed_plotly(fig, height=360), width="stretch")
        else:
            empty_state("Registre artículos para generar los resúmenes visuales.")

    with register_tab:
        _register_article(repo)
