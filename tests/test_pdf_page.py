"""Plan PDF page size, margins and scale (IDE-0034)."""

from __future__ import annotations

import re

from boardcomposer import Board, Project, ProjectConstraints, StockPanel
from boardcomposer.domain import (
    AssemblySolution,
    BoardPlacement,
    Offcut,
    PanelReference,
    SolutionExplanation,
)
from boardcomposer.export import solution_to_pdf
from boardcomposer.export.pdf_page import (
    DEFAULT_PDF_MARGIN_MM,
    MM_TO_PT,
    PdfPageOptions,
    resolve_pdf_page,
)


def _single_panel_solution() -> tuple[Project, AssemblySolution]:
    project = Project(constraints=ProjectConstraints(allow_rotation=True))
    project.add_stock_panel(StockPanel(1000, 500, 19, "P1", quantity=1))
    project.add_board(Board(400, 300, 19, "A"))
    solution = AssemblySolution(
        placements=[
            BoardPlacement(
                "A",
                0,
                0,
                400,
                300,
                panel_reference=PanelReference(0, 0),
            )
        ],
        explanation=SolutionExplanation(notes=["test"]),
        offcuts=(Offcut(PanelReference(0, 0), 400, 0, 600, 300),),
    )
    return project, solution


def _mediabox(pdf: bytes) -> tuple[float, float]:
    match = re.search(rb"/MediaBox \[0 0 ([0-9.]+) ([0-9.]+)\]", pdf)
    assert match is not None
    return float(match.group(1)), float(match.group(2))


def test_resolve_pdf_page_drawing_keeps_1_to_1_and_legacy_margin():
    layout = resolve_pdf_page(1000, 530, PdfPageOptions())

    assert layout.paper == "drawing"
    assert layout.scale_pt_per_mm == MM_TO_PT
    assert layout.origin_x_pt == DEFAULT_PDF_MARGIN_MM * MM_TO_PT
    assert abs(layout.page_w_pt - (1000 * MM_TO_PT + 2 * layout.origin_x_pt)) < 0.01


def test_resolve_pdf_page_a4_portrait_fit_uses_iso_mediabox():
    layout = resolve_pdf_page(
        1000,
        530,
        PdfPageOptions(paper="a4", orientation="portrait", scale="fit"),
    )

    assert round(layout.page_w_pt, 2) == 595.28
    assert round(layout.page_h_pt, 2) == 841.89
    printable_w = layout.page_w_pt - 2 * layout.margin_mm * MM_TO_PT
    assert layout.scale_pt_per_mm < MM_TO_PT
    assert 1000 * layout.scale_pt_per_mm <= printable_w + 0.01


def test_resolve_pdf_page_auto_orientation_picks_landscape_for_wide_drawing():
    layout = resolve_pdf_page(
        1000,
        400,
        PdfPageOptions(paper="a4", orientation="auto", scale="fit"),
    )

    assert layout.orientation == "landscape"
    assert layout.page_w_pt > layout.page_h_pt


def test_normalize_rejects_unknown_page_values():
    page = PdfPageOptions(
        paper="tabloid",
        orientation=" sideways",
        scale="1:3",
        margin_mm=999,
    ).normalized()

    assert page.paper == "drawing"
    assert page.orientation == "auto"
    assert page.scale == "1:1"
    assert page.margin_mm == 50.0


def test_solution_to_pdf_a4_fit_sets_a4_mediabox():
    project, solution = _single_panel_solution()

    pdf = solution_to_pdf(
        solution,
        project,
        page=PdfPageOptions(paper="a4", orientation="portrait", scale="fit"),
    )

    width, height = _mediabox(pdf)
    assert round(width, 2) == 595.28
    assert round(height, 2) == 841.89
    assert b"A 400x300" in pdf
    assert b"600x300" in pdf


def test_solution_to_pdf_default_page_is_larger_than_a4():
    project, solution = _single_panel_solution()

    pdf = solution_to_pdf(solution, project)
    width, height = _mediabox(pdf)

    assert width > 595.28
    assert height > 400
    assert pdf.startswith(b"%PDF-1.4")
