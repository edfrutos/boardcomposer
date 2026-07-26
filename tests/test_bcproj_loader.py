"""Core ``.bcproj`` loader (EP-001 SPR-003)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from boardcomposer.io import (
    CURRENT_VERSION,
    UnsupportedProjectVersionError,
    load_project_from_bcproj,
)
from boardcomposer.io.bcproj import core_project_from_bcproj_dict


SAMPLE = Path("data/samples/multipanel_demo.bcproj")


def test_load_sample_bcproj_maps_stock_and_pieces():
    project = load_project_from_bcproj(SAMPLE)

    assert len(project.stock_panels) == 1
    assert project.stock_panels[0].id == "P1"
    assert project.stock_panels[0].quantity == 2
    assert project.stock_panels[0].material == "Melamina"
    assert len(project.boards) == 2
    assert {board.id for board in project.boards} == {"A", "B"}
    assert project.constraints.allow_rotation is True
    assert project.constraints.max_length_mm == 1000
    assert project.constraints.max_width_mm == 500


def test_migrate_v1_defaults_then_load_core(tmp_path):
    path = tmp_path / "legacy.bcproj"
    path.write_text(
        json.dumps(
            {
                "version": 1,
                "project_id": "PRJ-OLD",
                "name": "Legacy",
                "boards": [
                    {"board_id": "P1", "length_mm": 1000, "width_mm": 500},
                ],
                "pieces": [
                    {"piece_id": "A", "length_mm": 400, "width_mm": 300},
                ],
                "placements": [],
            }
        ),
        encoding="utf-8",
    )

    project = load_project_from_bcproj(path)
    assert project.stock_panels[0].thickness_mm == 19
    assert project.stock_panels[0].quantity == 1
    assert project.boards[0].thickness_mm == 19
    assert project.boards[0].material == "Demo"


def test_future_version_rejected():
    with pytest.raises(UnsupportedProjectVersionError) as excinfo:
        core_project_from_bcproj_dict(
            {
                "version": CURRENT_VERSION + 1,
                "project_id": "X",
                "name": "Future",
                "boards": [],
                "pieces": [],
            }
        )
    assert excinfo.value.file_version == CURRENT_VERSION + 1
