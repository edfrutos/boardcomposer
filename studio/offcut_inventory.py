"""Map Core offcut remnants onto Studio inventory boards (IDE-0025)."""

from __future__ import annotations

from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.inventory.offcut_inventory import remnant_stock_from_offcuts
from studio.models import StudioBoard


def remnant_studio_boards(
    core_project: Project,
    solution: AssemblySolution,
    existing_ids: set[str],
) -> list[StudioBoard]:
    """Studio remnant boards not already present (case-insensitive ids)."""
    taken = {item.casefold() for item in existing_ids}
    boards: list[StudioBoard] = []
    for panel in remnant_stock_from_offcuts(core_project, solution):
        board_id = panel.id
        if not board_id or board_id.casefold() in taken:
            continue
        boards.append(
            StudioBoard(
                board_id=board_id,
                length_mm=panel.length_mm,
                width_mm=panel.width_mm,
                material=panel.material,
                thickness_mm=panel.thickness_mm,
                quantity=panel.quantity,
                remnant=True,
            )
        )
        taken.add(board_id.casefold())
    return boards
