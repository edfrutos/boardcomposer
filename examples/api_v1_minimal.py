#!/usr/bin/env python3
"""Minimal integrator example for ``boardcomposer.api.v1`` (EP-001).

Run from the repo root (with ``src`` on ``PYTHONPATH``, e.g. via pytest
``pythonpath`` or ``pip install -e .``)::

    python examples/api_v1_minimal.py
"""

from __future__ import annotations

from pathlib import Path

from boardcomposer.api import v1

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "samples" / "basic_boards.csv"


def main() -> None:
    project, solutions = v1.run(CSV, strategy="balanced", top=1)
    print(
        f"api={v1.API_VERSION} boards={len(project.boards)} solutions={len(solutions)}"
    )
    if not solutions:
        print("No valid solutions.")
        return
    print(
        v1.export_json(
            solutions[0], project, strategy_name="balanced", solution_index=0
        )
    )


if __name__ == "__main__":
    main()
