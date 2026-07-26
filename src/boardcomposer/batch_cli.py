"""CLI entry for headless batch jobs (EP-002)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from boardcomposer.batch import BatchProfile, run_batch


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="boardcomposer-batch",
        description=(
            "Solve a folder (or file) of CSV / .bcproj projects and export "
            "results without Studio/Qt."
        ),
    )
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Input file (.csv / .bcproj) or directory containing them",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Output directory (creates per-project subfolders + manifest.json)",
    )
    parser.add_argument(
        "--profile",
        "-p",
        help="Optional JSON profile (strategy, top, formats)",
    )
    parser.add_argument(
        "--strategy",
        choices=["balanced", "material", "compact", "exact"],
        help="Override profile strategy",
    )
    parser.add_argument(
        "--top",
        type=int,
        help="Override profile max solutions to keep (exports best)",
    )
    parser.add_argument(
        "--formats",
        help="Override export formats, comma-separated: json,csv,svg",
    )
    return parser


def _resolve_profile(args: argparse.Namespace) -> BatchProfile:
    profile = BatchProfile.load(args.profile) if args.profile else BatchProfile()
    strategy = args.strategy or profile.strategy
    top = profile.top if args.top is None else args.top
    if args.formats:
        formats = tuple(
            part.strip() for part in args.formats.split(",") if part.strip()
        )
    else:
        formats = profile.formats
    return BatchProfile(strategy=strategy, top=top, formats=formats or ("json",))


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        profile = _resolve_profile(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Profile error: {exc}", file=sys.stderr)
        return 2

    report = run_batch(
        input_path=args.input,
        output_dir=args.output,
        profile=profile,
    )
    manifest = Path(args.output) / "manifest.json"
    print(
        f"batch done: ok={report.ok} error={report.error} "
        f"skipped={report.skipped} total={report.total}"
    )
    print(f"manifest: {manifest}")
    return report.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
