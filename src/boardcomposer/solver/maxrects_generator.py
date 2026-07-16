from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.solver.maxrects_search import (
    generate_beam_maxrects_solution,
    generate_best_maxrects_solution,
)
from boardcomposer.solver.multi_panel_maxrects import (
    generate_multi_panel_maxrects_solution,
)
from boardcomposer.solver.search import search_best_solution


def generate_maxrects_solution(project: Project) -> AssemblySolution:
    if project.stock_panels:
        return generate_multi_panel_maxrects_solution(project)

    classic = generate_best_maxrects_solution(project)
    beam = generate_beam_maxrects_solution(
        project,
        beam_width=2,
        candidate_width=None,
    )

    return search_best_solution([classic, beam])
