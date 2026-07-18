"""Tests for opening/revealing exported files (FLW-005)."""

from pathlib import Path

from studio.events.catalog import CATALOG, EXPORT_FAILED, EXPORT_STARTED
from studio.file_reveal import open_local_path, reveal_in_file_manager


def test_export_started_and_failed_are_in_catalog():
    assert EXPORT_STARTED in CATALOG
    assert EXPORT_FAILED in CATALOG


def test_open_local_path_rejects_missing_file(tmp_path, monkeypatch):
    calls: list[str] = []

    monkeypatch.setattr(
        "PySide6.QtGui.QDesktopServices.openUrl",
        lambda url: calls.append(url.toLocalFile()) or True,
    )

    assert open_local_path(tmp_path / "missing.txt") is False
    assert calls == []


def test_open_local_path_opens_existing_file(tmp_path, monkeypatch):
    target = tmp_path / "out.svg"
    target.write_text("<svg/>", encoding="utf-8")
    calls: list[str] = []

    monkeypatch.setattr(
        "PySide6.QtGui.QDesktopServices.openUrl",
        lambda url: calls.append(url.toLocalFile()) or True,
    )

    assert open_local_path(target) is True
    assert calls == [str(target.resolve())]


def test_reveal_in_file_manager_opens_parent_folder(tmp_path, monkeypatch):
    target = tmp_path / "out.svg"
    target.write_text("<svg/>", encoding="utf-8")
    calls: list[str] = []

    monkeypatch.setattr(
        "PySide6.QtGui.QDesktopServices.openUrl",
        lambda url: calls.append(url.toLocalFile()) or True,
    )

    assert reveal_in_file_manager(target) is True
    assert calls == [str(Path(tmp_path).resolve())]
