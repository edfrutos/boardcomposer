from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.solver.maxrects_runner import iter_maxrects_solutions


def generate_best_maxrects_solution(project: Project) -> AssemblySolution:
    return max(
        iter_maxrects_solutions(project),
        key=lambda solution: (
            len(solution.placements),
            -solution.total_width_mm,
            -solution.total_length_mm,
        ),
    )
