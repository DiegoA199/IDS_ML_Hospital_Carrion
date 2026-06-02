from src.core.constants import ROLE_ADMIN, ROLE_ANALYST, ROLE_GUEST
from src.security import rbac


def test_dataset_access_all_demo_roles():
    assert rbac.can_access_dataset(ROLE_ADMIN)
    assert rbac.can_access_dataset(ROLE_ANALYST)
    assert rbac.can_access_dataset(ROLE_GUEST)


def test_training_and_inference_restricted_to_ti_roles():
    assert rbac.can_train(ROLE_ADMIN)
    assert rbac.can_train(ROLE_ANALYST)
    assert not rbac.can_train(ROLE_GUEST)
    assert rbac.can_infer(ROLE_ANALYST)
    assert not rbac.can_infer(ROLE_GUEST)


def test_alert_status_only_admin():
    assert rbac.can_manage_alerts(ROLE_ANALYST)
    assert rbac.can_change_alert_status(ROLE_ADMIN)
    assert not rbac.can_change_alert_status(ROLE_ANALYST)
    assert not rbac.can_manual_alert_demo(ROLE_GUEST)


def test_reports_and_system_status_for_ti_roles():
    assert rbac.can_reports(ROLE_ADMIN)
    assert rbac.can_system_status(ROLE_ANALYST)
    assert not rbac.can_reports(ROLE_GUEST)
    assert not rbac.can_system_status(ROLE_GUEST)
