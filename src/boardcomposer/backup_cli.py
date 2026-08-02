"""CLI: export a ``.bcproj`` plus its local revision ring to a backup folder.

Piloto DT-0006 opción D — ops backup sin SaaS (ver
``docs/masterplan/spikes/SPIKE-DT-0006-historial-cloud.md`` y DEC-0010).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from boardcomposer.io.bcproj_revisions import export_project_backup


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="boardcomposer-backup",
        description=(
            "Copy a .bcproj and its .<name>.bcproj.revs/ ring into a stamped "
            "folder under --dest (DT-0006 option D)."
        ),
    )
    parser.add_argument("project", help="Path to the .bcproj file")
    parser.add_argument(
        "--dest",
        required=True,
        help="Destination directory (created if missing)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code is None else int(exc.code)

    try:
        folder = export_project_backup(args.project, args.dest)
    except (OSError, ValueError) as exc:
        print(f"backup error: {exc}", file=sys.stderr)
        return 2

    print(Path(folder))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
