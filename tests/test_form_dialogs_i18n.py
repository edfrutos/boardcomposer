"""Tests for NewBoard / NewPiece form i18n (SCR-006)."""

from PySide6.QtWidgets import QFormLayout

from studio.dialogs.new_board_dialog import NewBoardDialog
from studio.dialogs.new_piece_dialog import NewPieceDialog


def _label_texts(dialog) -> list[str]:
    form = dialog.layout().itemAt(0).layout()
    assert isinstance(form, QFormLayout)
    labels = []
    for row in range(form.rowCount()):
        item = form.itemAt(row, QFormLayout.ItemRole.LabelRole)
        if item is not None and item.widget() is not None:
            labels.append(item.widget().text())
    return labels


def test_new_board_dialog_english_labels(qapp):
    del qapp
    dialog = NewBoardDialog(language="en", units="mm")

    assert dialog.windowTitle() == "New board"
    labels = _label_texts(dialog)
    assert "Identifier:" in labels
    assert "Length (mm):" in labels
    assert "Quantity:" in labels
    assert "Material:" in labels


def test_new_piece_dialog_english_labels(qapp):
    del qapp
    dialog = NewPieceDialog(language="en", units="cm")

    assert dialog.windowTitle() == "New piece"
    labels = _label_texts(dialog)
    assert "Identifier:" in labels
    assert "Width (cm):" in labels
    assert "Allow rotation:" in labels


def test_new_board_dialog_spanish_defaults(qapp):
    del qapp
    dialog = NewBoardDialog()

    assert dialog.windowTitle() == "Nuevo tablero"
    assert "Identificador:" in _label_texts(dialog)
