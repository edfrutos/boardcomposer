"""Local revision ring for ``.bcproj`` files (FLW-006).

Before overwriting a project file, Studio copies the previous bytes into a
sidecar folder ``.<name>.bcproj.revs/`` next to the file. Keeps the newest
``MAX_REVISIONS`` snapshots so the diff UI can compare against recent saves
without a full VCS.
"""

from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path

MAX_REVISIONS = 10


def revisions_dir(path: str | Path) -> Path:
    """Sidecar directory for snapshots of ``path``."""
    target = Path(path)
    return target.parent / f".{target.name}.revs"


def list_revisions(path: str | Path) -> list[Path]:
    """Return saved revisions newest-first (missing dir → empty)."""
    folder = revisions_dir(path)
    if not folder.is_dir():
        return []
    files = [p for p in folder.glob("*.bcproj") if p.is_file()]
    files.sort(key=lambda p: p.name, reverse=True)
    return files


def latest_revision(path: str | Path) -> Path | None:
    revisions = list_revisions(path)
    return revisions[0] if revisions else None


def snapshot_before_overwrite(
    path: str | Path,
    *,
    keep: int = MAX_REVISIONS,
) -> Path | None:
    """Copy ``path`` into the revisions ring if it already exists on disk.

    Returns the new snapshot path, or ``None`` when there was nothing to copy.
    """
    target = Path(path)
    if not target.is_file():
        return None

    folder = revisions_dir(target)
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest = folder / f"{stamp}.bcproj"
    # Avoid clobbering if two saves share the same UTC second.
    if dest.exists():
        dest = folder / f"{stamp}_{target.stat().st_mtime_ns}.bcproj"
    shutil.copy2(target, dest)
    _prune(folder, keep=keep)
    return dest


def _prune(folder: Path, *, keep: int) -> None:
    if keep < 1:
        return
    files = [p for p in folder.glob("*.bcproj") if p.is_file()]
    files.sort(key=lambda p: p.name, reverse=True)
    for stale in files[keep:]:
        try:
            stale.unlink()
        except OSError:
            pass


def export_project_backup(
    project_path: str | Path,
    destination_dir: str | Path,
) -> Path:
    """Copy ``.bcproj`` and its local revision ring into a stamped backup folder.

    Layout::

        destination_dir/<stem>-<UTC>/
            <name>.bcproj
            .<name>.bcproj.revs/   # only if the sidecar exists

    Returns the created backup folder. Raises ``FileNotFoundError`` if the
    project file is missing, ``NotADirectoryError`` if destination cannot be
    used as a directory.
    """
    source = Path(project_path)
    if not source.is_file():
        raise FileNotFoundError(f"Project file not found: {source}")

    dest_root = Path(destination_dir)
    dest_root.mkdir(parents=True, exist_ok=True)
    if not dest_root.is_dir():
        raise NotADirectoryError(f"Backup destination is not a directory: {dest_root}")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    folder = dest_root / f"{source.stem}-{stamp}"
    folder.mkdir(parents=False, exist_ok=False)

    shutil.copy2(source, folder / source.name)
    ring = revisions_dir(source)
    if ring.is_dir():
        shutil.copytree(ring, folder / ring.name)
    return folder
