from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.solver.maxrects_runner import iter_maxrects_solutions
from boardcomposer.solver.search import search_best_solution


def generate_best_maxrects_solution(project: Project) -> AssemblySolution:
    return search_best_solution(iter_maxrects_solutions(project))
