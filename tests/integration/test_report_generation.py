from src.reports import generator
from src.storage.sqlite_repository import SQLiteRepository


def test_report_summary_without_experiments(tmp_path):
    repo = SQLiteRepository(tmp_path / "idsml_empty.db")
    df = generator.build_summary_dataframe(repo)
    assert df.iloc[0]["mensaje"] == "Sin experimentos registrados"


def test_report_csv_generation(tmp_path, monkeypatch):
    repo = SQLiteRepository(tmp_path / "idsml.db")
    repo.save_experiment("Random Forest", {"accuracy": 1.0, "precision": 1.0, "recall": 1.0, "f1_score": 1.0})
    monkeypatch.setattr(generator, "REPORTS_DIR", tmp_path)
    path = generator.export_summary_csv(repo, "tester")
    assert path.exists()
    assert repo.list_reports(limit=1)[0]["report_format"] == "csv"


def test_report_pdf_generation(tmp_path, monkeypatch):
    repo = SQLiteRepository(tmp_path / "idsml_pdf.db")
    repo.save_experiment("Random Forest", {"accuracy": 1.0, "precision": 1.0, "recall": 1.0, "f1_score": 1.0})
    monkeypatch.setattr(generator, "REPORTS_DIR", tmp_path)

    path = generator.export_summary_pdf(repo, "tester")

    assert path is not None
    assert path.exists()
    assert repo.list_reports(limit=1)[0]["report_format"] == "pdf"
