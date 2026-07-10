"""Interactive board workspace for BoardComposer Studio."""

# pylint: disable=invalid-name,too-many-instance-attributes
from __future__ import annotations

from typing import TYPE_CHECKING, cast

from PySide6.QtCore import QPoint, QPointF, QRectF, Qt
from PySide6.QtGui import QMouseEvent, QPainter, QWheelEvent
from PySide6.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
)

from studio.commands import MovePieceCommand
from studio.workspace.board_item import create_board_item
from studio.workspace.board_piece_item import BoardPieceItem
from studio.workspace.drag_controller import DragController
from studio.workspace.grid import add_grid
from studio.workspace.piece_factory import create_piece_item
from studio.workspace.placement_validator import PlacementValidator
from studio.workspace.selection_controller import SelectionController
from studio.workspace.workspace_camera import WorkspaceCamera

if TYPE_CHECKING:
    from studio.main_window import MainWindow


class BoardWorkspace(QGraphicsView):
    """Interactive board workspace for BoardComposer Studio."""

    def __init__(self, services):
        super().__init__()
        self._validator = None

        self.services = services
        self._scene = QGraphicsScene(self)
        self._camera = WorkspaceCamera(center=QPointF(1500, 500))
        self._panning = False
        self._last_pan_point = QPoint()
        self._board_item: QGraphicsRectItem | None = None
        self._piece_items: list[BoardPieceItem] = []
        self.selection = SelectionController(services)
        self._drag = DragController()
        self._drag_start: tuple[str, float, float] | None = None

        self.setScene(self._scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        self.setCursor(Qt.CursorShape.OpenHandCursor)

    def reload_project(self) -> None:
        """Reload the project."""
        self._scene.clear()
        self._piece_items.clear()
        self._board_item = None
        self._scene.setSceneRect(QRectF(-5000, -5000, 13000, 11000))

        add_grid(self._scene)
        self._add_board()
        self._add_pieces()
        self.fit_board()

    def _add_board(self) -> None:
        project = self.services.projects.current_project
        if project is None or not project.boards:
            return

        board_model = project.boards[0]
        board = create_board_item(board_model)

        self._scene.addItem(board)
        self._board_item = board
        self._validator = PlacementValidator(
            QRectF(
                0,
                0,
                board_model.length_mm,
                board_model.width_mm,
            )
        )

        self._camera.center = board.sceneBoundingRect().center()

    def _add_pieces(self) -> None:
        project = self.services.projects.current_project
        if project is None:
            return

        for placement in project.placements:
            piece = project.piece_by_id(placement.piece_id)
            item = create_piece_item(piece, placement)
            self._scene.addItem(item)
            self._piece_items.append(item)
            self.selection.bind_items(self._piece_items)
            self.selection.bind_items(self._piece_items)

    def preview_solution(self, solution) -> None:
        """Preview the solution."""
        project = self.services.projects.current_project
        if project is None:
            return

        placements_by_piece_id = {
            placement.board_id: placement for placement in solution.placements
        }

        for item in self._piece_items:
            placement = placements_by_piece_id.get(item.piece_id)
            if placement is None:
                continue

            item.setPos(placement.x_mm, placement.y_mm)
            item.set_rotation(90 if placement.rotated else 0)

    def constrain_piece_position(
        self, item: BoardPieceItem, new_pos: QPointF
    ) -> QPointF:
        """Constrain the piece position."""
        if self._validator is None:
            return new_pos

        return self._validator.constrain_position(item, new_pos)

    def select_piece(self, piece_id: str) -> None:
        """Select the piece."""
        self.selection.select(piece_id)
        self.selection.sync_inspector(self.window())

    def fit_board(self) -> None:
        """Fit the board to the viewport."""
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
        """Handle the wheel event."""
        mouse_scene_before = self.mapToScene(event.position().toPoint())
        factor = self._camera.zoom_factor(event.angleDelta().y())
        self._camera.zoom = self._camera.clamp_zoom(self._camera.zoom * factor)
        self._apply_camera()

        mouse_scene_after = self.mapToScene(event.position().toPoint())
        self._camera.center += mouse_scene_before - mouse_scene_after
        self._apply_camera()
        event.accept()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Handle the mouse press event."""
        clicked_item = self.itemAt(event.position().toPoint())

        if isinstance(clicked_item, BoardPieceItem):
            self._drag.begin(
                clicked_item.piece_id,
                clicked_item.pos().x(),
                clicked_item.pos().y(),
            )

        if event.button() == Qt.MouseButton.RightButton or clicked_item is None:
            self._start_pan(event.position().toPoint())
            event.accept()
            return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """Handle the mouse move event."""
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

        selected = self.scene().selectedItems()

        if len(selected) == 1 and isinstance(selected[0], BoardPieceItem):
            item = selected[0]

            if self._validator is not None and not self._validator.can_place(item):
                item.set_invalid()
            else:
                item.set_valid()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """Handle the mouse release event."""
        if self._panning:
            self._end_pan()
            event.accept()
            return

        super().mouseReleaseEvent(event)
        self._finish_piece_drag()

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        """Handle the mouse double click event."""
        self.fit_board()
        event.accept()

    def _finish_piece_drag(self) -> None:
        """Finish the piece drag."""
        drag = self._drag.clear()
        if drag is None:
            return

        piece_id, old_x, old_y = drag

        item = self.piece_item_by_id(piece_id)
        if item is None:
            return

        if self._validator is not None and not self._validator.can_place(item):
            item.setPos(old_x, old_y)
            item.set_normal()
            return

        project = self.services.projects.current_project
        placement = project.placement_by_piece_id(piece_id) if project else None
        if placement is None:
            return

        if placement.x_mm == old_x and placement.y_mm == old_y:
            return

        command = MovePieceCommand(
            self.services,
            piece_id,
            old_x,
            old_y,
            placement.x_mm,
            placement.y_mm,
        )

        self.services.commands.execute(command)
        self.services.projects.mark_modified()

        window = cast("MainWindow", self.window())
        window.update_undo_redo()
        window.update_window_title()

        item.set_normal()

    def piece_item_by_id(self, piece_id: str) -> BoardPieceItem | None:
        """Get the piece item by ID."""
        for item in self._piece_items:
            if item.piece_id == piece_id:
                return item
        return None

    def can_rotate_item(self, item: BoardPieceItem, angle: int) -> bool:
        """Can rotate the item."""
        if self._validator is None:
            return False

        return self._validator.can_rotate(item, angle)

    def _start_pan(self, point: QPoint) -> None:
        self._panning = True
        self._last_pan_point = point
        self.setCursor(Qt.CursorShape.ClosedHandCursor)

    def _end_pan(self) -> None:
        """End the pan."""
        self._panning = False
        self.setCursor(Qt.CursorShape.OpenHandCursor)

    def _apply_camera(self) -> None:
        """Apply the camera."""
        self.resetTransform()
        self.scale(self._camera.zoom, self._camera.zoom)
        self.centerOn(self._camera.center)

    def piece_moved(self, piece_id: str, x: float, y: float) -> None:
        """Piece moved event."""
        project = self.services.projects.current_project
        if project is None:
            return

        placement = project.placement_by_piece_id(piece_id)
        if placement is not None:
            placement.x_mm = x
            placement.y_mm = y

        self.selection.select(piece_id)

        window = self.window()
        self.selection.sync_inspector(window)

        self.viewport().update()
