"""Export ranked Studio candidates to a folder (IDE-0035 / SCR-007).

EP-002 ``boardcomposer-batch`` still solves folders of projects. This helper
only writes already-ranked ``AssemblySolution`` rows from the Comparator.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path

from boardcomposer.domain import AssemblySolution, Project
from studio.export_options import ExportOptions, render_export


def ranked_export_filename(index: int, extension: str) -> str:
    """Return ``boardcomposer-solution-01.svg`` (1-based ranking index)."""
    return f"boardcomposer-solution-{index + 1:02d}.{extension}"


def write_export_payload(
    path: Path, payload: str | bytes, options: ExportOptions
) -> None:
    """Write one rendered export, converting SVG to raster when needed."""
    options = options.normalized()
    path.parent.mkdir(parents=True, exist_ok=True)
    if options.format in {"png", "jpeg"}:
        from studio.solution_thumbnail import svg_to_raster_bytes

        assert isinstance(payload, str)
        image_format = "PNG" if options.format == "png" else "JPEG"
        path.write_bytes(svg_to_raster_bytes(payload, image_format=image_format))
        return
    if isinstance(payload, bytes):
        path.write_bytes(payload)
        return
    path.write_text(payload, encoding="utf-8")


def export_ranked_solutions(
    solutions: Sequence[AssemblySolution],
    project: Project | None,
    options: ExportOptions,
    directory: str | Path,
    *,
    strategy_name: str | None = None,
    material_prices: Mapping[str, float] | None = None,
) -> list[Path]:
    """Write every ranked candidate into ``directory``. Returns written paths."""
    options = options.normalized()
    target = Path(directory)
    target.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for index, solution in enumerate(solutions):
        path = target / ranked_export_filename(index, options.extension)
        payload = render_export(
            solution,
            project,
            options,
            strategy_name=strategy_name,
            solution_index=index,
            material_prices=material_prices,
        )
        write_export_payload(path, payload, options)
        written.append(path)
    return written
