"""Tests for Studio preferences persistence and strategy resolution."""

from boardcomposer.solver.strategies import strategy_by_name
from studio.preferences import (
    PreferencesManager,
    StudioPreferences,
    WeightPreferences,
)


def test_resolved_strategy_uses_the_named_preset_by_default():
    prefs = StudioPreferences(strategy_name="compact")

    strategy = prefs.resolved_strategy()

    assert strategy.name == "compact"
    assert strategy.weights == strategy_by_name("compact").weights


def test_resolved_strategy_applies_custom_weights_when_enabled():
    prefs = StudioPreferences(
        strategy_name="material",
        use_custom_weights=True,
        weights=WeightPreferences(
            material_utilization=11,
            placed_boards=22,
            compactness=33,
            rotation_penalty=44,
        ),
    )

    strategy = prefs.resolved_strategy()

    assert strategy.name == "material"
    assert strategy.generator_names == strategy_by_name("material").generator_names
    assert strategy.weights.material_utilization == 11
    assert strategy.weights.compactness == 33


def test_preferences_manager_round_trips_through_json(tmp_path):
    path = tmp_path / "preferences.json"
    manager = PreferencesManager(path)
    updated = StudioPreferences(
        strategy_name="exact",
        use_custom_weights=True,
        weights=WeightPreferences(
            material_utilization=50,
            placed_boards=20,
            compactness=20,
            rotation_penalty=10,
        ),
        theme="dark",
        show_grid=False,
        grid_size_mm=50,
        last_export_directory="/tmp/exports",
        window_geometry="QUJDRA==",
        window_state="U1RBVEU=",
    )

    manager.update(updated)
    reloaded = PreferencesManager(path).current

    assert reloaded == updated
    assert path.is_file()


def test_preferences_manager_ignores_blank_last_export_directory(tmp_path):
    path = tmp_path / "preferences.json"
    path.write_text(
        '{"strategy_name": "material", "last_export_directory": "  "}\n',
        encoding="utf-8",
    )
    prefs = PreferencesManager(path).current
    assert prefs.last_export_directory is None


def test_preferences_manager_ignores_blank_last_backup_directory(tmp_path):
    path = tmp_path / "preferences.json"
    path.write_text(
        '{"strategy_name": "material", "last_backup_directory": "  "}\n',
        encoding="utf-8",
    )
    prefs = PreferencesManager(path).current
    assert prefs.last_backup_directory is None


def test_preferences_manager_ignores_blank_last_import_directory(tmp_path):
    path = tmp_path / "preferences.json"
    path.write_text(
        '{"strategy_name": "material", "last_import_directory": "  "}\n',
        encoding="utf-8",
    )
    prefs = PreferencesManager(path).current
    assert prefs.last_import_directory is None


def test_preferences_manager_ignores_blank_last_project_directory(tmp_path):
    path = tmp_path / "preferences.json"
    path.write_text(
        '{"strategy_name": "material", "last_project_directory": "  "}\n',
        encoding="utf-8",
    )
    prefs = PreferencesManager(path).current
    assert prefs.last_project_directory is None


def test_preferences_manager_ignores_blank_last_diff_directory(tmp_path):
    path = tmp_path / "preferences.json"
    path.write_text(
        '{"strategy_name": "material", "last_diff_directory": "  "}\n',
        encoding="utf-8",
    )
    prefs = PreferencesManager(path).current
    assert prefs.last_diff_directory is None


def test_preferences_dialog_preserves_last_export_directory(qapp):
    del qapp
    from studio.dialogs.preferences_dialog import PreferencesDialog

    dialog = PreferencesDialog(
        StudioPreferences(language="es", last_export_directory="/exports")
    )
    dialog.max_solutions.setValue(12)
    assert dialog.preferences().last_export_directory == "/exports"
    assert dialog.preferences().max_solutions == 12


def test_preferences_dialog_preserves_last_backup_directory(qapp):
    del qapp
    from studio.dialogs.preferences_dialog import PreferencesDialog

    dialog = PreferencesDialog(
        StudioPreferences(language="es", last_backup_directory="/backups")
    )
    dialog.max_solutions.setValue(8)
    assert dialog.preferences().last_backup_directory == "/backups"
    assert dialog.preferences().max_solutions == 8


def test_preferences_dialog_preserves_last_import_directory(qapp):
    del qapp
    from studio.dialogs.preferences_dialog import PreferencesDialog

    dialog = PreferencesDialog(
        StudioPreferences(language="es", last_import_directory="/imports")
    )
    dialog.max_solutions.setValue(9)
    assert dialog.preferences().last_import_directory == "/imports"
    assert dialog.preferences().max_solutions == 9


def test_preferences_dialog_preserves_last_project_directory(qapp):
    del qapp
    from studio.dialogs.preferences_dialog import PreferencesDialog

    dialog = PreferencesDialog(
        StudioPreferences(language="es", last_project_directory="/projects")
    )
    dialog.max_solutions.setValue(10)
    assert dialog.preferences().last_project_directory == "/projects"
    assert dialog.preferences().max_solutions == 10


def test_preferences_dialog_preserves_last_diff_directory(qapp):
    del qapp
    from studio.dialogs.preferences_dialog import PreferencesDialog

    dialog = PreferencesDialog(
        StudioPreferences(language="es", last_diff_directory="/diffs")
    )
    dialog.max_solutions.setValue(11)
    assert dialog.preferences().last_diff_directory == "/diffs"
    assert dialog.preferences().max_solutions == 11


def test_preferences_manager_ignores_invalid_window_layout_payload(tmp_path):
    path = tmp_path / "preferences.json"
    path.write_text(
        '{"strategy_name": "material", "window_geometry": 123, "window_state": ""}\n',
        encoding="utf-8",
    )
    prefs = PreferencesManager(path).current
    assert prefs.window_geometry is None
    assert prefs.window_state is None


