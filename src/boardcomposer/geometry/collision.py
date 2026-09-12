from boardcomposer.domain import BoardPlacement
from boardcomposer.geometry import Rectangle
from boardcomposer.layout.kerf import normalize_kerf


def placement_to_rectangle(
    placement: BoardPlacement, *, kerf_mm: float = 0.0
) -> Rectangle:
    kerf = normalize_kerf(kerf_mm)
    return Rectangle(
        x_mm=placement.x_mm,
        y_mm=placement.y_mm,
        length_mm=placement.length_mm + kerf,
        width_mm=placement.width_mm + kerf,
    )


def placements_overlap(
    a: BoardPlacement, b: BoardPlacement, *, kerf_mm: float = 0.0
) -> bool:
    return placement_to_rectangle(a, kerf_mm=kerf_mm).overlaps(
        placement_to_rectangle(b, kerf_mm=kerf_mm)
    )
