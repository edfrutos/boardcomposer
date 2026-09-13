"""Tests for the workshop cut list (IDE-0023)."""

import csv
import io

from boardcomposer import Board, Project, ProjectConstraints, StockPanel
from boardcomposer.domain import (
    AssemblySolution,
    BoardPlacement,
    PanelReference,
    SolutionExplanation,
    SolutionScore,
)
from boardcomposer.export import (
    CutListMeta,
    build_cut_list,
    cut_list_to_csv,
    cut_list_to_pdf,
    render_cut_list,
)
from boardcomposer.export.cut_list import normalize_cut_list_format


def _project_and_solution() -> tuple[Project, AssemblySolution]:
    project = Project(constraints=ProjectConstraints(kerf_mm=3.2))
    project.add_stock_panel(
        StockPanel(2500, 1250, 19, "P1", quantity=2, material="Melamina")
    )
    project.add_board(Board(400, 300, 19, "A", material="Melamina"))
    project.add_board(Board(200, 100, 19, "B", material="Melamina"))
    solution = AssemblySolution(
        placements=[
            BoardPlacement(
                "A",
                10,
                20,
                400,
                300,
                rotated=False,
                panel_reference=PanelReference(0, 0),
            )
        ],
        score=SolutionScore(),
        explanation=SolutionExplanation(),
        omitted_piece_ids=("B",),
    )
    return project, solution


def test_normalize_cut_list_format():
    assert normalize_cut_list_format("PDF") == "pdf"
    assert normalize_cut_list_format("nope") == "csv"
    assert normalize_cut_list_format(None) == "csv"


def test_build_cut_list_groups_panels_pieces_and_cuts():
    project, solution = _project_and_solution()
    cut_list = build_cut_list(
        solution,
        project,
        CutListMeta(project_name="Cocina", client="ACME", kerf_mm=3.2),
    )
    assert cut_list.meta.project_name == "Cocina"
    assert cut_list.meta.client == "ACME"
    assert cut_list.panels[0].panel_id == "P1"
    assert cut_list.panels[0].instances_used == 1
    assert cut_list.panels[0].quantity == 2
    pieces = {item.piece_id: item for item in cut_list.pieces}
    assert pieces["A"].omitted is False
    assert pieces["B"].omitted is True
    assert cut_list.cuts[0].piece_id == "A"
    assert cut_list.cuts[0].panel_id == "P1"
    assert cut_list.cuts[0].x_mm == 10


def test_cut_list_csv_has_meta_panels_pieces_and_cuts():
    project, solution = _project_and_solution()
    payload = cut_list_to_csv(
        build_cut_list(
            solution,
            project,
            CutListMeta(project_name="Cocina", reference="PED-1", kerf_mm=3.2),
        )
    )
    rows = list(csv.DictReader(io.StringIO(payload)))
    kinds = [row["section"] for row in rows]
    assert kinds.count("meta") == 5
    assert "panel" in kinds and "piece" in kinds and "cut" in kinds
    meta = {row["id"]: row["value"] for row in rows if row["section"] == "meta"}
    assert meta["project_name"] == "Cocina"
    assert meta["reference"] == "PED-1"
    assert meta["kerf_mm"] == "3.2"
    cut = next(row for row in rows if row["section"] == "cut")
    assert cut["id"] == "A"
    assert cut["panel_id"] == "P1"
    omitted = next(
        row for row in rows if row["section"] == "piece" and row["id"] == "B"
    )
    assert omitted["omitted"] == "true"


def test_cut_list_pdf_is_pdf_and_mentions_workshop_sections():
    project, solution = _project_and_solution()
    payload = cut_list_to_pdf(
        build_cut_list(solution, project, CutListMeta(project_name="Cocina"))
    )
    assert payload.startswith(b"%PDF-1.4")
    assert b"Lista de corte" in payload
    assert b"Cocina" in payload
    assert b"Tableros" in payload
    assert b"Piezas" in payload
    assert b"Cortes" in payload


def test_render_cut_list_picks_csv_or_pdf():
    project, solution = _project_and_solution()
    cut_list = build_cut_list(solution, project)
    csv_payload = render_cut_list(cut_list, "csv")
    pdf_payload = render_cut_list(cut_list, "pdf")
    assert isinstance(csv_payload, str)
    assert csv_payload.startswith("section,")
    assert isinstance(pdf_payload, bytes)
    assert pdf_payload.startswith(b"%PDF")


def test_build_cut_list_without_project_uses_placements():
    solution = AssemblySolution(
        placements=[BoardPlacement("A", 0, 0, 100, 50)],
        omitted_piece_ids=("B",),
    )
    cut_list = build_cut_list(solution)
    assert cut_list.panels == ()
    ids = {item.piece_id for item in cut_list.pieces}
    assert ids == {"A", "B"}
    assert cut_list.cuts[0].piece_id == "A"
