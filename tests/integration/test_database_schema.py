import sqlite3

from database.init_db import initialize_database


def test_database_schema_creates_sixty_two_tables_and_academic_seed(tmp_path):
    db_path = initialize_database(tmp_path / "idsml_relational.db", with_seed=True)
    with sqlite3.connect(db_path) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        ).fetchone()[0]
        roles = connection.execute("SELECT COUNT(*) FROM roles").fetchone()[0]
        test_cases = connection.execute("SELECT COUNT(*) FROM test_plan").fetchone()[0]
        articles = connection.execute("SELECT COUNT(*) FROM literature_implementation").fetchone()[0]
    assert count == 62
    assert roles >= 3
    assert test_cases == 10
    assert articles >= 5

