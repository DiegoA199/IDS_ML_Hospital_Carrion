from src.ui.theme import INSTITUTION_LOGO_PATH


def test_institution_logo_is_packaged_as_png():
    assert INSTITUTION_LOGO_PATH.is_file()
    assert INSTITUTION_LOGO_PATH.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
