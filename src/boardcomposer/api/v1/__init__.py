"""Stable Python API contract ``v1`` (EP-001).

Minimal surface for integrators that must not depend on Studio or Qt:

1. ``load_project`` — CSV → ``Project``
2. ``solve`` — layout candidates
3. ``export_json`` / ``export_svg`` / ``export_csv`` — solution artifacts
4. ``run`` — load + solve convenience

Domain types (``Project``, ``AssemblySolution``, …) remain importable from
``boardcomposer`` / ``boardcomposer.domain``.
"""

from boardcomposer.api.v1.pipeline import (
    export_csv,
    export_json,
    export_svg,
    load_project,
    run,
    solve,
)

API_VERSION = "1.0.0"

__all__ = [
    "API_VERSION",
    "export_csv",
    "export_json",
    "export_svg",
    "load_project",
    "run",
    "solve",
]
