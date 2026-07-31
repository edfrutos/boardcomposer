"""Enter / Editar… opens the edit dialog for the current selection."""

from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="EditSel",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
            pieces=[StudioPiece("A", 200, 100, "Demo", 19)],
            placements=[
                StudioPlacement("A", 10, 20, False, 0, "B1", 0, 0),
            ],
        )
    )
    window = MainWindow(services)
    window.workspace.reload_project()
    window._reload_explorer()
    return window


def test_edit_selection_shortcut_is_return(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    assert window._actions["edit_selection"].shortcut().toString() == "Return"


def test_edit_selection_opens_piece_dialog(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path)
    item = window._find_explorer_item_by_role("piece:A")
    assert item is not None
    window.explorer.setCurrentItem(item)
    called: list[str] = []
    monkeypatch.setattr(window, "_edit_piece", lambda piece_id: called.append(piece_id))

    window._actions["edit_selection"].trigger()

    assert called == ["A"]


def test_edit_selection_opens_board_dialog(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path)
    item = window._find_explorer_item_by_role("board:B1")
    assert item is not None
    window.explorer.setCurrentItem(item)
    called: list[str] = []
    monkeypatch.setattr(window, "_edit_board", lambda board_id: called.append(board_id))

    window._edit_selection()

    assert called == ["B1"]


def test_edit_selection_without_target_shows_status(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.explorer.setCurrentItem(None)
    window.workspace.clear_piece_selection()

    window._edit_selection()

    assert window._tr("status.nothing_to_edit_selection") in (
        window.statusBar().currentMessage()
    )


class _AcceptSameBoard:
    DialogCode = type("DialogCode", (), {"Accepted": 1})()

    def __init__(self, *args, **kwargs):
        del args, kwargs

    def exec(self):
        return self.DialogCode.Accepted

    def board_data(self):
        return {
            "board_id": "B1",
            "length_mm": 1000,
            "width_mm": 500,
            "thickness_mm": 19,
            "quantity": 1,
            "material": "Demo",
        }


class _AcceptSamePiece:
    DialogCode = type("DialogCode", (), {"Accepted": 1})()

    def __init__(self, *args, **kwargs):
        del args, kwargs

    def exec(self):
        return self.DialogCode.Accepted

    def piece_data(self):
        return {
            "piece_id": "A",
            "length_mm": 200,
            "width_mm": 100,
            "thickness_mm": 19,
            "quantity": 1,
            "material": "Demo",
            "rotatable": True,
        }


def test_edit_board_unchanged_shows_status(qapp, tmp_path, monkeypatch):
    del qapp
    import studio.main_window as mw

    window = _window(tmp_path)
    monkeypatch.setattr(mw, "NewBoardDialog", _AcceptSameBoard)

    window._edit_board("B1")

    assert window._tr("status.edit_unchanged") in window.statusBar().currentMessage()


def test_edit_piece_unchanged_shows_status(qapp, tmp_path, monkeypatch):
    del qapp
    import studio.main_window as mw

    window = _window(tmp_path)
    monkeypatch.setattr(mw, "NewPieceDialog", _AcceptSamePiece)

    window._edit_piece("A")

    assert window._tr("status.edit_unchanged") in window.statusBar().currentMessage()
