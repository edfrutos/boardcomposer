"""After solve, Comparador comes forward and status points to export."""

from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es", max_solutions=20))
    return MainWindow(services)


def test_reveal_comparator_shows_and_raises_dock(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.show()
    window.solutions_dock.hide()
    raised: list[object] = []
    window._raise_dock = raised.append  # type: ignore[method-assign]

    window._reveal_comparator_after_solve()

    assert window.solutions_dock.isVisible()
    assert raised == [window.solutions_dock]


def test_layout_ok_status_mentions_export(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.layout.stats.accepted = 5
    window._announce_layout_ok(shown=5)
    message = window.statusBar().currentMessage()
    assert "5 soluciones" in message
    assert "Ctrl+Shift+E" in message
    assert "Re/Av Pág" in message
    assert "Fijar referencia" in message


def test_calculate_layout_first_mentions_export_path():
    from studio.i18n import tr

    es = tr("status.calculate_layout_first", "es")
    assert "Ctrl+Return" in es
    assert "Ctrl+Shift+E" in es
    en = tr("status.calculate_layout_first", "en")
    assert "Ctrl+Return" in en
    assert "Ctrl+Shift+E" in en


def test_pin_reference_button_has_tooltip(qapp, tmp_path):
    del qapp
    from boardcomposer.domain import AssemblySolution, BoardPlacement

    window = _window(tmp_path)
    empty_tip = window.pin_reference_button.toolTip()
    assert "calcula un layout" in empty_tip.lower()

    sol = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 10, 10)])
    window.services.layout.solutions = [sol, sol]
    window._sync_solution_actions()
    tip = window.pin_reference_button.toolTip()
    assert "≥2" in tip or "2" in tip
