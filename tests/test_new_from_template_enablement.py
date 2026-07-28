"""Gate Nuevo desde plantilla when no project templates exist."""

from __future__ import annotations

import pytest

from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.project_templates import ProjectTemplatesManager
from studio.services import StudioServices

pytestmark = pytest.mark.usefixtures("qapp")


def _window(tmp_path) -> MainWindow:
    templates = ProjectTemplatesManager(
        directory=tmp_path / "templates", autoload=False
    )
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json"),
        project_templates=templates,
    )
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)
    window._sync_template_actions()
    return window


def test_new_from_template_disabled_when_empty(tmp_path):
    window = _window(tmp_path)
    action = window._actions["new_from_template"]
    assert not action.isEnabled()
    assert action.statusTip() == window._tr("status.template_empty")
    assert not window.welcome.template_button.isEnabled()
    assert window.welcome.template_button.statusTip() == window._tr(
        "status.template_empty"
    )


def test_new_from_template_enabled_after_save(tmp_path):
    window = _window(tmp_path)
    services = window.services
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Plantilla",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
            pieces=[StudioPiece("A", 200, 100, "Demo", 19)],
        )
    )
    services.project_templates.save_from_project(
        "Plantilla",
        services.projects.current_project,
    )
    window._sync_template_actions()

    action = window._actions["new_from_template"]
    assert action.isEnabled()
    tip = action.statusTip()
    assert tip != window._tr("status.template_empty")
    assert "Ctrl+Shift+N" in tip or "⇧⌘N" in tip
    assert window.welcome.template_button.isEnabled()
