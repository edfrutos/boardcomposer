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

    tmpl_a = manager.get("PDF", client="A")
    tmpl_b = manager.get("PDF", client="B")
    assert tmpl_a is not None
    assert tmpl_b is not None
    assert tmpl_a.options.format == "pdf"
    assert tmpl_b.options.format == "svg"


def test_export_templates_manager_replaces_same_client_and_name(tmp_path):
    path = tmp_path / "templates.json"
    manager = ExportTemplatesManager(path=path)
    manager.save_template("Demo", ExportOptions(format="svg"), client="Acme")
    manager.save_template(
        "Demo", ExportOptions(format="csv", include_offcuts=False), client="Acme"
    )

    assert manager.names(client="Acme") == ["Demo"]
    demo = manager.get("Demo", client="Acme")
    assert demo is not None
    assert demo.options.format == "csv"


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


def test_export_dialog_secondary_buttons_polished(qapp):
    del qapp
    dialog = ExportDialog(
        AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)]),
        None,
        ExportOptions(format="svg"),
        language="es",
    )
    for button in (
        dialog.save_template_button,
        dialog.delete_template_button,
        dialog.export_templates_button,
        dialog.import_templates_button,
    ):
        assert button.minimumHeight() >= 36
        assert button.toolTip()
        assert button.statusTip() == button.toolTip()
    assert "plantilla" in dialog.save_template_button.toolTip().lower()


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


def test_export_pack_and_import_merge(tmp_path):
    source = ExportTemplatesManager(path=tmp_path / "a.json", autoload=False)
    source.save_template("PDF", ExportOptions(format="pdf"), client="Acme")
    source.save_template("SVG", ExportOptions(format="svg"))

    pack = tmp_path / "pack.json"
    assert source.export_pack(pack) == 2
    assert source.export_pack(tmp_path / "acme.json", client="Acme") == 1

    target = ExportTemplatesManager(path=tmp_path / "b.json", autoload=False)
    target.save_template("SVG", ExportOptions(format="json"))
    imported, total = target.import_pack(pack, mode="merge")

    assert imported == 2
    assert total == 2
    svg = target.get("SVG", client="")
    assert svg is not None
    assert svg.options.format == "svg"
    assert target.get("PDF", client="Acme") is not None


def test_import_pack_replace_and_legacy_list(tmp_path):
    pack = tmp_path / "legacy.json"
    pack.write_text(
        '[{"name": "Solo", "format": "dxf", "client": "Beta"}]',
        encoding="utf-8",
    )
    manager = ExportTemplatesManager(path=tmp_path / "c.json", autoload=False)
    manager.save_template("Keep", ExportOptions(format="svg"))
    imported, total = manager.import_pack(pack, mode="replace")

    assert imported == 1
    assert total == 1
    assert manager.get("Keep") is None
    solo = manager.get("Solo", client="Beta")
    assert solo is not None
    assert solo.options.format == "dxf"


def test_export_dialog_shows_share_buttons(qapp):
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
    assert dialog.export_templates_button.text() == "Export pack…"
    assert dialog.import_templates_button.text() == "Import pack…"


def test_export_dialog_templates_path_uses_remembered_directory(qapp, tmp_path):
    del qapp
    pack_dir = tmp_path / "packs"
    pack_dir.mkdir()
    solution = AssemblySolution(
        placements=[BoardPlacement("A", 0, 0, 100, 50)],
    )
    dialog = ExportDialog(
        solution,
        None,
        ExportOptions(format="svg"),
        language="en",
        templates_directory=str(pack_dir),
    )
    assert dialog._suggested_templates_path(
        "boardcomposer-export-templates.json"
    ) == str(pack_dir / "boardcomposer-export-templates.json")
    assert dialog._suggested_templates_path() == str(pack_dir)


def test_export_dialog_export_pack_remembers_directory(qapp, tmp_path, monkeypatch):
    del qapp
    chosen: list[str] = []
    pack_dir = tmp_path / "out"
    pack_dir.mkdir()
    target = pack_dir / "pack.json"
    manager = ExportTemplatesManager(path=tmp_path / "templates.json", autoload=False)
    manager.save_template("SVG", ExportOptions(format="svg"))

    solution = AssemblySolution(
        placements=[BoardPlacement("A", 0, 0, 100, 50)],
    )
    dialog = ExportDialog(
        solution,
        None,
        ExportOptions(format="svg"),
        language="en",
        templates=manager,
        on_templates_directory=lambda path: chosen.append(str(path)),
    )
    monkeypatch.setattr(
        "studio.dialogs.export_dialog.QFileDialog.getSaveFileName",
        lambda *args, **kwargs: (str(target), "json"),
    )
    monkeypatch.setattr(
        "studio.dialogs.export_dialog.QMessageBox.information",
        lambda *args, **kwargs: None,
    )

    dialog._export_templates_pack()

    assert target.is_file()
    assert chosen == [str(target)]
    assert dialog._templates_directory == str(pack_dir.resolve())
