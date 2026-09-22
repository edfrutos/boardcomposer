"""Solve forces Workspace preview without applying (IDE-0052)."""

from boardcomposer.domain import AssemblySolution, BoardPlacement, PanelReference
from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window(tmp_path, *, placed: bool = False) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    placements = []
    if placed:
        placements.append(StudioPlacement("A", 10, 20, False, 0, "B1", 0, 0))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Preview",
            boards=[StudioBoard("B1", 1000, 500, "Roble", 19, 1)],
            pieces=[StudioPiece("A", 400, 300, "Roble", 19)],
            placements=placements,
        )
    )
    window = MainWindow(services)
    window.workspace.reload_project()
    return window


def _solved(window: MainWindow) -> AssemblySolution:
    solution = AssemblySolution(
        placements=[
            BoardPlacement(
                "A",
                80,
                40,
                400,
                300,
                panel_reference=PanelReference(0, 0),
            )
        ]
    )
    window.services.layout.solutions = [solution]
    window.services.layout.selected_solution_index = 0
    return solution


def _piece_scene_pos(window: MainWindow, piece_id: str) -> tuple[float, float]:
    item = next(
        candidate
        for candidate in window.workspace._piece_items
        if candidate.piece_id == piece_id
    )
    return item.pos().x(), item.pos().y()


def test_present_solved_layout_previews_without_applying(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, placed=False)
    assert window.workspace._piece_items == []
    solution = _solved(window)
    window._present_solved_layout(solution)
    assert window.workspace._piece_items
    assert _piece_scene_pos(window, "A") == (80, 40)
    assert window.services.projects.current_project.placements == []
    assert "Layout calculado" in window.inspector.toPlainText()


def test_present_solved_layout_moves_existing_placements(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, placed=True)
    assert _piece_scene_pos(window, "A") == (10, 20)
    window._present_solved_layout(_solved(window))
    assert _piece_scene_pos(window, "A") == (80, 40)
    applied = window.services.projects.current_project.placements
    assert applied[0].x_mm == 10
    assert applied[0].y_mm == 20


def test_solve_layout_previews_best_candidate(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path, placed=False)
    solution = _solved(window)

    def _fake_solve(**kwargs):
        del kwargs
        return solution

    monkeypatch.setattr(
        "studio.solve_worker.run_solve_with_progress",
        _fake_solve,
    )
    window._solve_layout()
    assert _piece_scene_pos(window, "A") == (80, 40)
    assert window.services.projects.current_project.placements == []
    message = window.statusBar().currentMessage()
    assert "Layout calculado" in message
