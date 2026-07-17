"""Tests for marking layout solutions outdated after project edits (FLW-006)."""

from boardcomposer.domain import AssemblySolution, BoardPlacement
from studio.events.catalog import PROJECT_MODIFIED, SOLUTIONS_MARKED_OUTDATED
from studio.services import StudioServices


def _fake_solution() -> AssemblySolution:
    return AssemblySolution(
        placements=[BoardPlacement("A", 0, 0, 100, 50)],
    )


def test_mark_project_modified_flags_existing_solutions():
    services = StudioServices()
    seen: list[str] = []
    services.events.subscribe(
        "*",
        lambda name, _payload: seen.append(name),
    )

    services.layout.solutions = [_fake_solution()]
    assert services.layout.solutions_outdated is False

    marked = services.mark_project_modified(reason="test")
    assert marked is True
    assert services.layout.solutions_outdated is True
    assert services.projects.is_modified is True
    assert PROJECT_MODIFIED in seen
    assert SOLUTIONS_MARKED_OUTDATED in seen

    # Second edit does not re-emit SolutionsMarkedOutdated.
    seen.clear()
    marked_again = services.mark_project_modified(reason="test-2")
    assert marked_again is False
    assert PROJECT_MODIFIED in seen
    assert SOLUTIONS_MARKED_OUTDATED not in seen


def test_mark_project_modified_skips_layout_when_requested():
    services = StudioServices()
    services.layout.solutions = [_fake_solution()]

    marked = services.mark_project_modified(
        affects_layout=False,
        reason="apply",
    )
    assert marked is False
    assert services.layout.solutions_outdated is False
    assert services.projects.is_modified is True


def test_solve_clears_outdated_flag():
    services = StudioServices()
    services.layout.solutions = [_fake_solution()]
    services.layout.solutions_outdated = True
    services.layout.clear_solutions()
    assert services.layout.solutions_outdated is False
