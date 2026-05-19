from src.domain.services.report_service import build_operational_summary


class FakeRepo:
    def get_dashboard_counts(self):
        return {"alerts": 2, "experiments": 1}


def test_build_operational_summary_uses_repository_counts():
    assert build_operational_summary(FakeRepo())["alerts"] == 2

