"""Tests for the exploratory CP-SAT single-panel generator (ADR-017)."""

from unittest.mock import patch

import pytest

from boardcomposer import Board, Project, ProjectConstraints
from boardcomposer.solver.cp_sat_runner import (
    CpSatUnavailableError,
    generate_cp_sat_solution,
)
from boardcomposer.solver.generators import GENERATOR_REGISTRY, cp_sat_generator
from boardcomposer.solver.strategies import exact_strategy, strategy_by_name


def test_cp_sat_is_registered_as_a_generator():
    assert "cp_sat" in GENERATOR_REGISTRY


def test_exact_strategy_includes_maxrects_and_cp_sat():
    strategy = exact_strategy()

    assert strategy.name == "exact"
    assert strategy.generator_names == ("maxrects", "cp_sat")
    assert strategy_by_name("exact").name == "exact"


def test_generate_cp_sat_solution_raises_when_ortools_is_missing():
    with patch("boardcomposer.solver.cp_sat_runner.cp_model", None):
        with pytest.raises(CpSatUnavailableError):
            generate_cp_sat_solution(
                Project(
                    constraints=ProjectConstraints(
                        max_length_mm=1000,
                        max_width_mm=500,
                    )
                )
            )


def test_cp_sat_generator_returns_empty_list_when_ortools_is_missing():
    with patch("boardcomposer.solver.cp_sat_runner.cp_model", None):
        solutions = cp_sat_generator(
            Project(
                constraints=ProjectConstraints(
                    max_length_mm=1000,
                    max_width_mm=500,
                )
            )
        )

    assert solutions == []


@pytest.fixture
def ortools_available():
    pytest.importorskip("ortools")


def test_cp_sat_places_every_piece_that_fits(ortools_available):
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=1000,
            max_width_mm=500,
            allow_rotation=True,
        )
    )
    project.add_board(Board(400, 300, 19, "A"))
    project.add_board(Board(400, 300, 19, "B"))

    solution = generate_cp_sat_solution(project, time_limit_seconds=2.0)

    assert len(solution.placements) == 2
    assert solution.omitted_piece_ids == ()
    assert "cp_sat" in solution.explanation.notes
    assert set(solution.explanation.notes) & {"optimo", "factible"}


def test_cp_sat_reports_pieces_that_never_fit_as_omitted(ortools_available):
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=500,
            max_width_mm=500,
            allow_rotation=False,
        )
    )
    project.add_board(Board(400, 400, 19, "A"))
    project.add_board(Board(900, 900, 19, "B"))

    solution = generate_cp_sat_solution(project, time_limit_seconds=2.0)

    assert [placement.board_id for placement in solution.placements] == ["A"]
    assert solution.omitted_piece_ids == ("B",)


def test_cp_sat_returns_an_empty_partial_solution_without_panel_bounds(
    ortools_available,
):
    project = Project(constraints=ProjectConstraints(allow_rotation=True))
    project.add_board(Board(400, 300, 19, "A"))

    solution = generate_cp_sat_solution(project)

    assert solution.placements == []
    assert solution.omitted_piece_ids == ("A",)
    assert "sin_panel" in solution.explanation.notes


def test_cp_sat_generator_returns_a_solution_when_ortools_is_installed(
    ortools_available,
):
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=1000,
            max_width_mm=500,
            allow_rotation=True,
        )
    )
    project.add_board(Board(400, 300, 19, "A"))

    solutions = cp_sat_generator(project)

    assert len(solutions) == 1
    assert solutions[0].placements
