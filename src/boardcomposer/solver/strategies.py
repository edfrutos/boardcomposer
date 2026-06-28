from dataclasses import dataclass

from boardcomposer.solver.scoring_weights import (
    ScoringWeights,
    balanced,
    compact_first,
    material_first,
)


@dataclass(frozen=True)
class OptimizationStrategy:
    name: str
    weights: ScoringWeights


def balanced_strategy() -> OptimizationStrategy:
    return OptimizationStrategy(
        name="balanced",
        weights=balanced(),
    )


def material_first_strategy() -> OptimizationStrategy:
    return OptimizationStrategy(
        name="material",
        weights=material_first(),
    )


def compact_first_strategy() -> OptimizationStrategy:
    return OptimizationStrategy(
        name="compact",
        weights=compact_first(),
    )


def strategy_by_name(name: str) -> OptimizationStrategy:
    strategies = {
        "balanced": balanced_strategy,
        "material": material_first_strategy,
        "compact": compact_first_strategy,
    }

    try:
        return strategies[name]()
    except KeyError as exc:
        valid = ", ".join(sorted(strategies))
        raise ValueError(f"Estrategia desconocida: {name}. Válidas: {valid}") from exc
