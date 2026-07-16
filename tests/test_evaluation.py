from boardcomposer import AssemblySolution, Offcut, PanelReference
from boardcomposer.solver.evaluation import evaluate


def test_evaluation_returns_score():
    solution = evaluate(AssemblySolution(placements=[]))

    assert solution.score.total >= 0


def test_evaluation_preserves_offcuts():
    """evaluate() rebuilds the solution to attach scoring; it must not
    silently drop the offcuts reported by the generator (ADR-016)."""
    offcuts = (Offcut(PanelReference(0, 0), 400, 0, 600, 1000),)
    solution = evaluate(AssemblySolution(placements=[], offcuts=offcuts))

    assert solution.offcuts == offcuts
