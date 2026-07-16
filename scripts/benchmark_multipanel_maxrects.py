"""Reproducible benchmarks for `generate_multi_panel_maxrects_solution`.

Every scenario below is built from a fixed random seed, so re-running this
script always exercises the exact same boards/panels and can be used to spot
regressions in packing quality (waste, offcuts, omitted pieces) or in
generation time as the solver's search space grows (heuristics x board
orderings x panel orderings, see ADR-014/ADR-015/ADR-016).

Usage:
    python scripts/benchmark_multipanel_maxrects.py
"""

from __future__ import annotations

import random
import time
from dataclasses import dataclass

from boardcomposer import Board, Project, ProjectConstraints, StockPanel
from boardcomposer.solver.multi_panel_maxrects import (
    generate_multi_panel_maxrects_solution,
)


@dataclass(frozen=True)
class BenchmarkResult:
    scenario: str
    board_count: int
    panel_instance_count: int
    elapsed_ms: float
    placed: int
    omitted: int
    panel_waste_ratio: float
    offcut_count: int
    offcut_area_mm2: float


def _random_boards(
    rng: random.Random,
    count: int,
    *,
    min_mm: float = 150,
    max_mm: float = 900,
    thickness_mm: float = 19,
    material: str = "Generico",
) -> list[Board]:
    return [
        Board(
            length_mm=rng.randint(int(min_mm), int(max_mm)),
            width_mm=rng.randint(int(min_mm), int(max_mm)),
            thickness_mm=thickness_mm,
            id=f"P{index + 1}",
            material=material,
        )
        for index in range(count)
    ]


def _scenario_small_single_material() -> Project:
    rng = random.Random(1)
    project = Project(constraints=ProjectConstraints(allow_rotation=True))
    project.add_stock_panel(
        StockPanel(2440, 1220, 19, "TAB-1", quantity=2, material="Melamina")
    )
    for board in _random_boards(rng, 12, material="Melamina"):
        project.add_board(board)
    return project


def _scenario_medium_mixed_panel_types() -> Project:
    rng = random.Random(2)
    project = Project(constraints=ProjectConstraints(allow_rotation=True))
    project.add_stock_panel(
        StockPanel(2440, 1220, 19, "TAB-1", quantity=2, material="Melamina")
    )
    project.add_stock_panel(
        StockPanel(2750, 1830, 19, "TAB-2", quantity=1, material="Melamina")
    )
    for board in _random_boards(rng, 25, material="Melamina"):
        project.add_board(board)
    return project


def _scenario_two_materials() -> Project:
    rng = random.Random(3)
    project = Project(constraints=ProjectConstraints(allow_rotation=True))
    project.add_stock_panel(
        StockPanel(2440, 1220, 19, "TAB-MEL", quantity=2, material="Melamina")
    )
    project.add_stock_panel(
        StockPanel(2440, 1220, 19, "TAB-MDF", quantity=2, material="MDF")
    )
    for board in _random_boards(rng, 10, material="Melamina"):
        project.add_board(board)
    for board in _random_boards(rng, 10, material="MDF"):
        project.add_board(board)
    return project


def _scenario_insufficient_inventory() -> Project:
    """More/larger pieces than the available panels can ever hold, to
    benchmark the partial-solution path (ADR-014's soft-validation rules)."""
    rng = random.Random(4)
    project = Project(constraints=ProjectConstraints(allow_rotation=True))
    project.add_stock_panel(
        StockPanel(1220, 610, 19, "TAB-1", quantity=1, material="Melamina")
    )
    for board in _random_boards(rng, 15, min_mm=300, max_mm=700, material="Melamina"):
        project.add_board(board)
    return project


def _scenario_large_stress() -> Project:
    rng = random.Random(5)
    project = Project(constraints=ProjectConstraints(allow_rotation=True))
    project.add_stock_panel(
        StockPanel(2440, 1220, 19, "TAB-1", quantity=4, material="Melamina")
    )
    project.add_stock_panel(
        StockPanel(2750, 1830, 19, "TAB-2", quantity=2, material="Melamina")
    )
    for board in _random_boards(rng, 60, min_mm=100, max_mm=600, material="Melamina"):
        project.add_board(board)
    return project


SCENARIOS: dict[str, callable] = {
    "pequeno-1-material": _scenario_small_single_material,
    "medio-2-tipos-panel": _scenario_medium_mixed_panel_types,
    "2-materiales": _scenario_two_materials,
    "inventario-insuficiente": _scenario_insufficient_inventory,
    "grande-estres": _scenario_large_stress,
}


def _run(scenario_name: str, build_project: callable) -> BenchmarkResult:
    project = build_project()

    started = time.perf_counter()
    solution = generate_multi_panel_maxrects_solution(project)
    elapsed_ms = (time.perf_counter() - started) * 1000

    # `generate_multi_panel_maxrects_solution` returns the raw candidate,
    # before `evaluate()` fills in `omitted_piece_ids` (see evaluation.py),
    # so unplaced boards are counted directly from what wasn't placed.
    placed = len(solution.placements)

    return BenchmarkResult(
        scenario=scenario_name,
        board_count=len(project.boards),
        panel_instance_count=len(project.stock_panel_instances()),
        elapsed_ms=elapsed_ms,
        placed=placed,
        omitted=len(project.boards) - placed,
        panel_waste_ratio=solution.panel_waste_ratio(project),
        offcut_count=len(solution.offcuts),
        offcut_area_mm2=solution.total_offcut_area_mm2,
    )


def main() -> None:
    results = [_run(name, builder) for name, builder in SCENARIOS.items()]

    header = (
        f"{'Escenario':<24} {'Tableros':>8} {'Paneles':>8} {'Tiempo':>9} "
        f"{'Colocadas':>10} {'Omitidas':>9} {'Desperdicio':>12} "
        f"{'Retales':>8} {'Área retal':>12}"
    )
    print(header)
    print("-" * len(header))

    for result in results:
        print(
            f"{result.scenario:<24} "
            f"{result.board_count:>8} "
            f"{result.panel_instance_count:>8} "
            f"{result.elapsed_ms:>7.1f}ms "
            f"{result.placed:>10} "
            f"{result.omitted:>9} "
            f"{result.panel_waste_ratio:>11.1%} "
            f"{result.offcut_count:>8} "
            f"{result.offcut_area_mm2:>12.0f}"
        )


if __name__ == "__main__":
    main()
