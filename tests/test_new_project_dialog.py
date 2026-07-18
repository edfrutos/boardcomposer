from PySide6.QtWidgets import QDialogButtonBox

from studio.dialogs import NewProjectDialog
from studio.events.catalog import CATALOG, WORKSPACE_OPENED
from studio.project_ids import new_project_id


def test_new_project_id_has_expected_shape():
    project_id = new_project_id()
    assert project_id.startswith("PRJ-")
    assert len(project_id) == 12
    assert project_id == project_id.upper()
    assert new_project_id() != project_id


def test_workspace_opened_is_in_catalog():
    assert WORKSPACE_OPENED in CATALOG


def test_new_project_dialog_returns_cleaned_data(qapp):
    del qapp
    dialog = NewProjectDialog(name="  Cocina  ", units="cm", language="es")
    assert dialog.project_data() == {"name": "Cocina", "units": "cm"}


def test_new_project_dialog_ok_enabled_with_prefilled_name(qapp):
    del qapp
    dialog = NewProjectDialog(name="Demo", units="mm", language="en")
    buttons = dialog.findChild(QDialogButtonBox)
    assert buttons is not None
    ok = buttons.button(QDialogButtonBox.StandardButton.Ok)
    assert ok is not None
    assert ok.isEnabled()
