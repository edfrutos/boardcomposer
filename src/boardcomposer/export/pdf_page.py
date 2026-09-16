"""ISO paper, margins and scale for plan PDFs (IDE-0034 / SCR-007).

Cut-list and quote reports stay on A4 via ``report_pdf``; this module only
sizes the layout drawing produced by ``solution_to_pdf``.
"""

from __future__ import annotations

from dataclasses import dataclass

MM_TO_PT = 72.0 / 25.4

VALID_PDF_PAPERS = ("drawing", "a4", "a3", "letter")
VALID_PDF_ORIENTATIONS = ("auto", "portrait", "landscape")
VALID_PDF_SCALES = ("fit", "1:1", "1:2", "1:5", "1:10")

DEFAULT_PDF_PAPER = "drawing"
DEFAULT_PDF_ORIENTATION = "auto"
DEFAULT_PDF_SCALE = "1:1"
DEFAULT_PDF_MARGIN_MM = 12.7  # 36 pt — previous hardcoded margin
MIN_PDF_MARGIN_MM = 0.0
MAX_PDF_MARGIN_MM = 50.0

# Portrait millimetres (ISO 216 / ANSI Letter).
_PAPER_SIZE_MM: dict[str, tuple[float, float]] = {
    "a4": (210.0, 297.0),
    "a3": (297.0, 420.0),
    "letter": (215.9, 279.4),
}

# Denominator of 1:n. ``fit`` is computed from the printable area.
_SCALE_DENOMINATOR: dict[str, float | None] = {
    "fit": None,
    "1:1": 1.0,
    "1:2": 2.0,
    "1:5": 5.0,
    "1:10": 10.0,
}


def normalize_pdf_paper(value: object) -> str:
    paper = str(value or "").strip().lower()
    return paper if paper in VALID_PDF_PAPERS else DEFAULT_PDF_PAPER


def normalize_pdf_orientation(value: object) -> str:
    orientation = str(value or "").strip().lower()
    if orientation in VALID_PDF_ORIENTATIONS:
        return orientation
    return DEFAULT_PDF_ORIENTATION


def normalize_pdf_scale(value: object) -> str:
    scale = str(value or "").strip().lower()
    return scale if scale in VALID_PDF_SCALES else DEFAULT_PDF_SCALE


def normalize_pdf_margin_mm(value: object) -> float:
    try:
        margin = float(value)
    except (TypeError, ValueError):
        return DEFAULT_PDF_MARGIN_MM
    return max(MIN_PDF_MARGIN_MM, min(MAX_PDF_MARGIN_MM, margin))


@dataclass(frozen=True)
class PdfPageOptions:
    """User page settings for a plan PDF."""

    paper: str = DEFAULT_PDF_PAPER
    orientation: str = DEFAULT_PDF_ORIENTATION
    scale: str = DEFAULT_PDF_SCALE
    margin_mm: float = DEFAULT_PDF_MARGIN_MM

    def normalized(self) -> PdfPageOptions:
        return PdfPageOptions(
            paper=normalize_pdf_paper(self.paper),
            orientation=normalize_pdf_orientation(self.orientation),
            scale=normalize_pdf_scale(self.scale),
            margin_mm=normalize_pdf_margin_mm(self.margin_mm),
        )


@dataclass(frozen=True)
class PdfPageLayout:
    """Resolved MediaBox and drawing transform in PDF points."""

    page_w_pt: float
    page_h_pt: float
    origin_x_pt: float
    origin_y_top_pt: float
    scale_pt_per_mm: float
    paper: str
    orientation: str
    scale: str
    margin_mm: float


def resolve_pdf_page(
    drawing_width_mm: float,
    drawing_height_mm: float,
    options: PdfPageOptions | None = None,
) -> PdfPageLayout:
    """Map drawing millimetres onto a PDF page."""
    opts = (options or PdfPageOptions()).normalized()
    drawing_w = max(float(drawing_width_mm), 1.0)
    drawing_h = max(float(drawing_height_mm), 1.0)
    margin_pt = opts.margin_mm * MM_TO_PT

    if opts.paper == "drawing":
        return PdfPageLayout(
            page_w_pt=drawing_w * MM_TO_PT + 2 * margin_pt,
            page_h_pt=drawing_h * MM_TO_PT + 2 * margin_pt,
            origin_x_pt=margin_pt,
            origin_y_top_pt=margin_pt,
            scale_pt_per_mm=MM_TO_PT,
            paper=opts.paper,
            orientation=opts.orientation,
            scale=opts.scale,
            margin_mm=opts.margin_mm,
        )

    portrait_w_mm, portrait_h_mm = _PAPER_SIZE_MM[opts.paper]
    landscape = opts.orientation == "landscape" or (
        opts.orientation == "auto" and drawing_w >= drawing_h
    )
    if landscape:
        page_w_mm, page_h_mm = portrait_h_mm, portrait_w_mm
        resolved_orientation = "landscape"
    else:
        page_w_mm, page_h_mm = portrait_w_mm, portrait_h_mm
        resolved_orientation = "portrait"

    page_w_pt = page_w_mm * MM_TO_PT
    page_h_pt = page_h_mm * MM_TO_PT
    printable_w = max(page_w_pt - 2 * margin_pt, 1.0)
    printable_h = max(page_h_pt - 2 * margin_pt, 1.0)

    denominator = _SCALE_DENOMINATOR[opts.scale]
    if denominator is None:
        scale = min(printable_w / drawing_w, printable_h / drawing_h)
    else:
        scale = MM_TO_PT / denominator

    extra_x = max(0.0, printable_w - drawing_w * scale)
    extra_y = max(0.0, printable_h - drawing_h * scale)
    return PdfPageLayout(
        page_w_pt=page_w_pt,
        page_h_pt=page_h_pt,
        origin_x_pt=margin_pt + extra_x / 2.0,
        origin_y_top_pt=margin_pt + extra_y / 2.0,
        scale_pt_per_mm=scale,
        paper=opts.paper,
        orientation=resolved_orientation,
        scale=opts.scale,
        margin_mm=opts.margin_mm,
    )
