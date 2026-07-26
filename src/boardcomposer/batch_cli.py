"""CLI entry for headless batch jobs (EP-002)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from boardcomposer.batch import BatchProfile, run_batch
from boardcomposer.io.export_templates import default_export_templates_path


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
        help="Input file (.csv / .bcproj) or directory containing them",
    )
    parser.add_argument(
        "--list",
        "-L",
        dest="list_path",
        help=(
            "Text file with explicit project paths (one per line; "
            "# comments allowed). Can combine with --input."
        ),
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
        help="Optional JSON profile (strategy, top, formats, template, …)",
    )
    parser.add_argument(
        "--template",
        "-t",
        help="Named Studio export template (format + include_* flags)",
    )
    parser.add_argument(
        "--client",
        help="Client scope for --template (default: general / empty client)",
    )
    parser.add_argument(
        "--templates-file",
        help=(
            "Path to export_templates.json or share pack "
            f"(default: {default_export_templates_path()})"
        ),
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
        help="Override export formats, comma-separated: json,csv,svg,dxf,pdf",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List planned jobs and write manifest only (no solve/export)",
    )
    return parser


def _resolve_profile(args: argparse.Namespace) -> BatchProfile:
    if args.profile:
        profile = BatchProfile.load(args.profile)
    elif args.template:
        profile = BatchProfile.from_named_template(
            args.template,
            client=args.client or "",
            templates_path=args.templates_file,
        )
    else:
        profile = BatchProfile()

    if args.template and args.profile:
        # CLI --template wins over bare profile fields for export options.
        named = BatchProfile.from_named_template(
            args.template,
            client=args.client or "",
            templates_path=args.templates_file,
            strategy=profile.strategy,
            top=profile.top,
        )
        profile = named

    strategy = args.strategy or profile.strategy
    top = profile.top if args.top is None else args.top
    if args.formats:
        formats = tuple(
            part.strip() for part in args.formats.split(",") if part.strip()
        )
    else:
        formats = profile.formats
    return BatchProfile(
        strategy=strategy,
        top=top,
        formats=formats or ("json",),
        include_metrics=profile.include_metrics,
        include_explanation=profile.include_explanation,
        include_offcuts=profile.include_offcuts,
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        if not args.input and not args.list_path:
            parser.error("Provide --input and/or --list")
    except SystemExit as exc:
        code = 0 if exc.code is None else int(exc.code)
        return code

    try:
        profile = _resolve_profile(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Profile error: {exc}", file=sys.stderr)
        return 2

    report = run_batch(
        input_path=args.input,
        list_path=args.list_path,
        output_dir=args.output,
        profile=profile,
        dry_run=args.dry_run,
    )
    manifest = Path(args.output) / "manifest.json"
    if args.dry_run:
        print(
            f"batch dry-run: planned={report.planned} error={report.error} "
            f"skipped={report.skipped} total={report.total}"
        )
        for job in report.jobs:
            print(f"  {job.status}: {job.source} -> {job.output_dir}")
    else:
        print(
            f"batch done: ok={report.ok} error={report.error} "
            f"skipped={report.skipped} total={report.total}"
        )
    print(f"manifest: {manifest}")
    return report.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
