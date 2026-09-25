"""Workspace zoom resets to 100% (IDE-0056)."""

from tests.test_zoom_limit_enablement import _window


def test_zoom_100_restores_factor_and_disables_action(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.workspace.zoom_in()
    assert window.workspace.zoom != 1.0
    window._sync_zoom_actions()
    assert window._actions["zoom_100"].isEnabled()
    window._zoom_100()
    assert window.workspace.zoom == 1.0
    assert not window._actions["zoom_100"].isEnabled()
    window._zoom_100()
    assert window.workspace.zoom == 1.0
