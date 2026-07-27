"""PgUp/PgDown follow comparator display order (SCR-003)."""

from boardcomposer.domain import (
    AssemblySolution,
    BoardPlacement,
    SolutionExplanation,
    SolutionScore,
)
from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _solution(placements, *, score: float, omitted=()) -> AssemblySolution:
    return AssemblySolution(
        placements=placements,
        score=SolutionScore(waste_score=score),
        explanation=SolutionExplanation(),
        omitted_piece_ids=omitted,
    )


def test_page_navigation_follows_sorted_display_order(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Nav",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
            pieces=[
                StudioPiece("A", 10, 10, "Demo", 19),
                StudioPiece("B", 10, 10, "Demo", 19),
                StudioPiece("C", 10, 10, "Demo", 19),
            ],
            placements=[StudioPlacement("A", 0, 0, False, 0, "B1", 0, 0)],
        )
    )
    # Solver order 0,1,2 — pieces count makes display order 1, 2, 0.
    services.layout.solutions = [
        _solution([BoardPlacement("A", 0, 0, 10, 10)], score=1.0),
        _solution(
            [
                BoardPlacement("A", 0, 0, 10, 10),
                BoardPlacement("B", 10, 0, 10, 10),
                BoardPlacement("C", 20, 0, 10, 10),
            ],
            score=3.0,
        ),
        _solution(
            [
                BoardPlacement("A", 0, 0, 10, 10),
                BoardPlacement("B", 10, 0, 10, 10),
            ],
            score=2.0,
        ),
    ]
    services.layout.select_solution(0)
    window = MainWindow(services)
    window._comparator_sort_by = "pieces"
    window._reload_solution_table()
    assert window._solution_display_indexes == [1, 2, 0]

    window._next_layout_solution()
    assert services.layout.selected_solution_index == 1

    window._next_layout_solution()
    assert services.layout.selected_solution_index == 2

    window._next_layout_solution()
    assert services.layout.selected_solution_index == 0

    window._previous_layout_solution()
    assert services.layout.selected_solution_index == 2
