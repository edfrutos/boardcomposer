"""Tests for advanced export options and preview (SCR-007)."""

import json

from boardcomposer.domain import (
    AssemblySolution,
    BoardPlacement,
    Offcut,
    PanelReference,
    SolutionExplanation,
    SolutionScore,
)
from boardcomposer.export import DEFAULT_SVG_PALETTE, prepare_solution_for_export
from studio.export_options import (
    ExportOptions,
    prepare_solution,
    preview_svg,
    preview_text,
    render_export,
)


def _solution() -> AssemblySolution:
    return AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50, panel_reference=PanelReference(0, 0))
        ],
        score=SolutionScore(waste_score=4.0),
        explanation=SolutionExplanation(notes=["test"], strengths=["compacta"]),
        offcuts=(Offcut(PanelReference(0, 0), 100, 0, 200, 50),),
    )


def test_prepare_solution_can_drop_offcuts():
    solution = _solution()

    without = prepare_solution(
        solution, ExportOptions(format="svg", include_offcuts=False)
    )

    assert solution.offcuts
    assert without.offcuts == ()


def test_prepare_solution_for_export_core_helper():
    solution = _solution()
    assert prepare_solution_for_export(solution).offcuts == solution.offcuts
    assert prepare_solution_for_export(solution, include_offcuts=False).offcuts == ()
    assert prepare_solution_for_export(solution, include_offcuts=True) is solution


def test_render_export_json_respects_content_flags():
    solution = _solution()

    payload = json.loads(
        render_export(
            solution,
            None,
            ExportOptions(
                format="json",
                include_metrics=False,
                include_explanation=False,
                include_offcuts=False,
            ),
        )
    )

    assert "metrics" not in payload
    assert "notes" not in payload
    assert "offcuts" not in payload
    assert payload["placements"][0]["piece_id"] == "A"


def test_preview_text_includes_format_summary():
    text = preview_text(_solution(), None, ExportOptions(format="pdf"))

    assert "Formato: PDF" in text
    assert "Piezas colocadas: 1" in text
    assert "Papel: drawing" in text
    assert "escala: 1:1" in text
    assert "Cotas L×A del tablero incluidas." in text


def test_render_export_png_and_jpeg_return_svg_payload():
    svg_png = render_export(_solution(), None, ExportOptions(format="png"))
    svg_jpeg = render_export(_solution(), None, ExportOptions(format="jpeg"))
    assert isinstance(svg_png, str)
    assert isinstance(svg_jpeg, str)
    assert "<svg" in svg_png
    assert "<svg" in svg_jpeg


def test_preview_svg_respects_offcuts_option():
    solution = _solution()

    with_offcuts = preview_svg(solution, None, ExportOptions(include_offcuts=True))
    without_offcuts = preview_svg(solution, None, ExportOptions(include_offcuts=False))

    assert DEFAULT_SVG_PALETTE.offcut_stroke in with_offcuts
    assert DEFAULT_SVG_PALETTE.offcut_stroke not in without_offcuts
    assert "A" in with_offcuts


def test_export_dialog_embeds_graphic_preview(qapp):
    del qapp
    from studio.dialogs import ExportDialog

    dialog = ExportDialog(_solution(), None, ExportOptions(format="svg"))
    pixmap = dialog.graphic_preview.pixmap()

    assert pixmap is not None
    assert not pixmap.isNull()
    assert "Formato: SVG" in dialog.preview.toPlainText()

    dialog.include_offcuts.setChecked(False)
    dialog._refresh_preview()
    assert "Retales: 0" in dialog.preview.toPlainText()


def test_preview_svg_respects_piece_labels_option():
    solution = _solution()

    with_labels = preview_svg(solution, None, ExportOptions(include_piece_labels=True))
    without_labels = preview_svg(
        solution, None, ExportOptions(include_piece_labels=False)
    )

    assert "A 100x50" in with_labels
    assert "A 100x50" not in without_labels


