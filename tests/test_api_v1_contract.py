"""Contract tests for boardcomposer.api.v1 (EP-001).

These tests intentionally pin the public surface. Renaming, removing, or
changing the meaning of an export without a version bump should fail CI.
"""

from __future__ import annotations

import importlib
import json
import sys

import pytest

from boardcomposer.api import v1


SAMPLE_CSV = "data/samples/basic_boards.csv"

EXPECTED_PUBLIC = {
    "API_VERSION",
    "export_csv",
    "export_json",
    "export_svg",
    "load_project",
    "run",
    "solve",
}


def test_api_version_is_semver_v1():
    assert v1.API_VERSION == "1.0.0"
    assert v1.API_VERSION.startswith("1.")


def test_public_exports_are_stable():
    assert set(v1.__all__) == EXPECTED_PUBLIC
    for name in EXPECTED_PUBLIC:
        assert hasattr(v1, name), f"missing public export: {name}"


def test_v1_does_not_import_studio():
    # Fresh import path: drop cached modules that tests may have loaded.
    for key in list(sys.modules):
        if key == "studio" or key.startswith("studio."):
            del sys.modules[key]

    importlib.reload(importlib.import_module("boardcomposer.api.v1"))
    importlib.reload(importlib.import_module("boardcomposer.api.v1.pipeline"))

    assert not any(
        name == "studio" or name.startswith("studio.") for name in sys.modules
    )


def test_load_solve_export_roundtrip_without_qt():
    project = v1.load_project(SAMPLE_CSV)
    solutions = v1.solve(project, strategy="balanced", top=3)

    assert len(project.boards) == 3
    assert solutions, "expected at least one layout solution"

    payload = json.loads(
        v1.export_json(
            solutions[0],
            project,
            strategy_name="balanced",
            solution_index=0,
        )
    )
    assert payload["strategy"] == "balanced"
    assert payload["placements"]

    svg = v1.export_svg(solutions[0], project)
    assert svg.lstrip().startswith("<svg")

    csv_text = v1.export_csv(solutions[0])
    assert "piece_id" in csv_text.splitlines()[0]


def test_run_convenience_matches_load_then_solve():
    project_a, solutions_a = v1.run(SAMPLE_CSV, strategy="material", top=2)
    project_b = v1.load_project(SAMPLE_CSV)
    solutions_b = v1.solve(project_b, strategy="material", top=2)

    assert len(project_a.boards) == len(project_b.boards)
    assert len(solutions_a) == len(solutions_b)
    assert len(solutions_a) <= 2


def test_solve_rejects_unknown_strategy():
    project = v1.load_project(SAMPLE_CSV)
    with pytest.raises(ValueError):
        v1.solve(project, strategy="not-a-strategy")
