"""Project serialization helpers for BoardComposer Studio.

Persisted `.bcproj` files carry an explicit `version` field. Loading a file
older than `CURRENT_VERSION` runs it through a chain of migration functions
(one per version step, see ADR-015) before building the in-memory model.
Files newer than `CURRENT_VERSION` are rejected explicitly rather than
silently truncated or guessed at.

Version migrations live in Core (`boardcomposer.io.bcproj`) so API `v1` and
Studio share one chain (EP-001 / SPR-003).
"""

from __future__ import annotations

import json
from pathlib import Path

from boardcomposer.io.bcproj import (
    CURRENT_VERSION,
    UnsupportedProjectVersionError,
    migrate_bcproj_dict,
)
from boardcomposer.io.bcproj_revisions import snapshot_before_overwrite
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject

__all__ = [
    "CURRENT_VERSION",
    "UnsupportedProjectVersionError",
    "load_project",
    "project_from_dict",
    "project_to_dict",
    "save_project",
]


def project_to_dict(project: StudioProject) -> dict:
    return {
        "version": CURRENT_VERSION,
        "project_id": project.project_id,
        "name": project.name,
        "boards": [
            {
                "board_id": board.board_id,
                "length_mm": board.length_mm,
                "width_mm": board.width_mm,
                "material": board.material,
                "thickness_mm": board.thickness_mm,
                "quantity": board.quantity,
            }
            for board in project.boards
        ],
        "pieces": [
            {
                "piece_id": piece.piece_id,
                "length_mm": piece.length_mm,
                "width_mm": piece.width_mm,
                "material": piece.material,
                "thickness_mm": piece.thickness_mm,
            }
            for piece in project.pieces
        ],
        "placements": [
            {
                "piece_id": placement.piece_id,
                "x_mm": placement.x_mm,
                "y_mm": placement.y_mm,
                "rotated": placement.rotated,
                "rotation": placement.rotation,
                "board_id": placement.board_id,
                "board_instance": placement.board_instance,
                "stock_panel_index": placement.stock_panel_index,
            }
            for placement in project.placements
        ],
    }


def project_from_dict(data: dict) -> StudioProject:
    data = migrate_bcproj_dict(data)

    return StudioProject(
        project_id=data["project_id"],
        name=data["name"],
        boards=[
            StudioBoard(
                board_id=item["board_id"],
                length_mm=item["length_mm"],
                width_mm=item["width_mm"],
                material=item.get("material", "Demo"),
                thickness_mm=item.get("thickness_mm", 19),
                quantity=item.get("quantity", 1),
            )
            for item in data.get("boards", [])
        ],
        pieces=[
            StudioPiece(
                piece_id=item["piece_id"],
                length_mm=item["length_mm"],
                width_mm=item["width_mm"],
                material=item.get("material", "Demo"),
                thickness_mm=item.get("thickness_mm", 19),
            )
            for item in data.get("pieces", [])
        ],
        placements=[
            StudioPlacement(
                piece_id=item["piece_id"],
                x_mm=item["x_mm"],
                y_mm=item["y_mm"],
                rotated=item.get("rotated", False),
                rotation=item.get("rotation", 0),
                board_id=item.get("board_id"),
                board_instance=item.get("board_instance", 0),
                stock_panel_index=item.get("stock_panel_index"),
            )
            for item in data.get("placements", [])
        ],
    )


def save_project(project: StudioProject, path: str | Path) -> Path | None:
    """Persist ``project`` to ``path``.

    Returns the path of the previous-revision snapshot when one was created
    (file already existed), otherwise ``None``.
    """
    target = Path(path)
    snapshot = snapshot_before_overwrite(target)
    target.write_text(
        json.dumps(project_to_dict(project), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return snapshot


def load_project(path: str | Path) -> StudioProject:
    return project_from_dict(json.loads(Path(path).read_text(encoding="utf-8")))
