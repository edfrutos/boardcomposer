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
                        rectangle.x_mm, rectangle.y_mm, length_mm, width_mm)
                )

            if allow_rotation and rectangle.fits(width_mm, length_mm):
                candidates.append(
                    MaxRectsPlacement(
                        rectangle.x_mm,
                        rectangle.y_mm,
                        width_mm,
                        length_mm,
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

    def place(
        self,
        length_mm: float,
        width_mm: float,
        allow_rotation: bool = False,
    ) -> MaxRectsPlacement | None:
        placement = self.find_best_rectangle(
            length_mm=length_mm,
            width_mm=width_mm,
            allow_rotation=allow_rotation,
        )

        if placement is None:
            return None

        used = placement
        new_rectangles: list[FreeRectangle] = []

        for rectangle in self.free_rectangles:
            if not self._intersects(rectangle, used):
                new_rectangles.append(rectangle)
                continue

            new_rectangles.extend(self._split_free_rectangle(rectangle, used))

        self.free_rectangles = [
            rectangle for rectangle in new_rectangles if rectangle.area_mm2 > 0
        ]
        self._prune_free_rectangles()

        return placement

    def _prune_free_rectangles(self) -> None:
        pruned = []

        for index, rectangle in enumerate(self.free_rectangles):
            contained = False

            for other_index, other in enumerate(self.free_rectangles):
                if index == other_index:
                    continue

                if self._contains(other, rectangle):
                    contained = True
                    break

            if not contained:
                pruned.append(rectangle)

        self.free_rectangles = pruned

    def _contains(
        self,
        outer: FreeRectangle,
        inner: FreeRectangle,
    ) -> bool:
        return (
            inner.x_mm >= outer.x_mm
            and inner.y_mm >= outer.y_mm
            and inner.x_mm + inner.length_mm <= outer.x_mm + outer.length_mm
            and inner.y_mm + inner.width_mm <= outer.y_mm + outer.width_mm
        )

    def _split_free_rectangle(
        self,
        rectangle: FreeRectangle,
        used: MaxRectsPlacement,
    ) -> list[FreeRectangle]:
        result = []

        rect_right = rectangle.x_mm + rectangle.length_mm
        rect_bottom = rectangle.y_mm + rectangle.width_mm
        used_right = used.x_mm + used.length_mm
        used_bottom = used.y_mm + used.width_mm

        if used.x_mm > rectangle.x_mm:
            result.append(
                FreeRectangle(
                    rectangle.x_mm,
                    rectangle.y_mm,
                    used.x_mm - rectangle.x_mm,
                    rectangle.width_mm,
                )
            )

        if used_right < rect_right:
            result.append(
                FreeRectangle(
                    used_right,
                    rectangle.y_mm,
                    rect_right - used_right,
                    rectangle.width_mm,
                )
            )

        if used.y_mm > rectangle.y_mm:
            result.append(
                FreeRectangle(
                    rectangle.x_mm,
                    rectangle.y_mm,
                    rectangle.length_mm,
                    used.y_mm - rectangle.y_mm,
                )
            )

        if used_bottom < rect_bottom:
            result.append(
                FreeRectangle(
                    rectangle.x_mm,
                    used_bottom,
                    rectangle.length_mm,
                    rect_bottom - used_bottom,
                )
            )

        return result

    def _intersects(
        self,
        rectangle: FreeRectangle,
        used: MaxRectsPlacement,
    ) -> bool:
        return not (
            used.x_mm >= rectangle.x_mm + rectangle.length_mm
            or used.x_mm + used.length_mm <= rectangle.x_mm
            or used.y_mm >= rectangle.y_mm + rectangle.width_mm
            or used.y_mm + used.width_mm <= rectangle.y_mm
        )

    def _waste_area(self, placement: MaxRectsPlacement) -> float:
        container = next(
            rectangle
            for rectangle in self.free_rectangles
            if rectangle.x_mm == placement.x_mm and rectangle.y_mm == placement.y_mm
        )

        return container.area_mm2 - (placement.length_mm * placement.width_mm)
