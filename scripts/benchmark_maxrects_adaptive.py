"""Compare fixed, contact and adaptive MaxRects strategies."""

from dataclasses import dataclass

from boardcomposer import Board, Project, ProjectConstraints
from boardcomposer.solver.board_ordering import largest_area_first
from boardcomposer.solver.maxrects.heuristics import (
    best_area_fit,
    best_bottom_left_fit,
    best_long_side_fit,
    best_short_side_fit,
)
from boardcomposer.solver.maxrects_runner import (
    generate_adaptive_maxrects_candidate,
    generate_contact_maxrects_candidate,
    generate_maxrects_candidate,
)


@dataclass(frozen=True)
class BenchmarkResult:
    scenario: str
    strategy: str
    placed: int
    bounding_area_mm2: float
    waste_ratio: float


FIXED_STRATEGIES = (
    ("area_fit", best_area_fit),
    ("short_side", best_short_side_fit),
    ("long_side", best_long_side_fit),
    ("bottom_left", best_bottom_left_fit),
)


SCENARIOS = {
    "tiras": [
        Board(1800, 120, 19, "A"),
        Board(1600, 120, 19, "B"),
        Board(1400, 120, 19, "C"),
        Board(1000, 120, 19, "D"),
        Board(800, 120, 19, "E"),
    ],
    "mixto": [
        Board(1800, 300, 19, "A"),
        Board(1200, 300, 19, "B"),
        Board(800, 200, 19, "C"),
        Board(700, 180, 19, "D"),
        Board(600, 250, 19, "E"),
        Board(500, 150, 19, "F"),
        Board(400, 120, 19, "G"),
    ],
    "cuadradas": [
        Board(600, 600, 19, "A"),
        Board(500, 500, 19, "B"),
        Board(400, 400, 19, "C"),
        Board(300, 300, 19, "D"),
        Board(250, 250, 19, "E"),
    ],
}


def make_project(boards: list[Board]) -> Project:
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=3000,
            max_width_mm=1200,
            allow_rotation=True,
        )
    )

    for board in boards:
        project.add_board(board)

    return project


def result_for(
    scenario: str,
    strategy: str,
    solution,
) -> BenchmarkResult:
    return BenchmarkResult(
        scenario=scenario,
        strategy=strategy,
        placed=len(solution.placements),
        bounding_area_mm2=solution.bounding_area_mm2,
        waste_ratio=solution.waste_ratio,
    )


def main() -> None:
    results: list[BenchmarkResult] = []

    for scenario, boards in SCENARIOS.items():
        project = make_project(boards)

        for strategy_name, heuristic in FIXED_STRATEGIES:
            solution = generate_maxrects_candidate(
                project=project,
                heuristic_name=strategy_name,
                heuristic=heuristic,
                ordering_name="largest_area",
                ordering=largest_area_first,
            )

            results.append(
                result_for(
                    scenario,
                    strategy_name,
                    solution,
                )
            )

        contact = generate_contact_maxrects_candidate(
            project=project,
            ordering_name="largest_area",
            ordering=largest_area_first,
        )

        adaptive = generate_adaptive_maxrects_candidate(
            project=project,
            ordering_name="largest_area",
            ordering=largest_area_first,
        )

        results.extend(
            [
                result_for(scenario, "contact", contact),
                result_for(scenario, "adaptive", adaptive),
            ]
        )

    print(
        f"{'Escenario':<12} {'Estrategia':<12} "
        f"{'Piezas':>7} {'Área':>12} {'Desperdicio':>12}"
    )

    for result in results:
        print(
            f"{result.scenario:<12} "
            f"{result.strategy:<12} "
            f"{result.placed:>7} "
            f"{result.bounding_area_mm2:>12.0f} "
            f"{result.waste_ratio:>11.1%}"
        )


if __name__ == "__main__":
    main()
