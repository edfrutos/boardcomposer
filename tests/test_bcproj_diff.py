"""Structural .bcproj revision diffs."""

from __future__ import annotations

import json
from pathlib import Path

from boardcomposer.diff_cli import main as diff_main
from boardcomposer.io.bcproj_diff import diff_bcproj

SAMPLES = Path("data/samples")
BASE = SAMPLES / "multipanel_demo.bcproj"


def test_identical_sample():
    report = diff_bcproj(BASE, BASE)
    assert report.identical
    assert report.changes == []


def test_detects_piece_and_board_changes(tmp_path):
    left = json.loads(BASE.read_text(encoding="utf-8"))
    right = json.loads(BASE.read_text(encoding="utf-8"))
    right["name"] = "Revised demo"
    right["boards"][0]["quantity"] = 3
    right["pieces"].append(
        {
            "piece_id": "C",
            "length_mm": 100,
            "width_mm": 50,
            "material": "Melamina",
            "thickness_mm": 19,
        }
    )
    del right["pieces"][1]  # remove B

    left_path = tmp_path / "left.bcproj"
    right_path = tmp_path / "right.bcproj"
    left_path.write_text(json.dumps(left), encoding="utf-8")
    right_path.write_text(json.dumps(right), encoding="utf-8")

    report = diff_bcproj(left_path, right_path)
    assert report.identical is False
    paths = {change.path for change in report.changes}
    assert "name" in paths
    assert "boards.P1.quantity" in paths
    assert "pieces.C" in paths
    assert "pieces.B" in paths


def test_placement_count_change(tmp_path):
    left = json.loads(BASE.read_text(encoding="utf-8"))
    right = dict(left)
    right["placements"] = [
        {
            "piece_id": "A",
            "x_mm": 0,
            "y_mm": 0,
            "rotated": False,
            "rotation": 0,
            "board_id": "P1",
            "board_instance": 0,
            "stock_panel_index": 0,
        }
    ]
    left_path = tmp_path / "a.bcproj"
    right_path = tmp_path / "b.bcproj"
    left_path.write_text(json.dumps(left), encoding="utf-8")
    right_path.write_text(json.dumps(right), encoding="utf-8")
    report = diff_bcproj(left_path, right_path)
    assert any(change.path == "placements.count" for change in report.changes)


def test_diff_cli_exit_codes(tmp_path):
    other = tmp_path / "other.bcproj"
    payload = json.loads(BASE.read_text(encoding="utf-8"))
    payload["name"] = "Other"
    other.write_text(json.dumps(payload), encoding="utf-8")

    assert diff_main([str(BASE), str(BASE)]) == 0
    assert diff_main([str(BASE), str(other)]) == 1
    assert diff_main([str(BASE), str(other), "--json"]) == 1
    assert diff_main([str(BASE), str(tmp_path / "missing.bcproj")]) == 2
