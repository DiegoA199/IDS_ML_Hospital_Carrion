from src.domain.services.academic_service import validate_literature_article, validate_test_case
from src.storage.sqlite_repository import SQLiteRepository


def test_sqlite_academic_modules_roundtrip(tmp_path):
    repo = SQLiteRepository(tmp_path / "academic.db")
    test_id = repo.save_test_case(
        validate_test_case(
            {
                "code": "CP-11",
                "module": "Dashboard",
                "description": "Validar dashboard",
                "test_type": "Funcional",
                "standard": "ISO/IEC 29119",
                "expected_result": "Dashboard disponible",
                "status": "Pendiente",
                "responsible": "QA",
                "execution_date": "2026-06-30",
            }
        )
    )
    assert test_id > 0
    assert repo.update_test_case_status("CP-11", "Aprobado", "Correcto", "captura.png")
    assert repo.list_test_cases()[0]["status"] == "Aprobado"

    article_id = repo.save_literature_article(
        validate_literature_article(
            {
                "article_code": "A06",
                "authors": "Autor",
                "year": 2024,
                "title": "Ingeniería de IDS",
                "source": "Revista",
                "contribution_type": "Implementación",
                "problem": "Arquitectura",
                "method": "Estudio de caso",
                "technologies": "Python, Streamlit",
                "main_results": "Prototipo validado",
                "relation_with_project": "Sustenta la implementación",
                "related_dimension": "Implementación del prototipo software",
                "citation_format": "A. Autor, Revista, 2024.",
            }
        )
    )
    assert article_id > 0
    assert repo.list_literature_articles()[0]["article_code"] == "A06"
