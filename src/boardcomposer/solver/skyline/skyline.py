from boardcomposer.solver.skyline.node import SkylineNode
from boardcomposer.solver.skyline.placement import SkylinePlacement


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

    def find_position(
        self,
        width_mm: float,
    ) -> SkylinePlacement | None:
        for node in self.nodes:
            if width_mm <= node.width_mm:
                return SkylinePlacement(
                    x_mm=node.x_mm,
                    y_mm=node.y_mm,
                )

        return None
