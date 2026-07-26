"""DOC-009 must stay aligned with the live v1 exporters (EP-001 SPR-002)."""

from __future__ import annotations

from pathlib import Path

DOC = Path("docs/masterplan/DOC-009-API-v1-Formatos.md")


def test_doc_009_exists_and_pins_key_contract_fields():
    text = DOC.read_text(encoding="utf-8")
    assert "DOC-009" in text
    assert "1.1.0" in text or "API_VERSION" in text

    for field in (
        "length_mm",
        "width_mm",
        "thickness_mm",
        "piece_id",
        "omitted_piece_ids",
        "panel_reference",
        "stock_panel_index",
        "instance_index",
        "offcuts",
        "waste_ratio",
        "export_json",
        "load_project",
        ".bcproj",
        "StockPanel",
    ):
        assert field in text, f"DOC-009 missing field/token: {field}"


def test_doc_009_linked_from_index_and_ep001():
    index = Path("docs/masterplan/INDEX.md").read_text(encoding="utf-8")
    epic = Path("docs/masterplan/epics/EP-001-API-Publica-Contratos.md").read_text(
        encoding="utf-8"
    )
    assert "DOC-009-API-v1-Formatos.md" in index
    assert "SPR-002" in epic
    assert "DOC-009" in epic
