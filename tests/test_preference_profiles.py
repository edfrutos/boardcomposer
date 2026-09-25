"""Named local preference profiles (IDE-0054)."""

import json

import pytest

from studio.dialogs.preferences_dialog import PreferencesDialog
from studio.preference_profiles import (
    PreferenceProfilesManager,
    preferences_from_profile,
)
from studio.preferences import StudioPreferences


def test_save_apply_and_delete_profile(tmp_path):
    manager = PreferenceProfilesManager(path=tmp_path / "profiles.json", autoload=False)
    saved = manager.save_profile(
        "Fino",
        StudioPreferences(units="cm", default_material="MDF"),
    )
    assert saved.name == "Fino"
    assert saved.preferences["units"] == "cm"
    assert "window_geometry" not in saved.preferences
    reloaded = PreferenceProfilesManager(path=tmp_path / "profiles.json")
    assert reloaded.names() == ["Fino"]
    current = StudioPreferences(last_project_directory="/taller")
    applied = preferences_from_profile(current, reloaded.get("Fino").preferences)
    assert applied.units == "cm"
    assert applied.default_material == "MDF"
    assert applied.last_project_directory == "/taller"
    assert manager.delete("fino") is True
    assert manager.names() == []


def test_blank_profile_name_rejected(tmp_path):
    manager = PreferenceProfilesManager(path=tmp_path / "profiles.json", autoload=False)
    with pytest.raises(ValueError):
        manager.save_profile("  ", StudioPreferences())


def test_dialog_apply_profile_does_not_persist_until_ok(qapp, tmp_path, monkeypatch):
    del qapp
    monkeypatch.setattr(
        "studio.dialogs.preferences_dialog.QMessageBox.information",
        lambda *args, **kwargs: None,
    )
    manager = PreferenceProfilesManager(path=tmp_path / "profiles.json", autoload=False)
    manager.save_profile("Métrico", StudioPreferences(units="cm", language="es"))
    dialog = PreferencesDialog(
        StudioPreferences(units="mm", language="es"),
        profiles=manager,
    )
    index = dialog.profile_combo.findData("Métrico")
    dialog.profile_combo.setCurrentIndex(index)
    dialog._apply_profile()
    assert dialog.preferences().units == "cm"
    raw = json.loads((tmp_path / "profiles.json").read_text(encoding="utf-8"))
    assert raw["profiles"][0]["preferences"]["units"] == "cm"
