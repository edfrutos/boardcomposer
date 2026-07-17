from PySide6.QtWidgets import QGraphicsScene

from studio.workspace.canvas_style import pen


def add_grid(scene: QGraphicsScene, grid_size: int = 100) -> None:
    grid_pen = pen("grid", 1)
    scene_rect = scene.sceneRect()

    for x_value in range(
        int(scene_rect.left()), int(scene_rect.right()) + 1, grid_size
    ):
        scene.addLine(x_value, scene_rect.top(), x_value, scene_rect.bottom(), grid_pen)

    for y_value in range(
        int(scene_rect.top()), int(scene_rect.bottom()) + 1, grid_size
    ):
        scene.addLine(scene_rect.left(), y_value, scene_rect.right(), y_value, grid_pen)
