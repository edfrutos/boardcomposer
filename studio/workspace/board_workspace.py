"""Interactive board workspace for BoardComposer Studio."""

from __future__ import annotations

# pylint: disable=invalid-name,missing-function-docstring

from dataclasses import dataclass

from PySide6.QtCore import QPoint, QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QMouseEvent, QPainter, QPen, QWheelEvent
from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsSimpleTextItem,
    QGraphicsView,
)


@dataclass
class WorkspaceCamera:
    """Persistent camera state for the graphics workspace."""

    center: QPointF
    zoom: float = 1.0
    min_zoom: float = 0.15
    max_zoom: float = 8.0

    def clamp_zoom(self, value: float) -> float:
        return max(self.min_zoom, min(self.max_zoom, value))

    def zoom_factor(self, wheel_delta: int) -> float:
        return 1.12 if wheel_delta > 0 else 1 / 1.12


class BoardPieceItem(QGraphicsRectItem):
    """Interactive graphics item representing a board piece."""

    def __init__(
        self,
        piece_id: str,
        x_mm: float,
        y_mm: float,
        length_mm: float,
        width_mm: float,
    ):
        super().__init__(0, 0, length_mm, width_mm)

        self.piece_id = piece_id
        self.setPos(x_mm, y_mm)
        self.setBrush(QColor("#dbeafe"))
        self.setPen(QPen(QColor("#1d4ed8"), 3))
        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable
            | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
        )

        label = QGraphicsSimpleTextItem(piece_id, self)
        label.setFont(QFont("Arial", 40))
        label.setBrush(QColor("#1e3a8a"))
        label.setPos(24, 20)

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            new_pos = value
            rect = self.rect()

            min_x = 0
            min_y = 0
            max_x = 3000 - rect.width()
            max_y = 1000 - rect.height()

            x = min(max(new_pos.x(), min_x), max_x)
            y = min(max(new_pos.y(), min_y), max_y)

            return QPointF(x, y)

        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            if self.scene() and self.scene().views():
                self.scene().views()[0].piece_moved(
                    self.piece_id,
                    value.x(),
                    value.y(),
                )
        return super().itemChange(change, value)


