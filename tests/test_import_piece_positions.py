"""Imported pieces must not all stack at the same free-position seed."""

from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def test_find_free_piece_position_accounts_for_pending_placements(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Import pile",
            boards=[StudioBoard("TAB-001", 2000, 1000, "Melamina blanca", 18, 2)],
            pieces=[],
            placements=[],
        )
    )
    window = MainWindow(services)

    pieces = [
        StudioPiece("A1", 400, 300, "Melamina blanca", 18),
        StudioPiece("A2", 400, 300, "Melamina blanca", 18),
        StudioPiece("T1", 200, 100, "Tablex", 5),
    ]
    lookup = {piece.piece_id: piece for piece in pieces}
    placements: list[StudioPlacement] = []
    for piece in pieces:
        x_mm, y_mm = window._find_free_piece_position(
            piece.length_mm,
            piece.width_mm,
            extra_placements=placements,
            piece_lookup=lookup,
        )
        placements.append(
            StudioPlacement(
                piece_id=piece.piece_id,
                x_mm=x_mm,
                y_mm=y_mm,
                rotated=False,
                rotation=0,
                board_id="TAB-001",
                board_instance=0,
                stock_panel_index=0,
            )
        )

    coords = {(placement.x_mm, placement.y_mm) for placement in placements}
    assert len(coords) == 3
    assert (20.0, 20.0) in coords
