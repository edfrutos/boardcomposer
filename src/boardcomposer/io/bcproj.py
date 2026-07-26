"""Load Studio ``.bcproj`` JSON into a Core ``Project`` (no Qt / studio.*).

Migrations match ADR-015 / Studio serializer semantics so CLI and API `v1`
can open the same files. Placements in the file are ignored for Core load:
the solver regenerates layout from pieces + stock inventory.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path

from boardcomposer.domain import Board, Project, ProjectConstraints, StockPanel

CURRENT_VERSION = 2


class UnsupportedProjectVersionError(Exception):
    """Raised when a ``.bcproj`` declares a version this build cannot read."""

    def __init__(self, file_version: int) -> None:
        self.file_version = file_version
        super().__init__(
            f"El proyecto usa la versión {file_version}, pero esta versión de "
            f"BoardComposer solo admite hasta la versión {CURRENT_VERSION}. "
            "Actualiza la aplicación para abrir este archivo."
        )


def _migrate_v1_to_v2(data: dict) -> dict:
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


def migrate_bcproj_dict(data: dict) -> dict:
    """Run version migrations up to ``CURRENT_VERSION`` (ADR-015)."""
    file_version = data.get("version", 1)

    if file_version > CURRENT_VERSION:
        raise UnsupportedProjectVersionError(file_version)

    migrated = data
    version = file_version
    while version < CURRENT_VERSION:
        migrated = _MIGRATIONS[version](migrated)
        version += 1
    return migrated


def core_project_from_bcproj_dict(data: dict) -> Project:
    """Build a Core ``Project`` from a (possibly unmigrated) ``.bcproj`` dict.

    Studio ``boards`` → ``StockPanel`` inventory; ``pieces`` → ``Board`` pieces.
    """
    data = migrate_bcproj_dict(data)
    boards = data.get("boards", [])
    first = boards[0] if boards else None

    if first is not None:
        constraints = ProjectConstraints(
            max_length_mm=float(first["length_mm"]),
            max_width_mm=float(first["width_mm"]),
            allow_rotation=True,
            allow_cutting=False,
        )
    else:
        constraints = ProjectConstraints(
            allow_rotation=True,
            allow_cutting=False,
        )

    project = Project(constraints=constraints)

    for item in boards:
        project.add_stock_panel(
            StockPanel(
                length_mm=float(item["length_mm"]),
                width_mm=float(item["width_mm"]),
                thickness_mm=float(item.get("thickness_mm", 19)),
                id=item.get("board_id"),
                quantity=int(item.get("quantity", 1)),
                material=str(item.get("material", "Demo")),
            )
        )

    for item in data.get("pieces", []):
        project.add_board(
            Board(
                length_mm=float(item["length_mm"]),
                width_mm=float(item["width_mm"]),
                thickness_mm=float(item.get("thickness_mm", 19)),
                id=item.get("piece_id"),
                material=str(item.get("material", "Demo")),
            )
        )

    return project


def load_project_from_bcproj(path: str | Path) -> Project:
    """Load a Core ``Project`` from a ``.bcproj`` file path."""
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return core_project_from_bcproj_dict(payload)