class BoardWorkspace(QGraphicsView):
    """Graphics workspace used to display boards and placements."""

    def __init__(self, services):
        super().__init__()

        self.services = services
        self._scene = QGraphicsScene(self)
        self._camera = WorkspaceCamera(center=QPointF(1500, 500))
        self._panning = False
        self._last_pan_point = QPoint()
        self._board_item: QGraphicsRectItem | None = None
        self._piece_items: list[BoardPieceItem] = []
        self._initial_fit_done = False

        self.setScene(self._scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        self.setCursor(Qt.CursorShape.OpenHandCursor)

    def reload_project(self) -> None:
        self._scene.clear()
        self._piece_items.clear()
        self._board_item = None
        self._scene.setSceneRect(QRectF(-5000, -5000, 13000, 11000))

        self._add_grid()
        self._add_board()
        self._add_pieces()
        self.fit_board()

    def _add_grid(self) -> None:
        grid_pen = QPen(QColor("#e5e7eb"), 1)
        grid_size = 100
        scene_rect = self._scene.sceneRect()

        left = int(scene_rect.left())
        right = int(scene_rect.right())
        top = int(scene_rect.top())
        bottom = int(scene_rect.bottom())

        for x_value in range(left, right + 1, grid_size):
            self._scene.addLine(x_value, top, x_value, bottom, grid_pen)

        for y_value in range(top, bottom + 1, grid_size):
            self._scene.addLine(left, y_value, right, y_value, grid_pen)

    def _add_board(self) -> None:
        project = self.services.projects.current_project

        if project is None or not project.boards:
            return

        board_model = project.boards[0]
        board = QGraphicsRectItem(
            0,
            0,
            board_model.length_mm,
            board_model.width_mm,
        )
        board.setBrush(QColor("#f8fafc"))
        board.setPen(QPen(QColor("#111827"), 4))
        self._scene.addItem(board)
        self._board_item = board
        self._camera.center = board.sceneBoundingRect().center()

    def _add_pieces(self) -> None:
        project = self.services.projects.current_project

        if project is None:
            return

        for placement in project.placements:
            piece = project.piece_by_id(placement.piece_id)
            item = BoardPieceItem(
                piece.piece_id,
                placement.x_mm,
                placement.y_mm,
                piece.length_mm,
                piece.width_mm,
            )
            self._scene.addItem(item)
            self._piece_items.append(item)

    def select_piece(self, piece_id: str) -> None:
        self._scene.clearSelection()

        for item in self._piece_items:
            is_selected = item.piece_id == piece_id
            item.setSelected(is_selected)

            if is_selected:
                item.setBrush(QColor("#bfdbfe"))
                item.setPen(QPen(QColor("#dc2626"), 10))
                # self.centerOn(item.sceneBoundingRect().center())
            else:
                item.setBrush(QColor("#dbeafe"))
                item.setPen(QPen(QColor("#1d4ed8"), 3))

    def fit_board(self) -> None:
        if self._board_item is None:
            return

        viewport_rect = self.viewport().rect()
        board_rect = self._board_item.sceneBoundingRect()

        if viewport_rect.width() <= 0 or viewport_rect.height() <= 0:
            return

        x_zoom = viewport_rect.width() / board_rect.width()
        y_zoom = viewport_rect.height() / board_rect.height()
        self._camera.zoom = self._camera.clamp_zoom(min(x_zoom, y_zoom) * 0.75)
        self._camera.center = board_rect.center()
        self._apply_camera()

    def wheelEvent(self, event: QWheelEvent) -> None:
        mouse_scene_before = self.mapToScene(event.position().toPoint())
        factor = self._camera.zoom_factor(event.angleDelta().y())
        self._camera.zoom = self._camera.clamp_zoom(self._camera.zoom * factor)
        self._apply_camera()

        mouse_scene_after = self.mapToScene(event.position().toPoint())
        self._camera.center += mouse_scene_before - mouse_scene_after
        self._apply_camera()
        event.accept()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        clicked_item = self.itemAt(event.position().toPoint())

        if event.button() == Qt.MouseButton.RightButton or clicked_item is None:
            self._start_pan(event.position().toPoint())
            event.accept()
            return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._panning:
            current_position = event.position().toPoint()
            delta = current_position - self._last_pan_point
            self._last_pan_point = current_position

            self._camera.center -= QPointF(
                delta.x() / self._camera.zoom,
                delta.y() / self._camera.zoom,
            )
            self._apply_camera()
            event.accept()
            return

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self._panning:
            self._end_pan()
            event.accept()
            return

        self.services.projects.mark_modified()
        window = self.window()
        if hasattr(window, "_update_window_title"):
            window._update_window_title()
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        self.fit_board()
        event.accept()

    def _start_pan(self, point: QPoint) -> None:
        self._panning = True
        self._last_pan_point = point
        self.setCursor(Qt.CursorShape.ClosedHandCursor)

    def _end_pan(self) -> None:
        self._panning = False
        self.setCursor(Qt.CursorShape.OpenHandCursor)

    def _apply_camera(self) -> None:
        self.resetTransform()
        self.scale(self._camera.zoom, self._camera.zoom)
        self.centerOn(self._camera.center)

    def piece_moved(self, piece_id: str, x: float, y: float):
        project = self.services.projects.current_project

        if project is None:
            return

        placement = project.placement_by_piece_id(piece_id)
        if placement is not None:
            placement.x_mm = x
            placement.y_mm = y

        self.services.selection.select_one(piece_id)

        window = self.window()
        if hasattr(window, "refresh_inspector_for_piece"):
            window.refresh_inspector_for_piece(piece_id)

        self.viewport().update()