def test_preferences_manager_falls_back_on_corrupt_or_missing_files(tmp_path):
    missing = PreferencesManager(tmp_path / "missing.json")
    assert missing.current.strategy_name == "material"

    corrupt_path = tmp_path / "corrupt.json"
    corrupt_path.write_text("{not-json", encoding="utf-8")
    corrupt = PreferencesManager(corrupt_path)
    assert corrupt.current.strategy_name == "material"


def test_unknown_strategy_name_falls_back_to_material():
    prefs = StudioPreferences(strategy_name="nope")

    assert prefs.resolved_strategy().name == "material"


def test_preferences_clamp_grid_size_and_reject_unknown_theme(tmp_path):
    path = tmp_path / "preferences.json"
    path.write_text(
        '{"theme": "neon", "grid_size_mm": 9999, "show_grid": false, '
        '"max_solutions": 999}',
        encoding="utf-8",
    )

    prefs = PreferencesManager(path).current

    assert prefs.theme == "system"
    assert prefs.grid_size_mm == 500
    assert prefs.show_grid is False
    assert prefs.max_solutions == 100


def test_preferences_dialog_exposes_advanced_max_solutions(qapp):
    del qapp
    from studio.dialogs.preferences_dialog import PreferencesDialog

    dialog = PreferencesDialog(StudioPreferences(max_solutions=5, language="en"))
    assert dialog.advanced.title() == "Advanced / performance"
    assert dialog.max_solutions.value() == 5
    dialog.max_solutions.setValue(8)
    assert dialog.preferences().max_solutions == 8


def test_preferences_dialog_labels_follow_language(qapp):
    del qapp
    from studio.dialogs.preferences_dialog import PreferencesDialog

    dialog = PreferencesDialog(StudioPreferences(language="en"))
    assert dialog.use_custom_weights.text() == "Use custom weights"
    assert dialog._weight_material_label.text() == "Material utilization:"
    assert dialog.export_include_offcuts.text() == "Include offcuts"
    assert "Material first" in [
        dialog.strategy.itemText(i) for i in range(dialog.strategy.count())
    ]
    assert "System" in [dialog.theme.itemText(i) for i in range(dialog.theme.count())]

    dialog.language.setCurrentIndex(dialog.language.findData("es"))
    assert dialog.use_custom_weights.text() == "Usar pesos personalizados"
    assert dialog._weight_material_label.text() == "Aprovechamiento de material:"
    assert dialog.export_include_offcuts.text() == "Incluir retales"
    assert "Material primero" in [
        dialog.strategy.itemText(i) for i in range(dialog.strategy.count())
    ]


def test_apply_theme_switches_palette(qapp):
    from PySide6.QtGui import QColor

    from studio.theme import apply_theme
    from studio.theme_tokens import DARK, LIGHT

    apply_theme(qapp, "dark")
    dark_window = qapp.palette().color(qapp.palette().ColorRole.Window)
    dark_accent = qapp.palette().color(qapp.palette().ColorRole.Highlight)
    assert dark_window.name() == QColor(DARK.window).name()
    assert dark_accent.name() == QColor(DARK.accent).name()
    assert qapp.styleSheet()

    apply_theme(qapp, "light")
    light_window = qapp.palette().color(qapp.palette().ColorRole.Window)
    light_accent = qapp.palette().color(qapp.palette().ColorRole.Highlight)
    light_highlight_text = qapp.palette().color(
        qapp.palette().ColorRole.HighlightedText
    )
    assert light_window.name() == QColor(LIGHT.window).name()
    assert light_accent.name() == QColor(LIGHT.accent).name()
    assert light_highlight_text.name() == QColor(LIGHT.accent_text).name()
    assert LIGHT.accent_text == "#1a1410"
    sheet = qapp.styleSheet()
    assert "primaryButton" in sheet
    assert "QPushButton:focus" in sheet
    assert "welcomeClearRecent" in sheet
    assert "QDockWidget::title" in sheet
    assert "workspaceEmptyOverlay" in sheet
    assert "inspectorPanel" in sheet
    assert "QDialogButtonBox QPushButton" in sheet
    assert "exportGraphicPreview" in sheet
    assert dark_window.lightness() < light_window.lightness()

    apply_theme(qapp, "system")
    system_sheet = qapp.styleSheet()
    assert "welcomeBrand" in system_sheet
    assert "primaryButton" not in system_sheet
    assert "QDockWidget::title" not in system_sheet


def test_layout_service_uses_preferences_strategy(tmp_path):
    from studio.layout_service import LayoutService
    from studio.preferences import PreferencesManager
    from studio.services import StudioServices

    services = StudioServices()
    services.preferences = PreferencesManager(tmp_path / "prefs.json")
    services.preferences.update(StudioPreferences(strategy_name="compact"))
    layout = LayoutService(services)

    assert layout._resolve_strategy().name == "compact"


def test_layout_service_truncates_to_max_solutions(tmp_path):
    from studio.preferences import PreferencesManager
    from studio.services import StudioServices
    from studio.models import StudioBoard, StudioPiece, StudioProject

    services = StudioServices()
    services.preferences = PreferencesManager(tmp_path / "prefs.json")
    services.preferences.update(StudioPreferences(max_solutions=1))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Limit",
            boards=[StudioBoard("TAB", 2000, 1000)],
            pieces=[
                StudioPiece("A", 400, 300),
                StudioPiece("B", 500, 300),
                StudioPiece("C", 600, 200),
            ],
        )
    )

    solution = services.layout.solve_current_project()
    assert solution is not None
    assert len(services.layout.solutions) == 1
