"""Interactive board workspace for BoardComposer Studio."""

from __future__ import annotations

# pylint: disable=invalid-name,missing-function-docstring

from dataclasses import dataclass

from PySide6.QtCore import QPoint, QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsSimpleTextItem,
    QGraphicsView,
)

from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject


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

    def __init__(self, piece_id, x_mm, y_mm, length_mm, width_mm):
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


class BoardWorkspace(QGraphicsView):
    """Graphics workspace used to display boards and placements."""

    def __init__(self):
        super().__init__()
        self._scene = QGraphicsScene(self)
        self._camera = WorkspaceCamera(center=QPointF(1500, 500))
        self._panning = False
        self._last_pan_point = QPoint()
        self._board_item = None
        self._piece_items = []
        self._project = self._create_demo_project()
        self._initial_fit_done = False

        self.setScene(self._scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        self.setCursor(Qt.CursorShape.OpenHandCursor)

        self._build_scene()

    def showEvent(self, event):
        super().showEvent(event)
        if not self._initial_fit_done:
            self.fit_board()
            self._initial_fit_done = True

    def _build_scene(self):
        self._scene.setSceneRect(QRectF(-5000, -5000, 13000, 11000))
        self._add_grid()
        self._add_board()
        self._add_demo_pieces()

    def _add_grid(self):
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

    def _add_board(self):
        board = QGraphicsRectItem(0, 0, 3000, 1000)
        board.setBrush(QColor("#f8fafc"))
        board.setPen(QPen(QColor("#111827"), 4))
        self._scene.addItem(board)
        self._board_item = board
        self._camera.center = board.sceneBoundingRect().center()

    def _add_demo_pieces(self):
        for placement in self._project.placements:
            piece = self._project.piece_by_id(placement.piece_id)
            item = BoardPieceItem(
                piece.piece_id,
                placement.x_mm,
                placement.y_mm,
                piece.length_mm,
                piece.width_mm,
            )
            self._scene.addItem(item)
            self._piece_items.append(item)

    def _create_demo_project(self):
        return StudioProject(
            project_id="PRJ-DEMO-001",
            name="Proyecto demo",
            boards=[StudioBoard("TAB-001", 3000, 1000)],
            pieces=[
                StudioPiece("P-001", 700, 300),
                StudioPiece("P-002", 520, 360),
                StudioPiece("P-003", 820, 240),
            ],
            placements=[
                StudioPlacement("P-001", 120, 120),
                StudioPlacement("P-002", 900, 120),
                StudioPlacement("P-003", 1500, 120),
            ],
        )

    def fit_board(self):
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

    def wheelEvent(self, event):
        mouse_scene_before = self.mapToScene(event.position().toPoint())
        factor = self._camera.zoom_factor(event.angleDelta().y())
        self._camera.zoom = self._camera.clamp_zoom(self._camera.zoom * factor)
        self._apply_camera()
        mouse_scene_after = self.mapToScene(event.position().toPoint())
        self._camera.center += mouse_scene_before - mouse_scene_after
        self._apply_camera()
        event.accept()

    def mousePressEvent(self, event):
        clicked_item = self.itemAt(event.position().toPoint())
        if event.button() == Qt.MouseButton.RightButton or clicked_item is None:
            self._start_pan(event.position().toPoint())
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
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

    def mouseReleaseEvent(self, event):
        if self._panning:
            self._end_pan()
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.fit_board()
        event.accept()

    def _start_pan(self, point):
        self._panning = True
        self._last_pan_point = point
        self.setCursor(Qt.CursorShape.ClosedHandCursor)

    def _end_pan(self):
        self._panning = False
        self.setCursor(Qt.CursorShape.OpenHandCursor)

    def _apply_camera(self):
        self.resetTransform()
        self.scale(self._camera.zoom, self._camera.zoom)
        self.centerOn(self._camera.center)
