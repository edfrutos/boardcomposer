"""Enable/disable apply/export/prev-next based on solution availability."""

from boardcomposer.domain import AssemblySolution, BoardPlacement

from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es", max_solutions=20))
    return MainWindow(services)


def _sol() -> AssemblySolution:
    return AssemblySolution(placements=[BoardPlacement("A", 0, 0, 10, 10)])


def test_solution_actions_disabled_without_solutions(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.layout.solutions = []
    window._reload_solution_table()

    assert not window._actions["apply_layout"].isEnabled()
    assert not window._actions["export_selected"].isEnabled()
    assert not window._actions["export_cut_list"].isEnabled()
    assert not window._actions["previous_solution"].isEnabled()
    assert not window._actions["next_solution"].isEnabled()
    assert not window._actions["repack_omitted"].isEnabled()
    assert not window._actions["promote_offcuts"].isEnabled()
    assert not window.pin_reference_button.isEnabled()
    assert not window.comparator_sort.isEnabled()
    assert not window.comparator_sort_label.isEnabled()
    assert not window.comparator_complete_only.isEnabled()
    tip = window._actions["export_selected"].statusTip()
    assert "calcula un layout" in tip.lower() or "Calcula" in tip or "calcula" in tip
    assert "Exportar" in tip
    assert (
        "calcula un layout" in window._actions["previous_solution"].statusTip().lower()
    )
    assert "calcula un layout" in window._actions["next_solution"].statusTip().lower()
    assert "calcula un layout" in window.comparator_sort.statusTip().lower()


def test_solution_actions_single_candidate(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.layout.solutions = [_sol()]
    window.services.layout.selected_solution_index = 0
    window._reload_solution_table()

    assert window._actions["apply_layout"].isEnabled()
    assert window._actions["export_selected"].isEnabled()
    assert window._actions["export_cut_list"].isEnabled()
    assert not window._actions["previous_solution"].isEnabled()
    assert not window._actions["next_solution"].isEnabled()
    assert not window._actions["repack_omitted"].isEnabled()
    assert not window._actions["promote_offcuts"].isEnabled()
    assert not window.pin_reference_button.isEnabled()
    assert window.comparator_sort.isEnabled()
    assert window.comparator_complete_only.isEnabled()
    assert "1 candidata" in window._actions["next_solution"].statusTip()
    assert "1 candidata" in window.pin_reference_button.statusTip()
    assert "Ordena" in window.comparator_sort.statusTip()


def test_solution_actions_multiple_candidates(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.layout.solutions = [_sol(), _sol()]
    window.services.layout.selected_solution_index = 0
    window._reload_solution_table()

    assert window._actions["apply_layout"].isEnabled()
    assert window._actions["export_selected"].isEnabled()
    assert window._actions["export_cut_list"].isEnabled()
    assert window._actions["previous_solution"].isEnabled()
    assert window._actions["next_solution"].isEnabled()
    assert window.pin_reference_button.isEnabled()
    assert window.comparator_sort.isEnabled()
    assert window.comparator_complete_only.isEnabled()
    tip = window._actions["export_selected"].statusTip()
    assert "Comparador" in tip
    assert "PNG" in tip or "SVG" in tip
    assert "Ordena" in window.comparator_sort.statusTip()
    assert "parciales" in window.comparator_complete_only.statusTip()
    assert not window._actions["repack_omitted"].isEnabled()
    assert not window._actions["promote_offcuts"].isEnabled()


def test_repack_omitted_enabled_for_partial_and_places_leftover(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    from boardcomposer import Board, Project, StockPanel
    from boardcomposer.domain import PanelReference
    from studio.models import StudioBoard, StudioPiece, StudioProject

    window.services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Freeze",
            boards=[StudioBoard("P1", 1000, 500, "Demo", 19, 1)],
            pieces=[
                StudioPiece("A", 400, 300, "Demo", 19),
                StudioPiece("B", 200, 100, "Demo", 19),
            ],
        )
    )
    core = Project()
    core.add_stock_panel(StockPanel(1000, 500, 19, "P1"))
    core.add_board(Board(400, 300, 19, "A"))
    core.add_board(Board(200, 100, 19, "B"))
    window.services.layout._solved_project = core
    window.services.layout.solutions = [
        AssemblySolution(
            placements=[
                BoardPlacement(
                    "A",
                    0,
                    0,
                    400,
                    300,
                    panel_reference=PanelReference(0, 0),
                )
            ],
            omitted_piece_ids=("B",),
        )
    ]
    window.services.layout.selected_solution_index = 0
    window._reload_solution_table()

    assert window._actions["repack_omitted"].isEnabled()
    window._repack_omitted()
    packed = window.services.layout.selected_solution
    assert packed is not None
    assert {item.board_id for item in packed.placements} == {"A", "B"}
    assert packed.omitted_piece_ids == ()


def test_promote_offcuts_enabled_and_adds_remnant_board(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    from boardcomposer import Board, Project, StockPanel
    from boardcomposer.domain import Offcut, PanelReference
    from studio.models import StudioBoard, StudioPiece, StudioProject

    window.services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Retales",
            boards=[StudioBoard("P1", 1000, 500, "Melamina", 19, 1)],
            pieces=[StudioPiece("A", 400, 300, "Melamina", 19)],
        )
    )
    core = Project()
    core.add_stock_panel(StockPanel(1000, 500, 19, "P1", material="Melamina"))
    core.add_board(Board(400, 300, 19, "A", material="Melamina"))
    window.services.layout._solved_project = core
    window.services.layout.solutions = [
        AssemblySolution(
            placements=[
                BoardPlacement(
                    "A",
                    0,
                    0,
                    400,
                    300,
                    panel_reference=PanelReference(0, 0),
                )
            ],
            offcuts=(Offcut(PanelReference(0, 0), 400, 0, 600, 500),),
        )
    ]
    window.services.layout.selected_solution_index = 0
    window._reload_solution_table()

    assert window._actions["promote_offcuts"].isEnabled()
    window._promote_offcuts()
    project = window.services.projects.current_project
    assert project is not None
    remnant = next(board for board in project.boards if board.remnant)
    assert remnant.board_id == "P1-0-R1"
    assert remnant.length_mm == 600
    assert remnant.material == "Melamina"
    window._promote_offcuts()
    assert sum(1 for board in project.boards if board.remnant) == 1