def test_preview_svg_respects_offcut_labels_option():
    solution = _solution()

    with_labels = preview_svg(solution, None, ExportOptions(include_offcut_labels=True))
    without_labels = preview_svg(
        solution, None, ExportOptions(include_offcut_labels=False)
    )

    assert "200x50" in with_labels
    assert "200x50" not in without_labels
    assert DEFAULT_SVG_PALETTE.offcut_stroke in without_labels


def test_preview_svg_respects_panel_dimensions_option():
    from boardcomposer.domain import Project, StockPanel

    project = Project()
    project.add_stock_panel(StockPanel(1000, 500, 19, "P1"))
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 400, 300, panel_reference=PanelReference(0, 0))
        ]
    )

    with_dims = preview_svg(
        solution, project, ExportOptions(include_panel_dimensions=True)
    )
    without_dims = preview_svg(
        solution, project, ExportOptions(include_panel_dimensions=False)
    )

    assert ">1000</text>" in with_dims
    assert ">500</text>" in with_dims
    assert ">1000</text>" not in without_dims
    assert ">500</text>" not in without_dims


def test_preview_svg_respects_plan_traceability_option():
    solution = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])

    with_trace = preview_svg(
        solution,
        None,
        ExportOptions(include_plan_traceability=True),
        strategy_name="material",
    )
    without_trace = preview_svg(
        solution,
        None,
        ExportOptions(include_plan_traceability=False),
        strategy_name="material",
    )

    assert "BoardComposer" in with_trace
    assert "material" in with_trace
    assert "BoardComposer" not in without_trace


def test_export_dialog_piece_labels_enabled_for_plan_formats(qapp):
    del qapp
    from studio.dialogs import ExportDialog

    dialog = ExportDialog(_solution(), None, ExportOptions(format="svg"))
    assert dialog.include_piece_labels.isEnabled()
    assert dialog.include_piece_labels.text() == "Etiquetas de piezas (id y medidas)"
    assert dialog.include_offcut_labels.isEnabled()
    assert dialog.include_offcut_labels.text() == "Etiquetas de retales (medidas)"
    assert dialog.include_panel_dimensions.isEnabled()
    assert dialog.include_panel_dimensions.text() == "Cotas L×A del tablero"
    assert dialog.include_plan_traceability.isEnabled()
    assert dialog.include_plan_traceability.text() == (
        "Trazabilidad (versión, algoritmo, fecha)"
    )

    dialog.format.setCurrentIndex(dialog.format.findData("json"))
    dialog._refresh_preview()
    assert not dialog.include_piece_labels.isEnabled()
    assert not dialog.include_offcut_labels.isEnabled()
    assert not dialog.include_panel_dimensions.isEnabled()
    assert not dialog.include_plan_traceability.isEnabled()

    dialog.format.setCurrentIndex(dialog.format.findData("svg"))
    dialog.include_offcuts.setChecked(False)
    dialog._refresh_preview()
    assert dialog.include_piece_labels.isEnabled()
    assert not dialog.include_offcut_labels.isEnabled()
    assert dialog.include_panel_dimensions.isEnabled()
    assert dialog.include_plan_traceability.isEnabled()


def test_export_dialog_pdf_page_controls_enabled_only_for_pdf(qapp):
    del qapp
    from studio.dialogs import ExportDialog

    dialog = ExportDialog(
        _solution(),
        None,
        ExportOptions(format="pdf", pdf_paper="a4", pdf_scale="fit"),
    )
    assert dialog.pdf_paper.isEnabled()
    assert dialog.pdf_orientation.isEnabled()
    assert dialog.pdf_scale.isEnabled()
    assert dialog.pdf_margin_mm.isEnabled()
    assert dialog.pdf_paper.currentData() == "a4"
    assert "Papel: a4" in dialog.preview.toPlainText()

    dialog.format.setCurrentIndex(dialog.format.findData("svg"))
    dialog._refresh_preview()
    assert not dialog.pdf_paper.isEnabled()
    assert not dialog.pdf_orientation.isEnabled()
    assert not dialog.pdf_scale.isEnabled()
    assert not dialog.pdf_margin_mm.isEnabled()

    dialog.format.setCurrentIndex(dialog.format.findData("pdf"))
    dialog.pdf_paper.setCurrentIndex(dialog.pdf_paper.findData("drawing"))
    dialog._refresh_preview()
    assert dialog.pdf_paper.isEnabled()
    assert not dialog.pdf_orientation.isEnabled()
    assert not dialog.pdf_scale.isEnabled()
    assert dialog.pdf_margin_mm.isEnabled()


