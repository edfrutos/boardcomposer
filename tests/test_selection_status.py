"""Status bar shows how many Workspace pieces are selected (IDE-0063)."""

from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from tests.test_copy_selection_id import _window


def test_selection_status_hidden_until_pieces_are_selected(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    assert window._selection_label.text() == ""
    assert window._selection_label.isHidden()

    window.workspace.select_piece("A")
    assert window._selection_label.text() == "1 sel."
    assert not window._selection_label.isHidden()
    assert "seleccionadas" in window._selection_label.toolTip().casefold()
    assert "1" in window._selection_label.toolTip()

    window.workspace.clear_piece_selection()
    assert window._selection_label.text() == ""
    assert window._selection_label.toolTip() == ""
    assert window._selection_label.isHidden()


def test_selection_status_counts_many_and_follows_language(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    project = StudioProject(
        project_id="PRJ-2",
        name="Dos",
        boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
        pieces=[
            StudioPiece("A", 200, 100, "Demo", 19),
            StudioPiece("B", 180, 90, "Demo", 19),
        ],
        placements=[
            StudioPlacement("A", 10, 20, False, 0, "B1", 0, 0),
            StudioPlacement("B", 220, 20, False, 0, "B1", 0, 0),
        ],
    )
    window.services.projects.new_project(project)
    window.workspace.reload_project()
    window.services.preferences.update(
        window.services.preferences.current.__class__(language="en")
    )
    window._retranslate_ui()
    window.workspace.select_pieces(["A", "B"])
    assert window._selection_label.text() == "2 sel."
    assert "selected pieces" in window._selection_label.toolTip().casefold()
