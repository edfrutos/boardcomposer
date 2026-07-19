"""Interactive board workspace for BoardComposer Studio."""

# pylint: disable=invalid-name,too-many-instance-attributes
from __future__ import annotations

from typing import TYPE_CHECKING, cast

from PySide6.QtCore import QPoint, QPointF, QRectF, Qt, Signal
from PySide6.QtGui import QKeyEvent, QMouseEvent, QPainter, QResizeEvent, QWheelEvent
from PySide6.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
)

from studio.commands import MovePieceCommand
from studio.i18n import DEFAULT_LANGUAGE
from studio.workspace.board_item import create_board_item
from studio.workspace.board_piece_item import BoardPieceItem
from studio.workspace.drag_controller import DragController
from studio.workspace.empty_overlay import EmptyWorkspaceOverlay
from studio.workspace.grid import add_grid
from studio.workspace.panel_layout import PanelSlot, arrange_panel_slots, slot_at_point
from studio.workspace.piece_factory import create_piece_item
from studio.workspace.placement_validator import PlacementValidator
from studio.workspace.selection_controller import SelectionController
from studio.workspace.workspace_camera import WorkspaceCamera

if TYPE_CHECKING:
    from studio.main_window import MainWindow


class BoardWorkspace(QGraphicsView):
    """Interactive board workspace for BoardComposer Studio."""

    add_board_requested = Signal()
    add_piece_requested = Signal()
    import_boards_requested = Signal()
    import_pieces_requested = Signal()
    camera_changed = Signal(float)

    def __init__(self, services):
        super().__init__()

        self.services = services
        self._scene = QGraphicsScene(self)
        self._camera = WorkspaceCamera(center=QPointF(1500, 500))
        self._panning = False
        self._space_held = False
        self._last_pan_point = QPoint()
        self._board_item: QGraphicsRectItem | None = None
        self._board_items: dict[tuple[int, int], QGraphicsRectItem] = {}
        self._panel_slots: dict[tuple[int, int], PanelSlot] = {}
        self._validators: dict[tuple[int, int], PlacementValidator] = {}
        self._piece_items: list[BoardPieceItem] = []
        self._focused_board_id: str | None = None
        self.selection = SelectionController(services)
        self._drag = DragController()
        self._drag_start: tuple[str, float, float] | None = None
        self._language = DEFAULT_LANGUAGE

        self.setScene(self._scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        self._apply_canvas_background()

        self.empty_overlay = EmptyWorkspaceOverlay(self)
        self.empty_overlay.add_board_requested.connect(self.add_board_requested.emit)
        self.empty_overlay.add_piece_requested.connect(self.add_piece_requested.emit)
        self.empty_overlay.import_boards_requested.connect(
            self.import_boards_requested.emit
        )
        self.empty_overlay.import_pieces_requested.connect(
            self.import_pieces_requested.emit
        )
        self.empty_overlay.hide()

    def _apply_canvas_background(self) -> None:
        from studio.workspace.canvas_style import color

        self.setBackgroundBrush(color("background"))
        self._scene.setBackgroundBrush(color("background"))

    def reload_project(self, *, fit: bool = True) -> None:
        """Reload the project.

        When ``fit`` is False, preserve the current camera (e.g. grid toggle).
        """
        self._apply_canvas_background()
        self._scene.clear()
        self._piece_items.clear()
        self._board_item = None
        self._board_items.clear()
        self._panel_slots.clear()
        self._validators.clear()
        self._focused_board_id = None
        self._scene.setSceneRect(QRectF(-5000, -5000, 13000, 11000))

        preferences = getattr(self.services, "preferences", None)
        if preferences is None or preferences.current.show_grid:
            grid_size = (
                preferences.current.grid_size_mm if preferences is not None else 100
            )
            add_grid(self._scene, grid_size=grid_size)
        self._add_board()
        self._add_pieces()
        if fit:
            self.fit_board()
        else:
            self._apply_camera()
        self._refresh_empty_overlay()

    def _add_board(self) -> None:
        project = self.services.projects.current_project
        if project is None or not project.boards:
            return

        for slot in arrange_panel_slots(project.boards):
            board_model = project.boards[slot.stock_panel_index]
            board = create_board_item(board_model)
            board.setPos(slot.x_mm, slot.y_mm)
            self._scene.addItem(board)

            self._board_items[slot.key] = board
            self._panel_slots[slot.key] = slot
            self._validators[slot.key] = PlacementValidator(
                QRectF(
                    slot.x_mm,
                    slot.y_mm,
                    slot.length_mm,
                    slot.width_mm,
                )
            )

        if self._board_items:
            self._board_item = next(iter(self._board_items.values()))
            self._camera.center = self._all_boards_rect().center()

    def _add_pieces(self) -> None:
        project = self.services.projects.current_project
        if project is None:
            return

        for placement in project.placements:
            piece = project.piece_by_id(placement.piece_id)
            slot = self._slot_for_placement(placement)
            item = create_piece_item(
                piece,
                placement,
                offset_x=slot.x_mm if slot is not None else 0,
                offset_y=slot.y_mm if slot is not None else 0,
            )
            if slot is not None:
                item.stock_panel_index = slot.stock_panel_index
                item.board_id = slot.board_id
                item.board_instance = slot.instance_index
            self._scene.addItem(item)
            self._piece_items.append(item)

        self.selection.bind_items(self._piece_items)

    def preview_solution(self, solution, *, reveal_count: int | None = None) -> None:
        """Preview the solution.

        When ``reveal_count`` is set, only the first N placements are shown
        (pieces that belong to the solution but are not yet revealed are hidden).
        ``None`` shows every placement (default behaviour).
        """
        project = self.services.projects.current_project
        if project is None:
            return

        all_placements = solution.placements
        solution_ids = {placement.board_id for placement in all_placements}
        if reveal_count is None:
            revealed_ids = solution_ids
        else:
            count = max(0, min(reveal_count, len(all_placements)))
            revealed_ids = {placement.board_id for placement in all_placements[:count]}

        placements_by_piece_id = {
            placement.board_id: placement for placement in all_placements
        }

        for item in self._piece_items:
            if item.piece_id in solution_ids:
                item.setVisible(item.piece_id in revealed_ids)

            placement = placements_by_piece_id.get(item.piece_id)
            if placement is None:
                continue
            if item.piece_id not in revealed_ids:
                continue

            slot = None
            if placement.panel_reference is not None:
                panel_index = placement.panel_reference.stock_panel_index
                if panel_index < len(project.boards):
                    board_id = project.boards[panel_index].board_id
                    item.stock_panel_index = panel_index
                    item.board_id = board_id
                    item.board_instance = placement.panel_reference.instance_index
                    slot = self._panel_slots.get(
                        (panel_index, placement.panel_reference.instance_index)
                    )

            item.setPos(
                placement.x_mm + (slot.x_mm if slot is not None else 0),
                placement.y_mm + (slot.y_mm if slot is not None else 0),
            )
            item.set_rotation(90 if placement.rotated else 0)

    def constrain_piece_position(
        self, item: BoardPieceItem, new_pos: QPointF
    ) -> QPointF:
        """Constrain the piece position, reassigning it to whichever
        physical panel the drag is currently hovering over (DT-0003)."""
        center = QPointF(
            new_pos.x() + item.rect().width() / 2,
            new_pos.y() + item.rect().height() / 2,
        )
        candidate_slot = self._slot_at_point(center)
        if candidate_slot is not None:
            self._assign_item_to_slot(item, candidate_slot)

        key = self._panel_key(item)
        validator = self._validators.get(key) if key is not None else None
        if validator is None:
            return new_pos

        return validator.constrain_position(item, new_pos)

    def _slot_at_point(self, scene_pos: QPointF) -> PanelSlot | None:
        """Return the panel slot under `scene_pos`, if any."""
        return slot_at_point(
            list(self._panel_slots.values()),
            scene_pos.x(),
            scene_pos.y(),
        )

    def _assign_item_to_slot(self, item: BoardPieceItem, slot: PanelSlot) -> None:
        """Reassign `item` to the physical panel described by `slot`."""
        item.stock_panel_index = slot.stock_panel_index
        item.board_id = slot.board_id
        item.board_instance = slot.instance_index

    def _revert_item_to_panel(
        self,
        item: BoardPieceItem,
        old_x: float,
        old_y: float,
        old_board_id: str | None,
        old_board_instance: int,
        old_stock_panel_index: int | None,
    ) -> None:
        """Restore `item` to its pre-drag panel and local position, used
        when a drop lands on an invalid (occupied or out-of-bounds) spot."""
        item.board_id = old_board_id
        item.board_instance = old_board_instance
        item.stock_panel_index = old_stock_panel_index

        old_key = (
            (old_stock_panel_index, old_board_instance)
            if old_stock_panel_index is not None
            else None
        )
        old_slot = self._panel_slots.get(old_key) if old_key is not None else None
        item.setPos(
            old_x + (old_slot.x_mm if old_slot is not None else 0),
            old_y + (old_slot.y_mm if old_slot is not None else 0),
        )

    def retranslate(self, language: str) -> None:
        """Refresh empty-state strings for the selected language."""
        self._language = language
        self.empty_overlay.apply_language(language)

    def _project_is_empty(self) -> bool:
        project = self.services.projects.current_project
        return project is not None and not project.boards and not project.pieces

    def _refresh_empty_overlay(self) -> None:
        visible = self._project_is_empty()
        self.empty_overlay.setVisible(visible)
        if visible:
            self._position_empty_overlay()

    def _position_empty_overlay(self) -> None:
        overlay = self.empty_overlay
        overlay.adjustSize()
        hint = overlay.sizeHint()
        overlay.resize(max(hint.width(), 320), hint.height())
        geo = self.viewport().rect()
        overlay.move(
            geo.center().x() - overlay.width() // 2,
            max(16, geo.center().y() - overlay.height() // 2),
        )

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Keep the empty-state overlay centered on resize."""
        super().resizeEvent(event)
        if self.empty_overlay.isVisible():
            self._position_empty_overlay()

    def select_piece(self, piece_id: str) -> None:
        """Select the piece."""
        self.clear_board_focus()
        self.selection.select(piece_id)
        self.selection.sync_inspector(self.window())

    def select_all_pieces(self) -> None:
        """Select every piece on the canvas."""
        self.clear_board_focus()
        self.selection.select_all()
        self.selection.sync_inspector(self.window())

    def clear_piece_selection(self) -> None:
        """Clear the canvas piece selection."""
        self.clear_board_focus()
        self.selection.clear()
        self.selection.sync_inspector(self.window())

    def invert_piece_selection(self) -> None:
        """Invert the current piece selection on the canvas."""
        self.clear_board_focus()
        self.selection.invert_selection()
        self.selection.sync_inspector(self.window())

    def focused_board_id(self) -> str | None:
        """Return the board id currently highlighted from the Explorador."""
        return self._focused_board_id

    def clear_board_focus(self) -> None:
        """Remove board highlight from the canvas."""
        if self._focused_board_id is None:
            return
        self._focused_board_id = None
        self._apply_board_highlights()

    def focus_board(self, board_id: str) -> None:
        """Highlight panels for ``board_id`` and center the camera on them."""
        self._focused_board_id = board_id
        self._apply_board_highlights()
        self._center_on_board(board_id)

    def select_board_at(self, x_mm: float, y_mm: float) -> bool:
        """Focus the board under a scene point; return True if a panel was hit."""
        slot = slot_at_point(list(self._panel_slots.values()), x_mm, y_mm)
        if slot is None:
            return False
        window = self.window()
        if hasattr(window, "select_explorer_board"):
            window.select_explorer_board(slot.board_id)
        else:
            self.clear_piece_selection()
            self.focus_board(slot.board_id)
        return True

    def _apply_board_highlights(self) -> None:
        from studio.workspace.canvas_style import pen

        for key, item in self._board_items.items():
            slot = self._panel_slots[key]
            if (
                self._focused_board_id is not None
                and slot.board_id == self._focused_board_id
            ):
                item.setPen(pen("selected_stroke", 8))
            else:
                item.setPen(pen("board_stroke", 4))

    def _center_on_board(self, board_id: str) -> None:
        rect = QRectF()
        for key, slot in self._panel_slots.items():
            if slot.board_id != board_id:
                continue
            board_rect = self._board_items[key].sceneBoundingRect()
            rect = board_rect if rect.isNull() else rect.united(board_rect)
        if rect.isNull():
            return
        self._camera.center = rect.center()
        self._apply_camera()

    def fit_board(self) -> None:
        """Fit the board to the viewport."""
        if not self._board_items:
            return

        viewport_rect = self.viewport().rect()
        board_rect = self._all_boards_rect()

        if viewport_rect.width() <= 0 or viewport_rect.height() <= 0:
            return

        x_zoom = viewport_rect.width() / board_rect.width()
        y_zoom = viewport_rect.height() / board_rect.height()
        self._camera.zoom = self._camera.clamp_zoom(min(x_zoom, y_zoom) * 0.75)
        self._camera.center = board_rect.center()
        self._apply_camera()

    def zoom_in(self) -> None:
        """Zoom in around the current camera center."""
        self._zoom_by_steps(1)

    def zoom_out(self) -> None:
        """Zoom out around the current camera center."""
        self._zoom_by_steps(-1)

    def _zoom_by_steps(self, direction: int) -> None:
        factor = self._camera.zoom_factor(direction)
        self._camera.zoom = self._camera.clamp_zoom(self._camera.zoom * factor)
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
        button = event.button()

        # Middle / right / Space+left: pan (even over a piece — never start a drag).
        if button in (Qt.MouseButton.MiddleButton, Qt.MouseButton.RightButton) or (
            button == Qt.MouseButton.LeftButton and self._space_held
        ):
            self._start_pan(event.position().toPoint())
            event.accept()
            return

        if isinstance(clicked_item, BoardPieceItem):
            old_x, old_y = self._local_item_position(clicked_item)
            self._drag.begin(
                clicked_item.piece_id,
                old_x,
                old_y,
                clicked_item.board_id,
                clicked_item.board_instance,
                clicked_item.stock_panel_index,
            )
            self.select_piece(clicked_item.piece_id)
        elif button == Qt.MouseButton.LeftButton:
            scene_pos = self.mapToScene(event.position().toPoint())
            if not self.select_board_at(scene_pos.x(), scene_pos.y()):
                # Empty canvas / gap between panels: clear selection.
                self.clear_piece_selection()

        if clicked_item is None:
            self._start_pan(event.position().toPoint())
            event.accept()
            return

        super().mousePressEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Arm temporary pan mode while Space is held."""
        if event.key() == Qt.Key.Key_Space and not event.isAutoRepeat():
            self._space_held = True
            event.accept()
            return
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        """Disarm temporary pan mode when Space is released."""
        if event.key() == Qt.Key.Key_Space and not event.isAutoRepeat():
            self._space_held = False
            event.accept()
            return
        super().keyReleaseEvent(event)

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

            key = self._panel_key(item)
            validator = self._validators.get(key) if key is not None else None
            if validator is not None and not validator.can_place(item):
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

        (
            piece_id,
            old_x,
            old_y,
            old_board_id,
            old_board_instance,
            old_stock_panel_index,
        ) = drag

        item = self.piece_item_by_id(piece_id)
        if item is None:
            return

        key = self._panel_key(item)
        validator = self._validators.get(key) if key is not None else None
        if validator is not None and not validator.can_place(item):
            self._revert_item_to_panel(
                item,
                old_x,
                old_y,
                old_board_id,
                old_board_instance,
                old_stock_panel_index,
            )
            item.set_normal()
            return

        project = self.services.projects.current_project
        placement = project.placement_by_piece_id(piece_id) if project else None
        if placement is None:
            return

        panel_unchanged = (
            placement.board_id == old_board_id
            and placement.board_instance == old_board_instance
            and placement.stock_panel_index == old_stock_panel_index
        )
        if placement.x_mm == old_x and placement.y_mm == old_y and panel_unchanged:
            return

        command = MovePieceCommand(
            self.services,
            piece_id,
            old_x,
            old_y,
            placement.x_mm,
            placement.y_mm,
            old_board_id=old_board_id,
            old_board_instance=old_board_instance,
            old_stock_panel_index=old_stock_panel_index,
            new_board_id=placement.board_id,
            new_board_instance=placement.board_instance,
            new_stock_panel_index=placement.stock_panel_index,
        )

        self.services.commands.execute(command)

        window = cast("MainWindow", self.window())
        if hasattr(window, "_mark_project_modified"):
            window._mark_project_modified(reason="piece_moved")
        else:
            self.services.mark_project_modified(reason="piece_moved")

        if hasattr(window, "update_undo_redo"):
            window.update_undo_redo()
        if hasattr(window, "update_window_title"):
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
        key = self._panel_key(item)
        validator = self._validators.get(key) if key is not None else None
        if validator is None:
            return False

        return validator.can_rotate(item, angle)

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
        self.camera_changed.emit(self._camera.zoom)

    @property
    def zoom(self) -> float:
        """Current Workspace camera zoom factor (1.0 = 100%)."""
        return self._camera.zoom

    def piece_moved(self, piece_id: str, x: float, y: float) -> None:
        """Piece moved event."""
        project = self.services.projects.current_project
        if project is None:
            return

        placement = project.placement_by_piece_id(piece_id)
        if placement is not None:
            item = self.piece_item_by_id(piece_id)
            key = self._panel_key(item) if item is not None else None
            slot = self._panel_slots.get(key) if key is not None else None
            placement.x_mm = x - (slot.x_mm if slot is not None else 0)
            placement.y_mm = y - (slot.y_mm if slot is not None else 0)
            if item is not None:
                placement.board_id = item.board_id
                placement.board_instance = item.board_instance
                placement.stock_panel_index = item.stock_panel_index

        self.selection.select(piece_id)

        window = self.window()
        self.selection.sync_inspector(window)

        self.viewport().update()

    def _slot_for_placement(self, placement) -> PanelSlot | None:
        key = (
            (placement.stock_panel_index, placement.board_instance)
            if placement.stock_panel_index is not None
            else None
        )
        slot = self._panel_slots.get(key) if key is not None else None
        if slot is not None:
            return slot
        if placement.board_id is not None:
            for candidate in self._panel_slots.values():
                if (
                    candidate.board_id == placement.board_id
                    and candidate.instance_index == placement.board_instance
                ):
                    return candidate
        return next(iter(self._panel_slots.values()), None)

    def _local_item_position(self, item: BoardPieceItem) -> tuple[float, float]:
        key = self._panel_key(item)
        slot = self._panel_slots.get(key) if key is not None else None
        return (
            item.pos().x() - (slot.x_mm if slot is not None else 0),
            item.pos().y() - (slot.y_mm if slot is not None else 0),
        )

    @staticmethod
    def _panel_key(item: BoardPieceItem) -> tuple[int, int] | None:
        if item.stock_panel_index is None:
            return None
        return item.stock_panel_index, item.board_instance

    def _all_boards_rect(self) -> QRectF:
        rect = QRectF()
        for board in self._board_items.values():
            board_rect = board.sceneBoundingRect()
            rect = board_rect if rect.isNull() else rect.united(board_rect)
        return rect
