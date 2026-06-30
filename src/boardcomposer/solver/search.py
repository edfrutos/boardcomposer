from collections.abc import Iterable

from boardcomposer.domain import AssemblySolution
from boardcomposer.solver.solution_selector import select_best_solution


def search_best_solution(
    solutions: Iterable[AssemblySolution],
) -> AssemblySolution:
    return select_best_solution(solutions)
