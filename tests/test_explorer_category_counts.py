"""Explorer category headers show inventory counts."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeWidgetItem

from studio.i18n import tr
from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _category_labels(root: QTreeWidgetItem) -> dict[str, str]:
    labels: dict[str, str] = {}
    for index in range(root.childCount()):
        child = root.child(index)
        role = child.data(0, Qt.ItemDataRole.UserRole)
        if isinstance(role, str) and role.startswith("category:"):
            labels[role.removeprefix("category:")] = child.text(0)
    return labels


def test_explorer_category_count_i18n_keys():
    assert tr("explorer.boards", "es", n=3) == "Tableros (3)"
    assert tr("explorer.pieces", "en", n=0) == "Pieces (0)"
    assert tr("explorer.solutions", "es", n=2) == "Soluciones (2)"


def test_explorer_headers_include_counts(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Counts",
            boards=[
                StudioBoard("B1", 3000, 1000, "Demo", 19, 1),
                StudioBoard("B2", 2800, 900, "Demo", 19, 2),
            ],
            pieces=[StudioPiece("A", 400, 300, "Demo", 19)],
            placements=[],
        )
    )

    window = MainWindow(services)
    root = window.explorer.topLevelItem(0)
    assert root is not None
    labels = _category_labels(root)

    assert labels["boards"] == "Tableros (2)"
    assert labels["pieces"] == "Piezas (1)"
    assert labels["solutions"] == "Soluciones (0)"
