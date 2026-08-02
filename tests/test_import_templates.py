"""Tests for import column-mapping templates (FLW-002)."""

from studio.import_templates import ImportMappingTemplate, ImportTemplatesManager


def test_import_templates_manager_round_trips(tmp_path):
    path = tmp_path / "import_templates.json"
    manager = ImportTemplatesManager(path=path)
    manager.save_template(
        "boards",
        "ERP Acme",
        {
            "board_id": "Codigo",
            "length_mm": "L",
            "width_mm": "A",
        },
    )
    manager.save_template(
        "pieces",
        "ERP Acme",
        {
            "piece_id": "Ref",
            "length_mm": "Largo",
            "width_mm": "Ancho",
        },
    )

    reloaded = ImportTemplatesManager(path=path)

    assert reloaded.names("boards") == ["ERP Acme"]
    assert reloaded.names("pieces") == ["ERP Acme"]
    boards = reloaded.get("boards", "ERP Acme")
    assert boards is not None
    assert boards.header_map["board_id"] == "Codigo"


def test_import_templates_manager_replaces_same_kind_and_name(tmp_path):
    path = tmp_path / "import_templates.json"
    manager = ImportTemplatesManager(path=path)
    manager.save_template(
        "boards",
        "Demo",
        {"board_id": "Id", "length_mm": "L", "width_mm": "W"},
    )
    manager.save_template(
        "boards",
        "Demo",
        {"board_id": "Codigo", "length_mm": "Largo", "width_mm": "Ancho"},
    )

    assert manager.names("boards") == ["Demo"]
    replaced = manager.get("boards", "Demo")
    assert replaced is not None
    assert replaced.header_map["board_id"] == "Codigo"


def test_import_templates_manager_delete(tmp_path):
    path = tmp_path / "import_templates.json"
    manager = ImportTemplatesManager(path=path)
    manager.save_template(
        "pieces",
        "Demo",
        {"piece_id": "Id", "length_mm": "L", "width_mm": "W"},
    )

    assert manager.delete("pieces", "Demo") is True
    assert manager.names("pieces") == []
    assert manager.delete("pieces", "Demo") is False


def test_find_applicable_returns_covering_template(tmp_path):
    path = tmp_path / "import_templates.json"
    manager = ImportTemplatesManager(path=path)
    manager.save_template(
        "boards",
        "Partial",
        {"board_id": "Codigo", "length_mm": "L"},
    )
    manager.save_template(
        "boards",
        "Complete",
        {
            "board_id": "Codigo",
            "length_mm": "L",
            "width_mm": "A",
            "material": "Mat",
        },
    )

    found = manager.find_applicable(
        "boards",
        ["Codigo", "L", "A", "Mat"],
        ("board_id", "length_mm", "width_mm"),
    )

    assert found is not None
    assert found.name == "Complete"


def test_find_applicable_skips_templates_with_missing_headers(tmp_path):
    path = tmp_path / "import_templates.json"
    manager = ImportTemplatesManager(path=path)
    manager.save_template(
        "boards",
        "Stale",
        {
            "board_id": "OldId",
            "length_mm": "L",
            "width_mm": "W",
        },
    )

    found = manager.find_applicable(
        "boards",
        ["Codigo", "L", "W"],
        ("board_id", "length_mm", "width_mm"),
    )

    assert found is None


def test_import_mapping_template_from_dict_rejects_bad_kind():
    assert (
        ImportMappingTemplate.from_dict(
            {
                "name": "X",
                "kind": "panels",
                "header_map": {"board_id": "Id"},
            }
        )
        is None
    )


def test_mapping_dialog_delete_button_polished(qapp, tmp_path):
    del qapp
    from studio.dialogs.import_column_mapping_dialog import ImportColumnMappingDialog

    path = tmp_path / "import_templates.json"
    manager = ImportTemplatesManager(path=path)
    manager.save_template(
        "boards",
        "ERP",
        {"board_id": "Codigo", "length_mm": "L", "width_mm": "A"},
    )
    dialog = ImportColumnMappingDialog(
        fieldnames=["Codigo", "L", "A"],
        field_order=("board_id", "length_mm", "width_mm"),
        required_fields=("board_id", "length_mm", "width_mm"),
        initial_map={},
        missing_fields=["board_id", "length_mm", "width_mm"],
        templates_manager=manager,
        language="es",
    )
    assert dialog._delete_template_button is not None
    assert dialog._delete_template_button.minimumHeight() >= 36
    tip = dialog._delete_template_button.toolTip().lower()
    assert "mapeo" in tip or "plantilla" in tip


def test_mapping_dialog_applies_selected_template(qapp):
    del qapp
    from studio.dialogs.import_column_mapping_dialog import ImportColumnMappingDialog
    from studio.import_templates import ImportMappingTemplate

    template = ImportMappingTemplate(
        name="ERP",
        kind="boards",
        header_map={
            "board_id": "Codigo",
            "length_mm": "L",
            "width_mm": "A",
        },
    )
    dialog = ImportColumnMappingDialog(
        fieldnames=["Codigo", "L", "A", "Extra"],
        field_order=("board_id", "length_mm", "width_mm", "material"),
        required_fields=("board_id", "length_mm", "width_mm"),
        initial_map={},
        missing_fields=["board_id", "length_mm", "width_mm"],
        templates=[template],
    )

    assert dialog._template_combo is not None
    dialog._template_combo.setCurrentIndex(1)

    assert dialog.header_map() == {
        "board_id": "Codigo",
        "length_mm": "L",
        "width_mm": "A",
    }


def test_mapping_dialog_deletes_selected_template(qapp, tmp_path, monkeypatch):
    del qapp
    from PySide6.QtWidgets import QMessageBox

    from studio.dialogs.import_column_mapping_dialog import ImportColumnMappingDialog

    path = tmp_path / "import_templates.json"
    manager = ImportTemplatesManager(path=path)
    manager.save_template(
        "boards",
        "ERP",
        {
            "board_id": "Codigo",
            "length_mm": "L",
            "width_mm": "A",
        },
    )
    dialog = ImportColumnMappingDialog(
        fieldnames=["Codigo", "L", "A"],
        field_order=("board_id", "length_mm", "width_mm"),
        required_fields=("board_id", "length_mm", "width_mm"),
        initial_map={},
        missing_fields=["board_id"],
        templates_manager=manager,
        kind="boards",
    )

    assert dialog._template_combo is not None
    assert dialog._delete_template_button is not None
    dialog._template_combo.setCurrentIndex(1)
    assert dialog._delete_template_button.isEnabled()

    monkeypatch.setattr(
        QMessageBox,
        "question",
        lambda *args, **kwargs: QMessageBox.StandardButton.Yes,
    )
    dialog._delete_selected_template()

    assert manager.names("boards") == []
    assert dialog._template_combo.count() == 1
    assert dialog._delete_template_button.isEnabled() is False
