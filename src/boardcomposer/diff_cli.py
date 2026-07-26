"""CLI: structural diff between two ``.bcproj`` files."""

from __future__ import annotations

import argparse
import json
import sys

from boardcomposer.io.bcproj_diff import diff_bcproj


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="boardcomposer-diff",
        description="Compare two .bcproj revisions (inventory, pieces, placements).",
    )
    parser.add_argument("left", help="Left / baseline .bcproj")
    parser.add_argument("right", help="Right / candidate .bcproj")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of a text summary",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code is None else int(exc.code)

    try:
        report = diff_bcproj(args.left, args.right)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"diff error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
    else:
        print("\n".join(report.summary_lines()))
    return 0 if report.identical else 1


if __name__ == "__main__":
    raise SystemExit(main())
