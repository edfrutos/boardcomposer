from boardcomposer.domain import AssemblySolution, SolutionExplanation, SolutionScore
from boardcomposer.solver.objectives import (
    compactness,
    material_utilization,
    placed_board_ratio,
    rotation_ratio,
)


def evaluate(solution: AssemblySolution, total_boards: int | None = None) -> AssemblySolution:
    total = total_boards if total_boards is not None else len(solution.placements)

    waste_score = material_utilization(solution) * 40.0
    usage_score = placed_board_ratio(solution, total) * 30.0
    regularity_score = compactness(solution) * 20.0
    rotation_penalty = rotation_ratio(solution) * 10.0
    cuts_score = max(0.0, 10.0 - rotation_penalty)

    strengths = []
    weaknesses = []

    if material_utilization(solution) >= 0.90:
        strengths.append("Muy buen aprovechamiento del material")
    elif material_utilization(solution) < 0.70:
        weaknesses.append("Aprovechamiento bajo del material")

    if compactness(solution) >= 0.50:
        strengths.append("Composición compacta")
    else:
        weaknesses.append("Composición alargada o poco compacta")

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
    )
