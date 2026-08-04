from studio.explorer_actions import explorer_context_actions, parse_explorer_role
from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def test_parse_explorer_role():
    assert parse_explorer_role("piece:A") == ("piece", "A")
    assert parse_explorer_role("category:boards") == ("category", "boards")
    assert parse_explorer_role(None) is None
    assert parse_explorer_role("invalid") is None


def test_explorer_context_actions_for_piece():
    assert explorer_context_actions("piece:A") == (
        "place_on_board",
        "edit",
        "rename",
        "duplicate",
        "copy_id",
        "delete",
    )


def test_explorer_context_actions_for_board_and_categories():
    assert explorer_context_actions("project:root") == ("rename", "reveal_folder")
    assert explorer_context_actions("board:B1") == (
        "edit",
        "rename",
        "duplicate",
        "copy_id",
        "delete",
    )
    assert explorer_context_actions("category:boards") == ("add_board",)
    assert explorer_context_actions("category:pieces") == ("add_piece",)
    assert explorer_context_actions("category:solutions") == ()
    assert explorer_context_actions("solution:2") == ("preview_solution",)


def test_explorer_context_tip_keys(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)

    assert window._explorer_context_tip_key("edit", "piece:A") == "tip.edit_selection"
    assert (
        window._explorer_context_tip_key("duplicate", "board:B1")
        == "tip.duplicate_piece"
    )
    assert window._explorer_context_tip_key("delete", "piece:A") == "tip.delete_piece"
    assert (
        window._explorer_context_tip_key("copy_id", "piece:A")
        == "tip.copy_selection_id"
    )
    assert (
        window._explorer_context_tip_key("rename", "project:root")
        == "tip.rename_project"
    )
    assert (
        window._explorer_context_tip_key("rename", "piece:A") == "tip.rename_selection"
    )
    assert window._explorer_context_tip_key("add_board", "category:boards") == (
        "tip.add_board"
    )
    assert window._explorer_context_tip_key("add_piece", "category:pieces") == (
        "tip.add_piece"
    )
    assert window._explorer_context_tip_key("preview_solution", "solution:0") == (
        "tip.preview_solution"
    )
    assert window._explorer_context_tip_key("reveal_folder", "project:root") == (
        "tip.reveal_project_folder"
    )
    assert window._explorer_context_tip_key("place_on_board", "piece:A") is None
    assert window._tr("tip.preview_solution") != "tip.preview_solution"


def test_explorer_preview_tip_outdated(qapp, tmp_path):
    from boardcomposer.domain import AssemblySolution, BoardPlacement
    from studio.models import StudioBoard, StudioPiece, StudioProject

    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    project = StudioProject(
        project_id="PRJ-P",
        name="Preview",
        boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
        pieces=[StudioPiece("A", 100, 50, "Demo", 19)],
        placements=[],
    )
    services.projects.new_project(project)
    window = MainWindow(services)
    services.layout.solutions = [
        AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])
    ]
    window._mark_project_modified(reason="edit")

    assert window._explorer_context_tip_key("preview_solution", "solution:0") == (
        "tip.preview_solution_outdated"
    )
    tip = window._tr("tip.preview_solution_outdated").lower()
    assert "desactualiz" in tip or "vieja" in tip
