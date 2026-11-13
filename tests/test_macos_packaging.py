"""Tests for macOS App Store packaging foundations."""

from __future__ import annotations

import plistlib
import sys
from pathlib import Path

from PySide6.QtGui import QAction

from boardcomposer.io.bcproj_revisions import (
    export_project_backup,
    list_revisions,
    snapshot_before_overwrite,
)
from studio.branding import APP_ICON_ICNS_PATH, app_icon
from studio.main_window import MainWindow
from studio.preferences import PreferencesManager
from studio.services import StudioServices
from studio.version import _default_root, read_package_version
from studio.whats_new import repo_root


def test_app_icon_icns_exists_and_loads(qapp):
    del qapp
    assert APP_ICON_ICNS_PATH.is_file()
    icon = app_icon()
    assert not icon.isNull()


def test_macos_menu_roles_configured(qapp, tmp_path):
    del qapp
    services = StudioServices(preferences=PreferencesManager(tmp_path / "prefs.json"))
    window = MainWindow(services)
    assert window._actions["about"].menuRole() == QAction.MenuRole.AboutRole
    assert window._actions["preferences"].menuRole() == QAction.MenuRole.PreferencesRole
    assert window._actions["exit"].menuRole() == QAction.MenuRole.QuitRole


def test_frozen_meipass_resolution(monkeypatch, tmp_path):
    fake_bundle = tmp_path / "bundle_resources"
    fake_bundle.mkdir()
    (fake_bundle / "pyproject.toml").write_text(
        '[project]\nname = "boardcomposer"\nversion = "9.8.7"\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(sys, "_MEIPASS", str(fake_bundle), raising=False)
    assert _default_root() == fake_bundle
    assert repo_root() == fake_bundle
    assert read_package_version(fake_bundle / "pyproject.toml") == "9.8.7"


def test_revisions_fallback_on_permission_error(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path / "sandbox_home"))
    project_file = tmp_path / "readonly_dir" / "cabinet.bcproj"
    project_file.parent.mkdir(parents=True)
    project_file.write_text('{"version": 6, "name": "v1"}', encoding="utf-8")

    orig_mkdir = Path.mkdir

    def guarded_mkdir(self: Path, *args, **kwargs):
        if self == project_file.parent / ".cabinet.bcproj.revs":
            raise PermissionError("App Sandbox blocks sibling hidden directory")
        return orig_mkdir(self, *args, **kwargs)

    monkeypatch.setattr(Path, "mkdir", guarded_mkdir)
    snap = snapshot_before_overwrite(project_file)
    assert snap is not None
    assert snap.is_file()
    assert ".boardcomposer/revs" in str(snap)
    revs = list_revisions(project_file)
    assert revs == [snap]

    backup_dest = tmp_path / "backups"
    stamped = export_project_backup(project_file, backup_dest)
    assert (stamped / "cabinet.bcproj").is_file()
    assert (stamped / ".cabinet.bcproj.revs" / snap.name).is_file()


def test_macos_packaging_plists_and_spec_are_valid():
    root = Path(__file__).resolve().parents[1]
    info_plist = root / "packaging" / "macos" / "Info.plist"
    mas_plist = root / "packaging" / "macos" / "entitlements.mas.plist"
    inherit_plist = root / "packaging" / "macos" / "entitlements.inherit.plist"
    spec_file = root / "packaging" / "macos" / "BoardComposer.spec"
    build_script = root / "packaging" / "macos" / "build_mas.sh"

    assert info_plist.is_file()
    assert mas_plist.is_file()
    assert inherit_plist.is_file()
    assert spec_file.is_file()
    assert build_script.is_file()

    info = plistlib.loads(info_plist.read_bytes())
    assert info["CFBundleIdentifier"] == "com.edefrutos.boardcomposer"
    assert info["CFBundleIconFile"] == "AppIcon.icns"
    assert info["ITSAppUsesNonExemptEncryption"] is False
    assert info["LSApplicationCategoryType"] == "public.app-category.productivity"

    mas = plistlib.loads(mas_plist.read_bytes())
    assert (
        mas["com.apple.application-identifier"]
        == "V29BTBRY6G.com.edefrutos.boardcomposer"
    )
    assert mas["com.apple.developer.team-identifier"] == "V29BTBRY6G"
    assert mas["com.apple.security.app-sandbox"] is True
    assert mas["com.apple.security.files.user-selected.read-write"] is True

    inherit = plistlib.loads(inherit_plist.read_bytes())
    assert inherit["com.apple.security.app-sandbox"] is True
    assert inherit["com.apple.security.inherit"] is True

    spec_text = spec_file.read_text(encoding="utf-8")
    assert "PySide6.QtWebEngine" in spec_text
