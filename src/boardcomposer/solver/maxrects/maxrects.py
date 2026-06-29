from boardcomposer.solver.maxrects.free_rectangle import FreeRectangle


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
