"""v1 pipeline: load CSV → solve → export (no Studio / Qt)."""

from __future__ import annotations

from pathlib import Path

from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.export import solution_to_csv, solution_to_json, solution_to_svg
from boardcomposer.io import load_project_from_csv
from boardcomposer.solver import GeometrySolver
from boardcomposer.solver.strategies import strategy_by_name


def load_project(path: str | Path) -> Project:
    """Load a project from a boards CSV (same format as the CLI ``--csv``)."""
    return load_project_from_csv(path)


def solve(
    project: Project,
    *,
    strategy: str = "balanced",
    top: int | None = None,
) -> list[AssemblySolution]:
    """Run the geometry solver and return ranked solutions.

    ``strategy`` accepts the same names as the CLI: ``balanced``,
    ``material``, ``compact``.
    When ``top`` is set, only the first ``top`` solutions are returned.
    """
    optimization = strategy_by_name(strategy)
    solutions = GeometrySolver(project, strategy=optimization).solve()
    if top is None:
        return solutions
    if top <= 0:
        return []
    return solutions[:top]


def export_json(
    solution: AssemblySolution,
    project: Project | None = None,
    *,
    strategy_name: str | None = None,
    solution_index: int | None = None,
) -> str:
    """Serialize one solution as a JSON document string."""
    return solution_to_json(
        solution,
        project,
        strategy_name=strategy_name,
        solution_index=solution_index,
    )


def export_svg(
    solution: AssemblySolution,
    project: Project | None = None,
) -> str:
    """Render one solution as an SVG document string."""
    return solution_to_svg(solution, project)


def export_csv(solution: AssemblySolution) -> str:
    """Export placements of one solution as a CSV table string."""
    return solution_to_csv(solution)


def run(
    path: str | Path,
    *,
    strategy: str = "balanced",
    top: int | None = None,
) -> tuple[Project, list[AssemblySolution]]:
    """Load a CSV project and solve it in one call."""
    project = load_project(path)
    return project, solve(project, strategy=strategy, top=top)
