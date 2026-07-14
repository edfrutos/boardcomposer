from collections.abc import Iterable

from boardcomposer.domain import AssemblySolution
from boardcomposer.solver.solution_ranking import solution_ranking_key


def search_best_solution(
    solutions: Iterable[AssemblySolution],
) -> AssemblySolution:
    return max(
        solutions,
        key=solution_ranking_key,
    )
