from src.services.dashboard_service import build_dashboard_context


EXPECTED_BEST_F1 = 0.91


class DashboardRepo:
    def get_dashboard_counts(self):
        return {"alerts": 2, "experiments": 2, "prediction_runs": 1}

    def list_experiments(self, limit=50):
        return [
            {"model_name": "Decision Tree", "f1_score": 0.72},
            {"model_name": "Random Forest", "f1_score": EXPECTED_BEST_F1},
        ]

    def list_alerts(self, limit=200):
        return [
            {"severidad": "Alta", "tipo_amenaza": "DDoS"},
            {"severidad": "Media", "tipo_amenaza": "Probe"},
        ]

    def get_active_model_version(self):
        return {"model_name": "Random Forest", "f1_score": EXPECTED_BEST_F1}

    def list_audit_events(self, limit=20):
        return [{"action": "inicio_sesion"}]

    def list_prediction_runs(self, limit=1):
        return [{"created_at": "2026-06-02T10:00:00"}]


def test_build_dashboard_context_summarizes_repository_data():
    context = build_dashboard_context(DashboardRepo())

    assert context["counts"]["alerts"] == 2
    assert context["severity_distribution"]["Alta"] == 1
    assert context["threat_type_distribution"]["DDoS"] == 1
    assert context["best_name_session"] == "Random Forest"
    assert abs(context["best_f1_session"] - EXPECTED_BEST_F1) < 0.0001
    assert context["last_prediction_at"] == "2026-06-02T10:00:00"
