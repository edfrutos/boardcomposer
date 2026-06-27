from dataclasses import dataclass, field

from .placement import BoardPlacement
from .score import SolutionScore


@dataclass(frozen=True)
class AssemblySolution:
    placements: list[BoardPlacement]
    score: SolutionScore = field(default_factory=SolutionScore)
    notes: list[str] = field(default_factory=list)

    @property
    def used_area_mm2(self) -> float:
        return sum(p.area_mm2 for p in self.placements)

    @property
    def total_length_mm(self) -> float:
        if not self.placements:
            return 0
        return max(p.right_mm for p in self.placements)

    @property
    def total_width_mm(self) -> float:
        if not self.placements:
            return 0
        return max(p.top_mm for p in self.placements)

    @property
    def bounding_area_mm2(self) -> float:
        return self.total_length_mm * self.total_width_mm

    @property
    def waste_area_mm2(self) -> float:
        return self.bounding_area_mm2 - self.used_area_mm2

    @property
    def waste_ratio(self) -> float:
        if self.bounding_area_mm2 == 0:
            return 0
        return self.waste_area_mm2 / self.bounding_area_mm2
