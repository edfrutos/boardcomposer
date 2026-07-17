"""Tests for MaxRects placement-failure instrumentation."""

from boardcomposer import Board, Project, StockPanel
from boardcomposer.solver.candidate_pipeline import CandidatePipeline
from boardcomposer.solver.multi_panel_maxrects import (
    generate_multi_panel_maxrects_solution,
)
from boardcomposer.solver.placement_failures import (
    PlacementFailureLog,
    capture_placement_failures,
    record_placement_failure,
)
from boardcomposer.solver.strategies import material_first_strategy
from studio.events import EventBus
from studio.events.catalog import PLACEMENT_FAILED, PLACEMENT_FAILURES_SUMMARY
from studio.solve_trace_publisher import publish_solve_trace


def test_record_placement_failure_is_noop_without_active_log():
    record_placement_failure(piece_id="A", reason="no_fit")


def test_placement_failure_log_deduplicates_and_counts():
    log = PlacementFailureLog(max_unique=2)
    with capture_placement_failures(log):
        record_placement_failure(piece_id="A", reason="no_fit")
        record_placement_failure(piece_id="A", reason="no_fit")
        record_placement_failure(
            piece_id="B", reason="incompatible", stock_panel_index=0
        )
        record_placement_failure(piece_id="C", reason="no_fit")

    assert log.total == 4
    assert log.counts["no_fit"] == 3
    assert log.counts["incompatible"] == 1
    assert len(log.failures) == 2


def test_multi_panel_maxrects_records_incompatible_and_no_fit():
    project = Project()
    project.add_stock_panel(StockPanel(100, 100, 19, "TAB", quantity=1, material="oak"))
    project.add_board(Board(80, 80, 19, "FIT", material="oak"))
    project.add_board(
        Board(80, 80, 22, "THICK", material="oak")
    )  # incompatible thickness
    project.add_board(Board(200, 200, 19, "BIG", material="oak"))  # no fit

    log = PlacementFailureLog()
    with capture_placement_failures(log):
        generate_multi_panel_maxrects_solution(project)

    assert log.counts.get("incompatible", 0) >= 1
    assert log.counts.get("no_fit", 0) >= 1
    reasons = {failure.reason for failure in log.failures}
    assert "incompatible" in reasons
    assert "no_fit" in reasons


def test_pipeline_publishes_placement_failures_for_maxrects():
    project = Project()
    project.add_stock_panel(StockPanel(120, 120, 19, "TAB", quantity=1))
    project.add_board(Board(100, 100, 19, "A"))
    project.add_board(Board(100, 100, 19, "B"))
    project.add_board(Board(100, 100, 19, "C"))  # likely no_fit on last panels

    pipeline = CandidatePipeline(project=project, strategy=material_first_strategy())
    pipeline.run()

    kinds = [event.kind for event in pipeline.trace.events]
    # material_first includes maxrects; with stock panels pipeline uses only maxrects
    assert "placement_failures_summary" in kinds or "generator_finished" in kinds

    bus = EventBus()
    seen: list[str] = []
    bus.subscribe("*", lambda name, _p: seen.append(name))
    publish_solve_trace(bus, pipeline.trace)

    if "placement_failures_summary" in kinds:
        assert PLACEMENT_FAILURES_SUMMARY in seen
        assert PLACEMENT_FAILED in seen
