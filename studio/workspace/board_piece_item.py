from PySide6.QtGui import QFont
from PySide6.QtWidgets import QGraphicsItem, QGraphicsRectItem, QGraphicsSimpleTextItem

from typing import TYPE_CHECKING, cast

from studio.workspace.canvas_style import color, pen

if TYPE_CHECKING:
    from studio.workspace.board_workspace import BoardWorkspace


class BoardPieceItem(QGraphicsRectItem):
    def __init__(
        self,
        piece_id: str,
        x_mm: float,
        y_mm: float,
        length_mm: float,
        width_mm: float,
        board_id: str | None = None,
        board_instance: int = 0,
        stock_panel_index: int | None = None,
    ):
        super().__init__(0, 0, length_mm, width_mm)

        self.piece_id = piece_id
        self.length_mm = length_mm
        self.width_mm = width_mm
        self.board_id = board_id
        self.board_instance = board_instance
        self.stock_panel_index = stock_panel_index
        self._label: QGraphicsSimpleTextItem | None = None

        self.setPos(x_mm, y_mm)

        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable
            | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
            | QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )

        label = QGraphicsSimpleTextItem(piece_id, self)
        label.setFont(QFont("Source Sans 3", 40))
        label.setPos(24, 20)
        self._label = label
        self.set_normal()

    def itemChange(self, change, value):
        scene = self.scene()
        views = scene.views() if scene is not None else []

        workspace = cast("BoardWorkspace", views[0]) if views else None

        if (
            change == QGraphicsItem.GraphicsItemChange.ItemPositionChange
            and workspace is not None
        ):
            return workspace.constrain_piece_position(self, value)

        if (
            change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged
            and workspace is not None
        ):
            workspace.piece_moved(
                self.piece_id,
                value.x(),
                value.y(),
            )

        return super().itemChange(change, value)

    def set_valid(self):
        self.setBrush(color("valid_fill"))
        self.setPen(pen("valid_stroke", 3))
        if self._label is not None:
            self._label.setBrush(color("piece_label"))

    def set_invalid(self):
        self.setBrush(color("invalid_fill"))
        self.setPen(pen("invalid_stroke", 3))
        if self._label is not None:
            self._label.setBrush(color("piece_label"))

    def set_normal(self):
        if self.isSelected():
            self.setBrush(color("selected_fill"))
            self.setPen(pen("selected_stroke", 10))
        else:
            self.setBrush(color("piece_fill"))
            self.setPen(pen("piece_stroke", 3))
        if self._label is not None:
            self._label.setBrush(color("piece_label"))

    def set_rotation(self, angle: int) -> None:
        angle = angle % 180

        if angle == 90:
            self.setRect(0, 0, self.width_mm, self.length_mm)
        else:
            self.setRect(0, 0, self.length_mm, self.width_mm)

        self.setTransformOriginPoint(self.rect().center())
        self.setRotation(0)
