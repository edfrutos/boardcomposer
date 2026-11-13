# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller specification for BoardComposer Studio (macOS / Mac App Store)."""

from pathlib import Path
import plistlib

REPO_ROOT = Path(SPECPATH).resolve().parents[1]
INFO_PLIST_PATH = Path(SPECPATH).resolve() / "Info.plist"

with INFO_PLIST_PATH.open("rb") as fp:
    INFO_PLIST = plistlib.load(fp)

EXCLUDED_MODULES = [
    "tkinter",
    "matplotlib",
    "scipy",
    "pytest",
    "ruff",
    "mypy",
    "pylint",
    "flake8",
    "flask",
    "PySide6.QtWebEngine",
    "PySide6.QtWebEngineCore",
    "PySide6.QtWebEngineWidgets",
    "PySide6.QtWebChannel",
    "PySide6.QtQml",
    "PySide6.QtQuick",
    "PySide6.QtQuickWidgets",
    "PySide6.Qt3DCore",
    "PySide6.Qt3DRender",
    "PySide6.Qt3DInput",
    "PySide6.Qt3DLogic",
    "PySide6.Qt3DExtras",
    "PySide6.Qt3DAnimation",
    "PySide6.QtMultimedia",
    "PySide6.QtMultimediaWidgets",
    "PySide6.QtBluetooth",
    "PySide6.QtNfc",
    "PySide6.QtPositioning",
    "PySide6.QtRemoteObjects",
    "PySide6.QtSensors",
    "PySide6.QtSerialPort",
    "PySide6.QtSerialBus",
    "PySide6.QtSql",
    "PySide6.QtTest",
    "PySide6.QtWebSockets",
]

DATAS = [
    (str(REPO_ROOT / "pyproject.toml"), "."),
    (str(REPO_ROOT / "CHANGELOG.md"), "."),
    (str(REPO_ROOT / "README.md"), "."),
    (str(REPO_ROOT / "docs" / "README.md"), "docs"),
    (str(REPO_ROOT / "docs" / "DESIGN.md"), "docs"),
    (str(REPO_ROOT / "docs" / "user" / "GUIA-RAPIDA.md"), "docs/user"),
    (str(REPO_ROOT / "docs" / "masterplan" / "INDEX.md"), "docs/masterplan"),
    (str(REPO_ROOT / "studio" / "assets"), "studio/assets"),
    (str(REPO_ROOT / "data" / "samples"), "data/samples"),
]

a = Analysis(
    [str(REPO_ROOT / "studio" / "app.py")],
    pathex=[str(REPO_ROOT / "src"), str(REPO_ROOT)],
    binaries=[],
    datas=DATAS,
    hiddenimports=["boardcomposer", "studio"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=EXCLUDED_MODULES,
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="BoardComposer",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="BoardComposer",
)

app = BUNDLE(
    coll,
    name="BoardComposer.app",
    icon=str(REPO_ROOT / "studio" / "assets" / "AppIcon.icns"),
    bundle_identifier="com.edfdeveloper.boardcomposer",
    version=INFO_PLIST.get("CFBundleShortVersionString", "0.4.4"),
    info_plist=INFO_PLIST,
)
