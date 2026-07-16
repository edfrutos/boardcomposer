"""Pure layout helpers for displaying physical stock panels in Studio."""

from dataclasses import dataclass

from studio.models import StudioBoard


@dataclass(frozen=True)
class PanelSlot:
    """Scene position and dimensions of one physical panel."""

    stock_panel_index: int
    board_id: str
    instance_index: int
    x_mm: float
    y_mm: float
    length_mm: float
    width_mm: float

    @property
    def key(self) -> tuple[int, int]:
        return self.stock_panel_index, self.instance_index


def slot_at_point(slots: list[PanelSlot], x_mm: float, y_mm: float) -> PanelSlot | None:
    """Return the panel slot whose scene bounds contain `(x_mm, y_mm)`, if any."""
    for slot in slots:
        if (
            slot.x_mm <= x_mm <= slot.x_mm + slot.length_mm
            and slot.y_mm <= y_mm <= slot.y_mm + slot.width_mm
        ):
            return slot
    return None


def arrange_panel_slots(
    boards: list[StudioBoard],
    *,
    gap_mm: float = 200,
) -> list[PanelSlot]:
    """Arrange every physical panel from left to right in scene coordinates."""
    slots: list[PanelSlot] = []
    x_mm = 0.0

    for stock_panel_index, board in enumerate(boards):
        for instance_index in range(board.quantity):
            slots.append(
                PanelSlot(
                    stock_panel_index=stock_panel_index,
                    board_id=board.board_id,
                    instance_index=instance_index,
                    x_mm=x_mm,
                    y_mm=0.0,
                    length_mm=board.length_mm,
                    width_mm=board.width_mm,
                )
            )
            x_mm += board.length_mm + gap_mm

    return slots
