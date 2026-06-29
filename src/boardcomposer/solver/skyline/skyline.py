from boardcomposer.solver.skyline.node import SkylineNode


class Skyline:
    def __init__(self, width_mm: float = 3000.0) -> None:
        self.width_mm = width_mm
        self.nodes = [
            SkylineNode(
                x_mm=0.0,
                y_mm=0.0,
                width_mm=width_mm,
            )
        ]