def test_svg_to_raster_bytes_supports_png_and_jpeg(qapp):
    del qapp
    from studio.solution_thumbnail import svg_to_raster_bytes

    svg = preview_svg(_solution(), None, ExportOptions(format="svg"))
    png = svg_to_raster_bytes(svg, image_format="PNG")
    jpeg = svg_to_raster_bytes(svg, image_format="JPEG")
    assert png.startswith(b"\x89PNG")
    assert jpeg[:2] == b"\xff\xd8"


def test_export_options_normalizes_raster_settings():
    from studio.export_options import MAX_JPEG_QUALITY, MAX_RASTER_DPI
    from studio.export_options import MIN_JPEG_QUALITY, MIN_RASTER_DPI

    low = ExportOptions(raster_dpi=1, jpeg_quality=0).normalized()
    assert low.raster_dpi == MIN_RASTER_DPI
    assert low.jpeg_quality == MIN_JPEG_QUALITY
    high = ExportOptions(raster_dpi=999, jpeg_quality=200).normalized()
    assert high.raster_dpi == MAX_RASTER_DPI
    assert high.jpeg_quality == MAX_JPEG_QUALITY


def test_export_dialog_raster_controls_enabled_for_png_and_jpeg(qapp):
    del qapp
    from studio.dialogs import ExportDialog

    dialog = ExportDialog(
        _solution(),
        None,
        ExportOptions(format="png", raster_dpi=150),
    )
    assert dialog.raster_dpi.isEnabled()
    assert not dialog.jpeg_quality.isEnabled()
    assert dialog.raster_dpi.value() == 150
    assert "Resolución: 150 DPI." in dialog.preview.toPlainText()

    dialog.format.setCurrentIndex(dialog.format.findData("jpeg"))
    dialog._refresh_preview()
    assert dialog.raster_dpi.isEnabled()
    assert dialog.jpeg_quality.isEnabled()
    assert "Calidad JPEG:" in dialog.preview.toPlainText()

    dialog.format.setCurrentIndex(dialog.format.findData("svg"))
    dialog._refresh_preview()
    assert not dialog.raster_dpi.isEnabled()
    assert not dialog.jpeg_quality.isEnabled()


def test_svg_to_raster_bytes_respects_dpi(qapp):
    del qapp
    from studio.solution_thumbnail import svg_to_raster_bytes

    svg = preview_svg(_solution(), None, ExportOptions(format="svg"))
    small = svg_to_raster_bytes(svg, image_format="PNG", dpi=36)
    large = svg_to_raster_bytes(svg, image_format="PNG", dpi=150)
    assert small.startswith(b"\x89PNG")
    assert large.startswith(b"\x89PNG")
    assert len(large) > len(small)


def test_svg_to_raster_bytes_respects_jpeg_quality(qapp):
    del qapp
    from studio.solution_thumbnail import svg_to_raster_bytes

    svg = preview_svg(_solution(), None, ExportOptions(format="svg"))
    low = svg_to_raster_bytes(svg, image_format="JPEG", dpi=96, jpeg_quality=10)
    high = svg_to_raster_bytes(svg, image_format="JPEG", dpi=96, jpeg_quality=95)
    assert low[:2] == b"\xff\xd8"
    assert high[:2] == b"\xff\xd8"
    assert len(high) > len(low)


def test_raster_pixel_size_clamps_huge_drawings(qapp):
    del qapp
    from PySide6.QtCore import QSize

    from studio.export_options import MAX_RASTER_EDGE_PX
    from studio.solution_thumbnail import raster_pixel_size

    size = raster_pixel_size(QSize(50000, 1000), 300)
    assert max(size.width(), size.height()) <= MAX_RASTER_EDGE_PX
