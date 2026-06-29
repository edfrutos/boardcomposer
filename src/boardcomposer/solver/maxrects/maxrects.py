from boardcomposer.solver.maxrects.free_rectangle import FreeRectangle
from boardcomposer.solver.maxrects.placement import MaxRectsPlacement


class MaxRects:
    def __init__(
        self,
        length_mm: float = 3000,
        width_mm: float = 3000,
    ) -> None:
        self.length_mm = length_mm
        self.width_mm = width_mm

        self.free_rectangles = [
            FreeRectangle(
                x_mm=0,
                y_mm=0,
                length_mm=length_mm,
                width_mm=width_mm,
            )
        ]

    def find_best_rectangle(
        self,
        length_mm: float,
        width_mm: float,
        allow_rotation: bool = False,
    ) -> MaxRectsPlacement | None:
        candidates = []

        for rectangle in self.free_rectangles:
            if rectangle.fits(length_mm, width_mm):
                candidates.append(
                    MaxRectsPlacement(
                        x_mm=rectangle.x_mm,
                        y_mm=rectangle.y_mm,
                        length_mm=length_mm,
                        width_mm=width_mm,
                        rotated=False,
                    )
                )

            if allow_rotation and rectangle.fits(width_mm, length_mm):
                candidates.append(
                    MaxRectsPlacement(
                        x_mm=rectangle.x_mm,
                        y_mm=rectangle.y_mm,
                        length_mm=width_mm,
                        width_mm=length_mm,
                        rotated=True,
                    )
                )

        if not candidates:
            return None

        return min(
            candidates,
            key=lambda candidate: (
                self._waste_area(candidate),
                candidate.y_mm,
                candidate.x_mm,
            ),
        )

    def _waste_area(self, placement: MaxRectsPlacement) -> float:
        container = next(
            rectangle
            for rectangle in self.free_rectangles
            if rectangle.x_mm == placement.x_mm and rectangle.y_mm == placement.y_mm
        )

        return container.area_mm2 - (placement.length_mm * placement.width_mm)
