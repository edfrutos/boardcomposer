"""Preview thumbnails for Studio project files (SCR-001)."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap

from boardcomposer import (
    AssemblySolution,
    Board,
    BoardPlacement,
    Project,
    ProjectConstraints,
    StockPanel,
)
from boardcomposer.domain import PanelReference
from boardcomposer.export import solution_to_svg

from studio.models import StudioProject
from studio.project_serializer import load_project
from studio.solution_thumbnail import svg_to_pixmap

RECENT_THUMBNAIL_SIZE = QSize(120, 72)
_PANEL_LABEL_MARGIN = 30
_PANEL_GAP = 50


def studio_to_core_project(studio: StudioProject) -> Project:
    """Convert a Studio project into a Core `Project` for SVG export."""
    source_board = studio.boards[0] if studio.boards else None
    constraints = ProjectConstraints(
        allow_rotation=True,
        allow_cutting=False,
    )
    if source_board is not None:
        constraints = ProjectConstraints(
            max_length_mm=source_board.length_mm,
            max_width_mm=source_board.width_mm,
            allow_rotation=True,
            allow_cutting=False,
        )

    core = Project(constraints=constraints)
    for board in studio.boards:
        core.add_stock_panel(
            StockPanel(
                id=board.board_id,
                length_mm=board.length_mm,
                width_mm=board.width_mm,
                thickness_mm=board.thickness_mm,
                quantity=board.quantity,
                material=board.material,
            )
        )
    for piece in studio.pieces:
        core.add_board(
            Board(
                id=piece.piece_id,
                length_mm=piece.length_mm,
                width_mm=piece.width_mm,
                thickness_mm=piece.thickness_mm,
                material=piece.material,
            )
        )
    return core


def studio_to_assembly_solution(studio: StudioProject) -> AssemblySolution:
    """Rebuild an `AssemblySolution` from Studio placements."""
    pieces_by_id = {piece.piece_id: piece for piece in studio.pieces}
    board_index = {board.board_id: index for index, board in enumerate(studio.boards)}
    placements: list[BoardPlacement] = []

    for studio_placement in studio.placements:
        piece = pieces_by_id.get(studio_placement.piece_id)
        if piece is None:
            continue

        if studio_placement.rotated:
            length_mm = piece.width_mm
            width_mm = piece.length_mm
        else:
            length_mm = piece.length_mm
            width_mm = piece.width_mm

        stock_index = studio_placement.stock_panel_index
        if stock_index is None and studio_placement.board_id is not None:
            stock_index = board_index.get(studio_placement.board_id)

        panel_reference = None
        if stock_index is not None:
            panel_reference = PanelReference(
                stock_index,
                studio_placement.board_instance,
            )

        placements.append(
            BoardPlacement(
                studio_placement.piece_id,
                studio_placement.x_mm,
                studio_placement.y_mm,
                length_mm,
                width_mm,
                studio_placement.rotated,
                panel_reference,
            )
        )

    return AssemblySolution(placements=placements)


def _boards_only_svg(studio: StudioProject) -> str:
    """Draw empty stock panels when the project has no placements yet."""
    next_x = 0.0
    max_height = 0.0
    parts: list[str] = []

    for board in studio.boards:
        y = _PANEL_LABEL_MARGIN
        parts.append(
            f'<rect x="{next_x:g}" y="{y:g}" width="{board.length_mm:g}" '
            f'height="{board.width_mm:g}" fill="none" stroke="#64748b" />'
        )
        label = board.board_id
        if board.quantity > 1:
            label = f"{label} ×{board.quantity}"
        parts.append(
            f'<text x="{next_x + 5:g}" y="{y - 10:g}" font-size="16">{label}</text>'
        )
        next_x += board.length_mm + _PANEL_GAP
        max_height = max(max_height, board.width_mm)

    width = max(1.0, next_x - _PANEL_GAP)
    height = max(1.0, max_height + _PANEL_LABEL_MARGIN)
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:g}" '
            f'height="{height:g}" viewBox="0 0 {width:g} {height:g}">',
            *parts,
            "</svg>",
        ]
    )


def studio_project_to_svg(studio: StudioProject) -> str | None:
    """Return an SVG preview of the project layout, or `None` if empty."""
    if not studio.boards and not studio.placements:
        return None

    solution = studio_to_assembly_solution(studio)
    if solution.placements:
        core = studio_to_core_project(studio)
        project = core if solution.panel_references else None
        return solution_to_svg(solution, project)

    if studio.boards:
        return _boards_only_svg(studio)

    return None


def project_file_thumbnail(
    path: str | Path,
    *,
    box: QSize = RECENT_THUMBNAIL_SIZE,
) -> QPixmap | None:
    """Load a `.bcproj` and rasterize a layout thumbnail, or `None` on failure."""
    try:
        studio = load_project(path)
    except Exception:
        return None

    svg = studio_project_to_svg(studio)
    if svg is None:
        return None

    return svg_to_pixmap(svg, box=box)
