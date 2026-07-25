"""Tests for shared dialog chrome (primary OK button)."""

from pathlib import Path

from PySide6.QtWidgets import QDialogButtonBox

from studio.board_csv_importer import ImportBoardsResult
from studio.dialogs.help_dialogs import AboutDialog, ShortcutsDialog, WhatsNewDialog
from studio.dialogs.import_boards_preview_dialog import ImportBoardsPreviewDialog
from studio.dialogs.project_template_dialog import ProjectTemplatePickerDialog
from studio.project_templates import ProjectTemplateInfo


def _assert_primary_ok(dialog) -> None:
    box = dialog.findChild(QDialogButtonBox)
    assert box is not None
    ok = box.button(QDialogButtonBox.StandardButton.Ok)
    assert ok is not None
    assert ok.objectName() == "primaryButton"
    assert ok.minimumHeight() >= 36


def test_help_dialogs_mark_ok_as_primary(qapp):
    del qapp
    for dialog in (
        WhatsNewDialog(language="en"),
        AboutDialog(language="en"),
        ShortcutsDialog(language="en"),
    ):
        _assert_primary_ok(dialog)


def test_import_preview_and_template_mark_ok_as_primary(qapp):
    del qapp
    preview = ImportBoardsPreviewDialog(ImportBoardsResult(), language="en")
    _assert_primary_ok(preview)

    picker = ProjectTemplatePickerDialog(
        [ProjectTemplateInfo(name="Demo", path=Path("/tmp/demo.bcproj"))],
        language="en",
    )
    _assert_primary_ok(picker)
