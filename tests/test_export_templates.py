"""Tests for named export templates / client profiles (SCR-007)."""

from boardcomposer.domain import AssemblySolution, BoardPlacement
from studio.dialogs import ExportDialog
from studio.dialogs.export_dialog import _template_key
from studio.export_options import ExportOptions
from studio.export_templates import ExportTemplate, ExportTemplatesManager


def test_export_templates_manager_round_trips(tmp_path):
    path = tmp_path / "templates.json"
    manager = ExportTemplatesManager(path=path)
    manager.save_template(
        "Fabricación PDF",
        ExportOptions(format="pdf", include_offcuts=False),
        client="Acme",
    )
    manager.save_template(
        "JSON completo",
        ExportOptions(format="json", include_metrics=True),
    )

    reloaded = ExportTemplatesManager(path=path)

    assert reloaded.clients() == ["Acme"]
    assert reloaded.names(client="Acme") == ["Fabricación PDF"]
    assert reloaded.names(client="") == ["JSON completo"]
    pdf = reloaded.get("Fabricación PDF", client="Acme")
    assert pdf is not None
    assert pdf.options.format == "pdf"
    assert pdf.client == "Acme"
    assert pdf.options.include_offcuts is False


def test_export_templates_same_name_allowed_for_different_clients(tmp_path):
    path = tmp_path / "templates.json"
    manager = ExportTemplatesManager(path=path)
    manager.save_template("PDF", ExportOptions(format="pdf"), client="A")
    manager.save_template("PDF", ExportOptions(format="svg"), client="B")

    assert manager.get("PDF", client="A").options.format == "pdf"
    assert manager.get("PDF", client="B").options.format == "svg"


def test_export_templates_manager_replaces_same_client_and_name(tmp_path):
    path = tmp_path / "templates.json"
    manager = ExportTemplatesManager(path=path)
    manager.save_template("Demo", ExportOptions(format="svg"), client="Acme")
    manager.save_template(
        "Demo", ExportOptions(format="csv", include_offcuts=False), client="Acme"
    )

    assert manager.names(client="Acme") == ["Demo"]
    assert manager.get("Demo", client="Acme").options.format == "csv"


def test_export_templates_manager_delete(tmp_path):
    path = tmp_path / "templates.json"
    manager = ExportTemplatesManager(path=path)
    manager.save_template("Demo", ExportOptions(format="dxf"), client="Acme")

    assert manager.delete("Demo", client="Acme") is True
    assert manager.names(client="Acme") == []
    assert manager.delete("Demo", client="Acme") is False


def test_export_template_from_dict_loads_legacy_without_client():
    template = ExportTemplate.from_dict({"name": "Legacy", "format": "svg"})
    assert template is not None
    assert template.client == ""
    assert template.display_label() == "Legacy"


def test_export_template_from_dict_rejects_empty_name():
    assert ExportTemplate.from_dict({"name": "  ", "format": "svg"}) is None


def test_export_dialog_applies_selected_template(qapp, tmp_path):
    del qapp
    manager = ExportTemplatesManager(path=tmp_path / "templates.json")
    manager.save_template(
        "Sin retales",
        ExportOptions(format="svg", include_offcuts=False),
        client="Taller",
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

    client_index = dialog.client.findData("Taller")
    dialog.client.setCurrentIndex(client_index)
    key = _template_key("Taller", "Sin retales")
    index = dialog.template.findData(key)
    dialog.template.setCurrentIndex(index)

    assert dialog.options().format == "svg"
    assert dialog.options().include_offcuts is False


def test_export_dialog_filters_templates_by_client(qapp, tmp_path):
    del qapp
    manager = ExportTemplatesManager(path=tmp_path / "templates.json")
    manager.save_template("A", ExportOptions(format="pdf"), client="Acme")
    manager.save_template("B", ExportOptions(format="svg"), client="Beta")
    solution = AssemblySolution(
        placements=[BoardPlacement("A", 0, 0, 100, 50)],
    )

    dialog = ExportDialog(
        solution,
        None,
        ExportOptions(format="svg"),
        templates=manager,
    )
    dialog.client.setCurrentIndex(dialog.client.findData("Acme"))

    keys = [
        dialog.template.itemData(i)
        for i in range(dialog.template.count())
        if dialog.template.itemData(i)
    ]
    assert keys == [_template_key("Acme", "A")]


def test_export_dialog_uses_english_labels(qapp):
    del qapp
    solution = AssemblySolution(
        placements=[BoardPlacement("A", 0, 0, 100, 50)],
    )
    dialog = ExportDialog(
        solution,
        None,
        ExportOptions(format="svg"),
        language="en",
    )

    assert dialog.windowTitle() == "Export solution"
    assert dialog.save_template_button.text() == "Save…"
    assert dialog.include_offcuts.text() == "Include offcuts"
    assert dialog.client.itemText(0) == "(all clients)"


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

    manager.save_template("PDF taller", dialog.options(), client="Acme")
    dialog._reload_clients(selected="Acme")
    dialog._reload_templates(selected_key=_template_key("Acme", "PDF taller"))

    assert manager.get("PDF taller", client="Acme") is not None
    assert dialog.template.currentData() == _template_key("Acme", "PDF taller")
