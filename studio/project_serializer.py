"""Project serialization helpers for BoardComposer Studio."""

from __future__ import annotations

import json
from pathlib import Path

from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject


def project_to_dict(project: StudioProject) -> dict:
    return {
        "version": 1,
        "project_id": project.project_id,
        "name": project.name,
        "boards": [
            {
                "board_id": board.board_id,
                "length_mm": board.length_mm,
                "width_mm": board.width_mm,
                "material": board.material,
            }
            for board in project.boards
        ],
        "pieces": [
            {
                "piece_id": piece.piece_id,
                "length_mm": piece.length_mm,
                "width_mm": piece.width_mm,
                "material": piece.material,
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
            }
            for placement in project.placements
        ],
    }


def project_from_dict(data: dict) -> StudioProject:
    return StudioProject(
        project_id=data["project_id"],
        name=data["name"],
        boards=[
            StudioBoard(
                board_id=item["board_id"],
                length_mm=item["length_mm"],
                width_mm=item["width_mm"],
                material=item.get("material", "Demo"),
            )
            for item in data.get("boards", [])
        ],
        pieces=[
            StudioPiece(
                piece_id=item["piece_id"],
                length_mm=item["length_mm"],
                width_mm=item["width_mm"],
                material=item.get("material", "Demo"),
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
