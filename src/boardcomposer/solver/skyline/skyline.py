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
        candidates = [
            node
            for node in self.nodes
            if width_mm <= node.width_mm
        ]

        if not candidates:
            return None

        best = min(
            candidates,
            key=lambda node: (node.y_mm, node.x_mm),
        )

        return SkylinePlacement(
            x_mm=best.x_mm,
            y_mm=best.y_mm,
        )

    def place(
        self,
        width_mm: float,
        height_mm: float,
    ) -> SkylinePlacement | None:
        position = self.find_position(width_mm)

        if position is None:
            return None

        node_index = next(
            index
            for index, node in enumerate(self.nodes)
            if node.x_mm == position.x_mm and node.y_mm == position.y_mm
        )
        node = self.nodes.pop(node_index)

        remaining = node.width_mm - width_mm

        self.nodes.insert(
            0,
            SkylineNode(
                x_mm=node.x_mm,
                y_mm=node.y_mm + height_mm,
                width_mm=width_mm,
            ),
        )

        if remaining > 0:
            self.nodes.insert(
                1,
                SkylineNode(
                    x_mm=node.x_mm + width_mm,
                    y_mm=node.y_mm,
                    width_mm=remaining,
                ),
            )

        return position
