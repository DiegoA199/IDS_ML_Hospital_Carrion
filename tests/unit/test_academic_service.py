import pytest

from src.domain.services.academic_service import (
    filter_literature,
    filter_test_cases,
    build_test_plan_summary,
    validate_literature_article,
    validate_test_case,
)


def test_validate_test_case_and_summary():
    case = validate_test_case(
        {
            "code": " cp-11 ",
            "module": "Dashboard",
            "description": "Validar indicadores",
            "test_type": "Funcional",
            "standard": "ISO/IEC 29119",
            "expected_result": "Indicadores visibles",
            "status": "Aprobado",
            "responsible": "QA",
            "execution_date": "2026-06-30",
        }
    )
    assert case["code"] == "CP-11"
    assert filter_test_cases([case], status="Aprobado") == [case]
    assert build_test_plan_summary([case]) == {
        "total": 1,
        "approved": 1,
        "failed": 0,
        "pending": 0,
        "compliance": 100.0,
    }


def test_validate_test_case_rejects_bad_code():
    with pytest.raises(ValueError, match="CP-01"):
        validate_test_case(
            {
                "code": "11",
                "module": "Dashboard",
                "description": "Prueba",
                "test_type": "Funcional",
                "standard": "ISO/IEC 29119",
                "expected_result": "Correcto",
                "responsible": "QA",
            }
        )


def test_validate_and_filter_literature():
    article = validate_literature_article(
        {
            "article_code": "a06",
            "authors": "Autor",
            "year": "2024",
            "title": "Despliegue seguro con Python",
            "source": "Revista",
            "contribution_type": "Despliegue",
            "problem": "Persistencia",
            "method": "Estudio de caso",
            "technologies": "Python, PostgreSQL, cloud",
            "main_results": "Arquitectura reproducible",
            "relation_with_project": "Sustenta el despliegue IDS-ML",
            "related_dimension": "Despliegue y persistencia en la nube",
            "citation_format": "A. Autor, Revista, 2024.",
        }
    )
    assert article["article_code"] == "A06"
    assert article["year"] == 2024
    assert filter_literature([article], technology="postgres", query="seguro") == [article]
    assert filter_literature([article], years=[2023]) == []
