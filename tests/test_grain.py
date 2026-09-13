"""Per-piece grain lock (IDE-0021)."""

from types import SimpleNamespace

from boardcomposer import Board, Project, ProjectConstraints, StockPanel
from boardcomposer.domain import AssemblySolution, BoardPlacement
from boardcomposer.domain.grain import (
    GRAIN_LOCKED,
    GRAIN_NONE,
    grain_allows_rotation,
    normalize_grain,
    rotation_allowed,
)
from boardcomposer.solver.maxrects_generator import generate_maxrects_solution
from boardcomposer.solver.packing_runner import place_all_boards
from boardcomposer.solver.solution_validator import validate_solution
from boardcomposer.solver.validation_result import ValidationReason
from studio.commands import RotatePieceCommand
from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def test_normalize_grain_accepts_aliases():
    assert normalize_grain("locked") == GRAIN_LOCKED
    assert normalize_grain("FIXED") == GRAIN_LOCKED
    assert normalize_grain(True) == GRAIN_LOCKED
    assert normalize_grain("none") == GRAIN_NONE
    assert normalize_grain("libre") == GRAIN_NONE
    assert normalize_grain("nope") == GRAIN_NONE
    assert grain_allows_rotation("locked") is False
    assert grain_allows_rotation("none") is True


def test_rotation_allowed_needs_project_and_free_grain():
    free = Board(100, 50, 19, "A")
    locked = Board(100, 50, 19, "B", grain="locked")
    assert rotation_allowed(free, True) is True
    assert rotation_allowed(free, False) is False
    assert rotation_allowed(locked, True) is False


def test_place_all_boards_disables_rotation_for_locked_grain():
    flags: list[bool] = []

    class Recorder:
        def place(self, length_mm, width_mm, allow_rotation=False):
            flags.append(allow_rotation)
            return SimpleNamespace(
                x_mm=0,
                y_mm=0,
                length_mm=length_mm,
                width_mm=width_mm,
                rotated=False,
            )

    boards = [
        Board(100, 50, 19, "A"),
        Board(100, 50, 19, "B", grain="locked"),
    ]
    place_all_boards(Recorder(), boards, True)
    assert flags == [True, False]


def test_solver_rotates_free_grain_but_not_locked():
    project = Project(constraints=ProjectConstraints(allow_rotation=True))
    project.add_stock_panel(StockPanel(100, 250, 19, id="P1", quantity=1))
    project.add_board(Board(200, 50, 19, id="A"))
    free = generate_maxrects_solution(project)
    assert free.placements
    assert free.placements[0].rotated is True

    locked_project = Project(constraints=ProjectConstraints(allow_rotation=True))
    locked_project.add_stock_panel(StockPanel(100, 250, 19, id="P1", quantity=1))
    locked_project.add_board(Board(200, 50, 19, id="A", grain="locked"))
    locked = generate_maxrects_solution(locked_project)
    placed = locked.placements
    assert all(not item.rotated for item in placed)
    if placed:
        assert placed[0].length_mm == 200


def test_validator_rejects_rotated_locked_grain():
    project = Project(constraints=ProjectConstraints(allow_rotation=True))
    project.add_board(Board(200, 50, 19, id="A", grain="locked"))
    solution = AssemblySolution(
        placements=[BoardPlacement("A", 0, 0, 50, 200, rotated=True)]
    )
    result = validate_solution(solution, project)
    assert ValidationReason.GRAIN_VIOLATION in result.reasons
    assert result.valid is False


def test_rotate_action_disabled_when_grain_locked(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Grain",
            boards=[StudioBoard("P1", 1000, 500, "Demo", 19, 1)],
            pieces=[StudioPiece("A", 400, 300, "Demo", 19, grain="locked")],
            placements=[StudioPlacement("A", 0, 0, False, 0, "P1", 0, 0)],
        )
    )
    window = MainWindow(services)
    window._show_workspace()
    window.workspace.reload_project()
    window.workspace.select_piece("A")
    window._sync_view_actions()
    assert not window._actions["rotate_piece"].isEnabled()
    assert "veta" in window._actions["rotate_piece"].statusTip().casefold()
    window._rotate_selected_piece()
    placement = services.projects.current_project.placement_by_piece_id("A")
    assert placement is not None
    assert placement.rotated is False
    command = RotatePieceCommand(services, "A", 0, 90)
    command.execute()
    assert placement.rotated is True
