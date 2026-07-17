"""Tests for SolveTrace phase replay (ADR-005)."""

from boardcomposer.solver.solve_trace import SolveTrace
from studio.timeline.phase_replay import SolvePhaseReplay


def test_phase_replay_loads_relevant_events_only():
    trace = SolveTrace()
    trace.record("generator_started", algorithm="skyline")
    trace.record("generator_finished", algorithm="skyline", count=1, duration_ms=3)
    trace.record("evaluation_started", unique=1)
    trace.record("evaluation_finished", accepted=1, rejected=0, duration_ms=1)

    replay = SolvePhaseReplay()
    replay.load(trace)

    assert replay.total == 4
    assert replay.step == 4
    assert replay.current is not None
    assert replay.current.kind == "evaluation_finished"


def test_phase_replay_steps_forward_and_back():
    trace = SolveTrace()
    trace.record("generator_started", algorithm="maxrects")
    trace.record("placement_failed", piece="A", reason="no_fit", algorithm="maxrects")
    trace.record("generator_finished", algorithm="maxrects", count=0)

    replay = SolvePhaseReplay()
    replay.load(trace)
    assert replay.reset() == 0
    assert replay.current is None

    assert replay.step_forward() == 1
    assert replay.current is not None
    assert replay.current.kind == "generator_started"
    assert replay.step_forward() == 2
    assert replay.current.payload["piece"] == "A"
    assert replay.step_back() == 1
    assert replay.finish() == 3


def test_phase_replay_play_cycles_from_end():
    trace = SolveTrace()
    trace.record("cancelled")
    replay = SolvePhaseReplay()
    replay.load(trace)
    assert replay.step == 1
    replay.start()
    assert replay.playing
    assert replay.step == 0
    assert replay.step_forward() == 1
    assert not replay.playing
