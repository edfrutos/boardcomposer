from boardcomposer.domain import BoardPlacement
from boardcomposer.geometry.collision import placements_overlap


def has_overlaps(placements: list[BoardPlacement], *, kerf_mm: float = 0.0) -> bool:
    for i, current in enumerate(placements):
        for other in placements[i + 1 :]:
            if placements_overlap(current, other, kerf_mm=kerf_mm):
                return True
    return False
