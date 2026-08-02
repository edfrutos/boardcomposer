"""Tests for shared dialog chrome (primary OK button)."""

from pathlib import Path

from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QApplication,
    QDialogButtonBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from studio.board_csv_importer import ImportBoardsResult, ImportedBoardRow
from studio.dialogs.dialog_chrome import (
    polish_secondary_button,
    repolish_secondary_buttons,
)
from studio.dialogs.help_dialogs import AboutDialog, ShortcutsDialog, WhatsNewDialog
from studio.dialogs.import_boards_preview_dialog import ImportBoardsPreviewDialog
from studio.dialogs.preferences_dialog import PreferencesDialog
from studio.models import StudioBoard
from studio.dialogs.project_template_dialog import ProjectTemplatePickerDialog
from studio.preferences import StudioPreferences
from studio.project_templates import ProjectTemplateInfo
from studio.theme import apply_theme
from studio.theme_tokens import LIGHT_CANVAS
from studio.workspace.canvas_style import set_active_canvas_theme


def _assert_primary_ok(dialog) -> None:
    box = dialog.findChild(QDialogButtonBox)
    assert box is not None
    ok = box.button(QDialogButtonBox.StandardButton.Ok)
    assert ok is not None
    assert ok.objectName() == "primaryButton"
    assert ok.minimumHeight() >= 36


def test_polish_secondary_button_sets_height_and_tip(qapp):
    del qapp
    button = QPushButton("Go")
    polish_secondary_button(button, tip="Do the thing")
    assert button.minimumHeight() >= 36
    assert button.toolTip() == "Do the thing"
    assert button.statusTip() == "Do the thing"


def test_repolish_secondary_buttons_after_theme_switch(qapp):
    """light → system can wipe minimumHeight; repolish restores it."""
    del qapp
    app = QApplication.instance()
    assert app is not None
    host = QWidget()
    button = polish_secondary_button(QPushButton("Go"), min_height=36)
    QVBoxLayout(host).addWidget(button)
    apply_theme(app, "light")
    host.show()
    app.processEvents()
    apply_theme(app, "system")
    app.processEvents()
    assert button.minimumHeight() == 0
    repolish_secondary_buttons(host)
    assert button.minimumHeight() >= 36


def test_preferences_open_config_folder_is_polished(qapp):
    del qapp
    dialog = PreferencesDialog(StudioPreferences(language="es"))
    assert dialog.open_config_folder.minimumHeight() >= 36
    tip = dialog.open_config_folder.toolTip().lower()
    assert "preferences" in tip or "configuración" in tip or "configuracion" in tip


def test_template_picker_secondary_buttons_polished(qapp):
    del qapp
    picker = ProjectTemplatePickerDialog(
        [ProjectTemplateInfo(name="Demo", path=Path("/tmp/demo.bcproj"))],
        language="es",
    )
    assert picker.rename_button.minimumHeight() >= 36
    assert picker.delete_button.minimumHeight() >= 36
    assert "renombr" in picker.rename_button.toolTip().lower()
    assert "elimin" in picker.delete_button.toolTip().lower()


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


def test_import_preview_error_rows_use_canvas_invalid_fill(qapp):
    del qapp
    set_active_canvas_theme("light")
    result = ImportBoardsResult(
        rows=(
            ImportedBoardRow(
                row_number=2,
                raw={},
                board=None,
                display_id="BAD",
                errors=("Dimensión inválida",),
            ),
        )
    )
    dialog = ImportBoardsPreviewDialog(result, language="en")
    item = dialog.table.item(0, 0)
    assert item is not None
    assert item.background().color().name() == QColor(LIGHT_CANVAS.invalid_fill).name()


def test_import_preview_shows_row_level_valid_and_error_status(qapp):
    del qapp
    result = ImportBoardsResult(
        rows=(
            ImportedBoardRow(
                row_number=2,
                raw={},
                board=StudioBoard("B-OK", 2000, 1000, "MDF", 19, 1),
                display_id="B-OK",
                errors=(),
            ),
            ImportedBoardRow(
                row_number=3,
                raw={},
                board=None,
                display_id="B-BAD",
                errors=("Dimensión inválida",),
            ),
        )
    )
    dialog = ImportBoardsPreviewDialog(result, language="es")
    status_col = dialog.table.columnCount() - 1

    assert dialog.table.item(0, status_col).text() == "OK"
    assert "Dimensión inválida" in dialog.table.item(1, status_col).text()
