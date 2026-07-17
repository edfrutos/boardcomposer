"""Export solution placements as a CSV table."""

from __future__ import annotations

import csv
import io

from boardcomposer.domain import AssemblySolution

_FIELDNAMES = (
    "piece_id",
    "x_mm",
    "y_mm",
    "length_mm",
    "width_mm",
    "rotated",
    "stock_panel_index",
    "instance_index",
)


def solution_to_csv(solution: AssemblySolution) -> str:
    """Return a CSV listing every placement in the solution.

    Omitted pieces are not rows; use the JSON exporter for that metadata.
    """
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=_FIELDNAMES, lineterminator="\n")
    writer.writeheader()

    for placement in solution.placements:
        reference = placement.panel_reference
        writer.writerow(
            {
                "piece_id": placement.board_id,
                "x_mm": placement.x_mm,
                "y_mm": placement.y_mm,
                "length_mm": placement.length_mm,
                "width_mm": placement.width_mm,
                "rotated": "true" if placement.rotated else "false",
                "stock_panel_index": (
                    "" if reference is None else reference.stock_panel_index
                ),
                "instance_index": (
                    "" if reference is None else reference.instance_index
                ),
            }
        )

    return buffer.getvalue()
