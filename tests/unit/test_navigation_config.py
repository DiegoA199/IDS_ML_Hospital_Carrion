from src.app.components.sidebar import SIDEBAR_MODULES


def test_sidebar_exposes_real_product_functions():
    expected = {
        "Dashboard",
        "Carga de datos",
        "Preparación de datos",
        "Entrenamiento",
        "Comparación",
        "Predicción",
        "Alertas",
        "Reportes",
        "Configuración",
    }
    assert set(SIDEBAR_MODULES) == expected


def test_sidebar_keeps_internal_inputs_hidden():
    forbidden = {
        "Plan de Pruebas",
        "Estado del Arte",
        "Mockups",
        "Insumos Codex",
        "Base de datos",
        "Usuarios y roles",
        "Estado del sistema",
        "Soporte operativo",
    }
    assert forbidden.isdisjoint(SIDEBAR_MODULES)
