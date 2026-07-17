"""Tests for named export templates (SCR-007)."""

from boardcomposer.domain import AssemblySolution, BoardPlacement
from studio.dialogs import ExportDialog
from studio.export_options import ExportOptions
from studio.export_templates import ExportTemplate, ExportTemplatesManager


def test_export_templates_manager_round_trips(tmp_path):
    path = tmp_path / "templates.json"
    manager = ExportTemplatesManager(path=path)
    manager.save_template(
        "Fabricación PDF",
        ExportOptions(format="pdf", include_offcuts=False),
    )
    manager.save_template(
        "JSON completo",
        ExportOptions(format="json", include_metrics=True),
    )

    reloaded = ExportTemplatesManager(path=path)

    assert reloaded.names() == ["Fabricación PDF", "JSON completo"]
    pdf = reloaded.get("Fabricación PDF")
    assert pdf is not None
    assert pdf.options.format == "pdf"
    assert pdf.options.include_offcuts is False


def test_export_templates_manager_replaces_same_name(tmp_path):
    path = tmp_path / "templates.json"
    manager = ExportTemplatesManager(path=path)
    manager.save_template("Demo", ExportOptions(format="svg"))
    manager.save_template("Demo", ExportOptions(format="csv", include_offcuts=False))

    assert manager.names() == ["Demo"]
    assert manager.get("Demo").options.format == "csv"


def test_export_templates_manager_delete(tmp_path):
    path = tmp_path / "templates.json"
    manager = ExportTemplatesManager(path=path)
    manager.save_template("Demo", ExportOptions(format="dxf"))

    assert manager.delete("Demo") is True
    assert manager.names() == []
    assert manager.delete("Demo") is False


def test_export_template_from_dict_rejects_empty_name():
    assert ExportTemplate.from_dict({"name": "  ", "format": "svg"}) is None


def test_export_dialog_applies_selected_template(qapp, tmp_path):
    del qapp
    manager = ExportTemplatesManager(path=tmp_path / "templates.json")
    manager.save_template(
        "Sin retales",
        ExportOptions(format="svg", include_offcuts=False),
    )
    solution = AssemblySolution(
        placements=[BoardPlacement("A", 0, 0, 100, 50)],
    )

    dialog = ExportDialog(
        solution,
        None,
        ExportOptions(format="json", include_offcuts=True),
        templates=manager,
    )

    index = dialog.template.findData("Sin retales")
    dialog.template.setCurrentIndex(index)

    assert dialog.options().format == "svg"
    assert dialog.options().include_offcuts is False


def test_export_dialog_save_template_via_manager(qapp, tmp_path):
    del qapp
    manager = ExportTemplatesManager(path=tmp_path / "templates.json")
    solution = AssemblySolution(
        placements=[BoardPlacement("A", 0, 0, 100, 50)],
    )
    dialog = ExportDialog(
        solution,
        None,
        ExportOptions(format="pdf", include_offcuts=False),
        templates=manager,
    )

    manager.save_template("PDF taller", dialog.options())
    dialog._reload_templates(selected="PDF taller")

    assert "PDF taller" in manager.names()
    assert dialog.template.currentData() == "PDF taller"
