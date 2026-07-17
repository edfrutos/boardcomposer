"""Tests for comparator solution thumbnails (SVG → pixmap)."""

from PySide6.QtCore import QSize

from boardcomposer import AssemblySolution, BoardPlacement
from boardcomposer.export import solution_to_svg
from studio.solution_thumbnail import (
    shared_fit_scale,
    solution_thumbnails,
    svg_default_size,
    svg_to_pixmap,
)


def test_svg_to_pixmap_produces_non_empty_image(qapp):
    del qapp
    svg = solution_to_svg(
        AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])
    )

    pixmap = svg_to_pixmap(svg, box=QSize(200, 120))

    assert not pixmap.isNull()
    assert pixmap.width() > 0
    assert pixmap.height() > 0


def test_solution_thumbnails_share_a_common_scale(qapp):
    del qapp
    small = solution_to_svg(
        AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])
    )
    large = solution_to_svg(
        AssemblySolution(placements=[BoardPlacement("B", 0, 0, 400, 200)])
    )
    box = QSize(200, 120)

    pixmaps = solution_thumbnails([small, large], box=box)
    sizes = [svg_default_size(small), svg_default_size(large)]
    scale = shared_fit_scale(sizes, box)

    assert len(pixmaps) == 2
    assert pixmaps[0].width() == max(1, round(sizes[0].width() * scale))
    assert pixmaps[1].width() == max(1, round(sizes[1].width() * scale))
    assert pixmaps[0].width() < pixmaps[1].width()
