"""Tests for solution placement replay (ADR-005)."""

from boardcomposer.domain import AssemblySolution, BoardPlacement
from studio.timeline.replay import SolutionReplay


def _solution_with_placements(count: int) -> AssemblySolution:
    placements = [
        BoardPlacement(f"P-{index}", float(index * 10), 0.0, 100.0, 50.0)
        for index in range(count)
    ]
    return AssemblySolution(placements=placements)


def test_solution_replay_steps_forward_and_back():
    replay = SolutionReplay()
    solution = _solution_with_placements(3)
    replay.load(solution)

    assert replay.total == 3
    assert replay.step == 3

    assert replay.reset() == 0
    assert replay.step_forward() == 1
    assert replay.step_forward() == 2
    assert replay.step_back() == 1
    assert replay.finish() == 3


def test_solution_replay_play_wraps_from_end():
    replay = SolutionReplay()
    replay.load(_solution_with_placements(2))
    assert replay.step == 2

    replay.start()
    assert replay.playing
    assert replay.step == 0

    replay.step_forward()
    replay.step_forward()
    assert replay.step == 2
    assert not replay.playing


def test_solution_replay_empty_solution_disabled():
    replay = SolutionReplay()
    replay.load(AssemblySolution(placements=[]))
    assert not replay.available
    replay.start()
    assert not replay.playing
