from boardcomposer.domain import (
    AssemblySolution,
    Project,
    SolutionExplanation,
    SolutionScore,
)
from boardcomposer.solver.scoring_weights import ScoringWeights
from boardcomposer.solver.objectives import (
    compactness,
    material_utilization,
    placed_board_ratio,
    rotation_ratio,
)


def evaluate(
    solution: AssemblySolution,
    total_boards: int | None = None,
    weights: ScoringWeights | None = None,
    project: Project | None = None,
    omitted_piece_ids: tuple[str, ...] = (),
) -> AssemblySolution:
    total = total_boards if total_boards is not None else len(solution.placements)
    weights = weights or ScoringWeights()

    utilization = material_utilization(solution, project)
    waste_score = utilization * weights.material_utilization
    usage_score = placed_board_ratio(solution, total) * weights.placed_boards
    regularity_score = compactness(solution) * weights.compactness
    rotation_penalty = rotation_ratio(solution) * weights.rotation_penalty
    cuts_score = max(0.0, 10.0 - rotation_penalty)

    strengths = []
    weaknesses = []

    if utilization >= 0.90:
        strengths.append("Muy buen aprovechamiento del material")
    elif utilization < 0.70:
        weaknesses.append("Aprovechamiento bajo del material")

    if compactness(solution) >= 0.50:
        strengths.append("Composición compacta")
    else:
        weaknesses.append("Composición alargada o poco compacta")

    if omitted_piece_ids:
        weaknesses.append(
            f"Solución parcial: {len(omitted_piece_ids)} pieza(s) sin colocar"
        )

    return AssemblySolution(
        placements=solution.placements,
        score=SolutionScore(
            waste_score=waste_score,
            material_usage_score=usage_score,
            regularity_score=regularity_score,
            cuts_score=cuts_score,
        ),
        explanation=SolutionExplanation(
            strengths=strengths,
            weaknesses=weaknesses,
            notes=solution.explanation.notes,
        ),
        omitted_piece_ids=omitted_piece_ids or solution.omitted_piece_ids,
        offcuts=solution.offcuts,
    )
