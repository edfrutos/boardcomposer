"""CLI: export a ``.bcproj`` plus its local revision ring to a backup folder.

Piloto DT-0006 opción D — ops backup sin SaaS (ver
``docs/masterplan/spikes/SPIKE-DT-0006-historial-cloud.md`` y DEC-0010).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from boardcomposer.io.bcproj_revisions import export_project_backup

_EPILOG = """\
Examples:
  .venv/bin/boardcomposer-backup job.bcproj --dest /mnt/backup
  python -m boardcomposer.backup_cli job.bcproj --dest /tmp/bc-backup

Notes:
  - Prefer the Studio .bcproj (not .bcstudio.json); the revision ring lives
    next to the .bcproj as .<name>.bcproj.revs/
  - After pulling new scripts: pip install -e .  (from the repo root / venv)
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="boardcomposer-backup",
        description=(
            "Copy a .bcproj and its .<name>.bcproj.revs/ ring into a stamped "
            "folder under --dest (DT-0006 option D)."
        ),
        epilog=_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "project",
        help="Path to the .bcproj file (revision ring sidecar is optional)",
    )
    parser.add_argument(
        "--dest",
        required=True,
        help="Destination directory (created if missing)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow non-.bcproj paths without prompting for a sibling .bcproj",
    )
    return parser


def _sibling_bcproj(path: Path) -> Path | None:
    """Return a same-stem ``.bcproj`` next to ``path`` when it exists."""
    name = path.name
    lower = name.lower()
    if lower.endswith(".bcstudio.json"):
        stem = name[: -len(".bcstudio.json")]
    elif lower.endswith(".bcproj"):
        return path if path.is_file() else None
    else:
        stem = path.stem

    candidate = path.parent / f"{stem}.bcproj"
    return candidate if candidate.is_file() else None


def resolve_project_path(raw: str | Path, *, force: bool = False) -> Path:
    """Return the path to back up, preferring a sibling ``.bcproj`` when needed."""
    path = Path(raw)
    if not path.is_file():
        raise FileNotFoundError(f"Project file not found: {path}")

    if path.name.lower().endswith(".bcproj") or force:
        return path

    sibling = _sibling_bcproj(path)
    if sibling is not None:
        print(
            f"note: using sibling project {sibling.name} "
            f"(revision ring belongs to .bcproj, not {path.name})",
            file=sys.stderr,
        )
        return sibling

    print(
        f"warning: {path.name} is not a .bcproj; "
        "Studio revision rings use .<name>.bcproj.revs/ next to the .bcproj. "
        "Pass the .bcproj path, or re-run with --force.",
        file=sys.stderr,
    )
    return path


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code is None else int(exc.code)

    try:
        project = resolve_project_path(args.project, force=args.force)
        folder = export_project_backup(project, args.dest)
    except (OSError, ValueError) as exc:
        print(f"backup error: {exc}", file=sys.stderr)
        return 2

    print(Path(folder))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
