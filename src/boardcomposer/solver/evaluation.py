from boardcomposer.domain import AssemblySolution, SolutionExplanation, SolutionScore


def evaluate(solution: AssemblySolution) -> AssemblySolution:

    waste_score = max(0.0, (1.0 - solution.waste_ratio) * 50.0)
    usage_score = 50.0 if solution.placements else 0.0

    strengths = []
    weaknesses = []

    if solution.waste_ratio < 0.10:
        strengths.append("Muy poco desperdicio")
    elif solution.waste_ratio < 0.25:
        strengths.append("Desperdicio aceptable")
    else:
        weaknesses.append("Desperdicio elevado")

    return AssemblySolution(
        placements=solution.placements,
        score=SolutionScore(
            waste_score=waste_score,
            material_usage_score=usage_score,
        ),
        explanation=SolutionExplanation(
            strengths=strengths,
            weaknesses=weaknesses,
            notes=solution.explanation.notes,
        ),
    )
