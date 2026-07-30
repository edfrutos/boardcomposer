"""MainWindow integration for the Compare .bcproj revisions action."""

from __future__ import annotations

from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.project_serializer import save_project
from studio.services import StudioServices


def test_diff_action_opens_dialog_with_current_project_context(
    qapp, tmp_path, monkeypatch
):
    del qapp
    path = tmp_path / "demo.bcproj"
    project = StudioProject(
        project_id="PRJ-DIFF",
        name="Demo",
        boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
        pieces=[],
        placements=[],
    )
    save_project(project, path)

    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    services.projects.open_project(project, str(path))

    window = MainWindow(services)

    captured: dict[str, object] = {}

    class _FakeDiffDialog:
        def __init__(self, parent, **kwargs):
            captured["parent"] = parent
            captured["kwargs"] = kwargs

        def exec(self):
            captured["exec_called"] = True
            return 1

    monkeypatch.setattr("studio.main_window.BcprojDiffDialog", _FakeDiffDialog)

    window._actions["diff_bcproj"].trigger()

    kwargs = captured["kwargs"]
    assert captured.get("exec_called") is True
    assert kwargs["project_path"] == str(path)
    assert kwargs["current_label"] == str(path)
    assert kwargs["language"] == "es"
    assert kwargs["start_dir"] == str(tmp_path)
    assert kwargs["current_project"]["name"] == "Demo"
