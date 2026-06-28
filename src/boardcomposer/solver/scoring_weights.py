from dataclasses import dataclass


@dataclass(frozen=True)
class ScoringWeights:
    material_utilization: float = 40.0
    placed_boards: float = 30.0
    compactness: float = 20.0
    rotation_penalty: float = 10.0
