from src.domain.services.auth_service import authenticate


def test_authenticate_valid_admin():
    user = authenticate("admin", "admin123")
    assert user is not None
    assert user.role == "Administrador TI"


def test_authenticate_invalid_password():
    assert authenticate("admin", "incorrecta") is None

