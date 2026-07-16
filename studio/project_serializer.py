"""Project serialization helpers for BoardComposer Studio.

Persisted `.bcproj` files carry an explicit `version` field. Loading a file
older than `CURRENT_VERSION` runs it through a chain of migration functions
(one per version step, see ADR-015) before building the in-memory model.
Files newer than `CURRENT_VERSION` are rejected explicitly rather than
silently truncated or guessed at.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject

CURRENT_VERSION = 2


class UnsupportedProjectVersionError(Exception):
    """Raised when a `.bcproj` file declares a version this build can't read."""

    def __init__(self, file_version: int) -> None:
        self.file_version = file_version
        super().__init__(
            f"El proyecto usa la versión {file_version}, pero esta versión de "
            f"BoardComposer solo admite hasta la versión {CURRENT_VERSION}. "
            "Actualiza la aplicación para abrir este archivo."
        )


def _migrate_v1_to_v2(data: dict) -> dict:
    """v1 -> v2: introduces per-board material/thickness/quantity, per-piece
    material/thickness, and per-placement physical-panel assignment
    (`board_id`, `board_instance`, `stock_panel_index`). Older files simply
    lack these keys, so migrating just means filling in their defaults
    explicitly (matching ADR-014's "Studio y persistencia" section).
    """
    migrated = dict(data)

    migrated["boards"] = [
        {
            "material": "Demo",
            "thickness_mm": 19,
            "quantity": 1,
            **board,
        }
        for board in data.get("boards", [])
    ]
    migrated["pieces"] = [
        {
            "material": "Demo",
            "thickness_mm": 19,
            **piece,
        }
        for piece in data.get("pieces", [])
    ]
    migrated["placements"] = [
        {
            "rotated": False,
            "rotation": 0,
            "board_id": None,
            "board_instance": 0,
            "stock_panel_index": None,
            **placement,
        }
        for placement in data.get("placements", [])
    ]
    migrated["version"] = 2

    return migrated


_MIGRATIONS: dict[int, Callable[[dict], dict]] = {
    1: _migrate_v1_to_v2,
}


def _migrate_to_current_version(data: dict) -> dict:
    file_version = data.get("version", 1)

    if file_version > CURRENT_VERSION:
        raise UnsupportedProjectVersionError(file_version)

    migrated = data
    version = file_version
    while version < CURRENT_VERSION:
        migration = _MIGRATIONS[version]
        migrated = migration(migrated)
        version += 1

    return migrated


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
    data = _migrate_to_current_version(data)

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


def save_project(project: StudioProject, path: str | Path) -> None:
    Path(path).write_text(
        json.dumps(project_to_dict(project), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def load_project(path: str | Path) -> StudioProject:
    return project_from_dict(json.loads(Path(path).read_text(encoding="utf-8")))
