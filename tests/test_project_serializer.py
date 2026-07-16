import pytest

from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.project_serializer import (
    CURRENT_VERSION,
    UnsupportedProjectVersionError,
    project_from_dict,
    project_to_dict,
)


def test_project_serialization_preserves_stock_and_panel_assignment():
    project = StudioProject(
        project_id="PRJ-1",
        name="Multipanel",
        boards=[StudioBoard("P1", 1000, 500, "Melamina", 19, 2)],
        pieces=[StudioPiece("A", 900, 400, "Melamina", 19)],
        placements=[StudioPlacement("A", 0, 0, False, 0, "P1", 1, 0)],
    )

    payload = project_to_dict(project)
    restored = project_from_dict(payload)

    assert payload["version"] == 2
    assert restored == project


def test_version_one_project_uses_backward_compatible_defaults():
    restored = project_from_dict(
        {
            "version": 1,
            "project_id": "PRJ-OLD",
            "name": "Legacy",
            "boards": [
                {
                    "board_id": "P1",
                    "length_mm": 1000,
                    "width_mm": 500,
                    "material": "Demo",
                }
            ],
            "pieces": [
                {
                    "piece_id": "A",
                    "length_mm": 900,
                    "width_mm": 400,
                    "material": "Demo",
                }
            ],
            "placements": [
                {
                    "piece_id": "A",
                    "x_mm": 0,
                    "y_mm": 0,
                }
            ],
        }
    )

    assert restored.boards[0].thickness_mm == 19
    assert restored.boards[0].quantity == 1
    assert restored.pieces[0].thickness_mm == 19
    assert restored.placements[0].board_id is None
    assert restored.placements[0].stock_panel_index is None


def test_project_without_an_explicit_version_is_treated_as_version_one():
    restored = project_from_dict(
        {
            "project_id": "PRJ-OLD",
            "name": "Legacy sin version",
            "boards": [],
            "pieces": [],
            "placements": [],
        }
    )

    assert restored.project_id == "PRJ-OLD"


def test_loading_a_future_project_version_raises_an_explicit_error():
    with pytest.raises(UnsupportedProjectVersionError) as excinfo:
        project_from_dict(
            {
                "version": CURRENT_VERSION + 1,
                "project_id": "PRJ-FUTURE",
                "name": "Del futuro",
                "boards": [],
                "pieces": [],
                "placements": [],
            }
        )

    assert excinfo.value.file_version == CURRENT_VERSION + 1


def test_migration_chain_fills_every_default_for_a_bare_version_one_project():
    restored = project_from_dict(
        {
            "version": 1,
            "project_id": "PRJ-BARE",
            "name": "Sin extras",
            "boards": [{"board_id": "P1", "length_mm": 1000, "width_mm": 500}],
            "pieces": [{"piece_id": "A", "length_mm": 400, "width_mm": 300}],
            "placements": [{"piece_id": "A", "x_mm": 0, "y_mm": 0}],
        }
    )

    assert restored.boards[0] == StudioBoard("P1", 1000, 500, "Demo", 19, 1)
    assert restored.pieces[0] == StudioPiece("A", 400, 300, "Demo", 19)
    assert restored.placements[0] == StudioPlacement("A", 0, 0, False, 0, None, 0, None)
