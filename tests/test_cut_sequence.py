"""Per-panel saw sequence (IDE-0027)."""

from boardcomposer import Project, StockPanel
from boardcomposer.domain import AssemblySolution, BoardPlacement, PanelReference
from boardcomposer.export import (
    CutListMeta,
    build_cut_list,
    build_cut_sequences,
    cut_list_to_csv,
    cut_list_to_pdf,
    piece_sequence_numbers,
    solution_to_dxf,
    solution_to_pdf,
    solution_to_svg,
)


def _side_by_side() -> tuple[Project, AssemblySolution]:
    project = Project()
    project.add_stock_panel(StockPanel(2500, 1250, 19, "P1"))
    solution = AssemblySolution(
        placements=[
            BoardPlacement(
                "B",
                400,
                0,
                200,
                300,
                panel_reference=PanelReference(0, 0),
            ),
            BoardPlacement(
                "A",
                0,
                0,
                400,
                300,
                panel_reference=PanelReference(0, 0),
            ),
        ]
    )
    return project, solution


def test_guillotine_side_by_side_rips_strip_then_cross_cuts():
    project, solution = _side_by_side()
    sequences = build_cut_sequences(solution, project)
    assert len(sequences) == 1
    panel = sequences[0]
    assert panel.guillotine is True
    assert panel.piece_order == ("A", "B")
    kinds = [step.kind for step in panel.steps]
    assert kinds == ["h", "v", "piece", "piece"]
    assert panel.steps[0].position_mm == 300
    assert panel.steps[1].position_mm == 400
    assert panel.steps[2].piece_id == "A"
    assert panel.steps[3].piece_id == "B"


def test_stacked_pieces_cut_horizontal_then_each_piece():
    project = Project()
    project.add_stock_panel(StockPanel(2500, 1250, 19, "P1"))
    solution = AssemblySolution(
        placements=[
            BoardPlacement(
                "A",
                0,
                0,
                400,
                300,
                panel_reference=PanelReference(0, 0),
            ),
            BoardPlacement(
                "B",
                0,
                300,
                400,
                200,
                panel_reference=PanelReference(0, 0),
            ),
        ]
    )
    panel = build_cut_sequences(solution, project)[0]
    assert panel.guillotine is True
    assert panel.piece_order == ("A", "B")
    assert [step.kind for step in panel.steps] == ["h", "piece", "piece"]
    assert panel.steps[0].position_mm == 300


def test_sequences_are_independent_per_physical_panel():
    project = Project()
    project.add_stock_panel(StockPanel(1000, 500, 19, "P1", quantity=2))
    solution = AssemblySolution(
        placements=[
            BoardPlacement(
                "A",
                0,
                0,
                400,
                300,
                panel_reference=PanelReference(0, 0),
            ),
            BoardPlacement(
                "B",
                0,
                0,
                200,
                150,
                panel_reference=PanelReference(0, 1),
            ),
        ]
    )
    sequences = build_cut_sequences(solution, project)
    assert len(sequences) == 2
    assert sequences[0].piece_order == ("A",)
    assert sequences[1].piece_order == ("B",)
    numbers = piece_sequence_numbers(solution, project)
    assert numbers[0] == 1
    assert numbers[1] == 1


def test_piece_sequence_numbers_follow_panel_order():
    project, solution = _side_by_side()
    numbers = piece_sequence_numbers(solution, project)
    # placements listed B then A; order on panel is A then B.
    assert numbers[0] == 2
    assert numbers[1] == 1


def test_cut_list_includes_sequence_and_saw_rows():
    project, solution = _side_by_side()
    cut_list = build_cut_list(solution, project, CutListMeta(project_name="Taller"))
    assert [cut.piece_id for cut in cut_list.cuts] == ["A", "B"]
    assert [cut.sequence for cut in cut_list.cuts] == [1, 2]
    csv_payload = cut_list_to_csv(cut_list)
    assert "sequence" in csv_payload.splitlines()[0]
    assert any(line.startswith("saw,") for line in csv_payload.splitlines())
    assert "guillotina" in cut_list_to_pdf(cut_list).decode("latin-1", errors="replace")
    pdf = cut_list_to_pdf(cut_list)
    assert b"Secuencia de sierra" in pdf
    assert b"Corte horizontal" in pdf


def test_plan_exporters_draw_sequence_numbers():
    project, solution = _side_by_side()
    svg = solution_to_svg(solution, project)
    assert 'data-cut-seq="1"' in svg
    assert 'data-cut-seq="2"' in svg
    assert "A 400x300" in svg

    svg_plain = solution_to_svg(solution, project, include_piece_labels=False)
    assert 'data-cut-seq="1"' in svg_plain
    assert "A 400x300" not in svg_plain

    dxf = solution_to_dxf(solution, project)
    assert "SEQ" in dxf
    pdf = solution_to_pdf(solution, project)
    assert pdf.startswith(b"%PDF-1.4")
