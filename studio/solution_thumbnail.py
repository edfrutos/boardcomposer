"""Render solution SVG documents as Qt pixmaps for the comparator strip."""

from __future__ import annotations

from PySide6.QtCore import QByteArray, QSize
from PySide6.QtGui import QColor, QImage, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

from boardcomposer.export import DEFAULT_SVG_PALETTE

DEFAULT_THUMBNAIL_SIZE = QSize(200, 120)


def svg_default_size(svg: str) -> QSize:
    """Return the intrinsic SVG size, or a 1×1 fallback if invalid."""
    renderer = QSvgRenderer(QByteArray(svg.encode("utf-8")))
    size = renderer.defaultSize()
    if size.width() <= 0 or size.height() <= 0:
        return QSize(1, 1)
    return size


def shared_fit_scale(sizes: list[QSize], box: QSize) -> float:
    """Scale that fits every size into `box` while keeping a common mm→px ratio."""
    if not sizes or box.width() <= 0 or box.height() <= 0:
        return 1.0

    max_width = max(size.width() for size in sizes)
    max_height = max(size.height() for size in sizes)
    if max_width <= 0 or max_height <= 0:
        return 1.0

    return min(box.width() / max_width, box.height() / max_height)


def _fill_color() -> QColor:
    return QColor(DEFAULT_SVG_PALETTE.background)


def svg_to_pixmap(
    svg: str,
    *,
    box: QSize = DEFAULT_THUMBNAIL_SIZE,
    scale: float | None = None,
) -> QPixmap:
    """Rasterize an SVG string into a pixmap.

    When `scale` is provided, all thumbnails share the same mm→px ratio
    (SCR-003: same scale across compared solutions). Otherwise the SVG is
    fitted independently into `box`.
    """
    renderer = QSvgRenderer(QByteArray(svg.encode("utf-8")))
    default = renderer.defaultSize()
    fill = _fill_color()
    if default.width() <= 0 or default.height() <= 0:
        pixmap = QPixmap(box)
        pixmap.fill(fill)
        return pixmap

    if scale is None:
        scale = min(box.width() / default.width(), box.height() / default.height())

    width = max(1, int(round(default.width() * scale)))
    height = max(1, int(round(default.height() * scale)))

    image = QImage(width, height, QImage.Format.Format_ARGB32)
    image.fill(fill)
    painter = QPainter(image)
    renderer.render(painter)
    painter.end()
    return QPixmap.fromImage(image)


def solution_thumbnails(
    svgs: list[str],
    *,
    box: QSize = DEFAULT_THUMBNAIL_SIZE,
) -> list[QPixmap]:
    """Render a list of SVG documents with a shared scale into `box`."""
    sizes = [svg_default_size(svg) for svg in svgs]
    scale = shared_fit_scale(sizes, box)
    return [svg_to_pixmap(svg, box=box, scale=scale) for svg in svgs]
