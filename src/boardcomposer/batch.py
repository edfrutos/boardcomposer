"""Headless batch solve/export for folders of CSV / ``.bcproj`` (EP-002)."""

from __future__ import annotations

import json
import traceback
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path

from boardcomposer.api import v1
from boardcomposer.export import solution_to_dxf, solution_to_pdf
from boardcomposer.integration.hooks import (
    HookConfig,
    JobHookPayload,
    dispatch_job_hooks,
    list_export_files,
    load_hook_config,
)
from boardcomposer.io.export_templates import find_export_template

_INPUT_SUFFIXES = {".csv", ".bcproj"}
_DEFAULT_FORMATS = ("json",)
_BATCH_FORMATS = {"json", "csv", "svg", "dxf", "pdf"}


@dataclass(frozen=True)
class BatchProfile:
    """Headless profile: strategy, ranking depth, and export formats."""

    strategy: str = "balanced"
    top: int = 1
    formats: tuple[str, ...] = _DEFAULT_FORMATS
    include_metrics: bool = True
    include_explanation: bool = True
    include_offcuts: bool = True

    @classmethod
    def from_dict(cls, data: dict) -> BatchProfile:
        formats = data.get("formats", list(_DEFAULT_FORMATS))
        if isinstance(formats, str):
            formats = [part.strip() for part in formats.split(",") if part.strip()]

        profile = cls(
            strategy=str(data.get("strategy", "balanced")),
            top=int(data.get("top", 1)),
            formats=tuple(formats) or _DEFAULT_FORMATS,
            include_metrics=bool(data.get("include_metrics", True)),
            include_explanation=bool(data.get("include_explanation", True)),
            include_offcuts=bool(data.get("include_offcuts", True)),
        )

        template_name = str(data.get("template", "")).strip()
        if not template_name:
            return profile
        return cls.from_named_template(
            template_name,
            client=str(data.get("client", "")),
            templates_path=data.get("templates_file"),
            strategy=profile.strategy,
            top=profile.top,
            formats_override=profile.formats if "formats" in data else None,
        )

    @classmethod
    def from_named_template(
        cls,
        name: str,
        *,
        client: str = "",
        templates_path: str | Path | None = None,
        strategy: str = "balanced",
        top: int = 1,
        formats_override: tuple[str, ...] | None = None,
    ) -> BatchProfile:
        """Build a profile from a Studio/Core named export template."""
        template = find_export_template(name, client=client, path=templates_path)
        if template is None:
            scope = f"client={client!r}" if client else "general"
            raise ValueError(f"Export template not found: {name!r} ({scope})")
        formats = formats_override or (template.format,)
        return cls(
            strategy=strategy,
            top=top,
            formats=tuple(formats) or _DEFAULT_FORMATS,
            include_metrics=template.include_metrics,
            include_explanation=template.include_explanation,
            include_offcuts=template.include_offcuts,
        )

    @classmethod
    def load(cls, path: str | Path) -> BatchProfile:
        profile_path = Path(path)
        payload = json.loads(profile_path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("Batch profile must be a JSON object")
        templates_file = payload.get("templates_file")
        if templates_file:
            templates_path = Path(str(templates_file))
            if not templates_path.is_absolute():
                payload = {
                    **payload,
                    "templates_file": str(
                        (profile_path.parent / templates_path).resolve()
                    ),
                }
        return cls.from_dict(payload)


@dataclass
class BatchJobResult:
    source: str
    status: str  # ok | error | skipped | planned
    output_dir: str | None = None
    solutions: int = 0
    error: str | None = None
    hooks: dict | None = None


@dataclass
class BatchReport:
    ok: int = 0
    error: int = 0
    skipped: int = 0
    planned: int = 0
    dry_run: bool = False
    jobs: list[BatchJobResult] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.jobs)

    def exit_code(self) -> int:
        """0 = all ok (or dry-run with plans); 1 = mixed; 2 = none ok."""
        if self.dry_run:
            if self.planned > 0 and self.error == 0:
                return 0
            if self.error > 0 and self.planned == 0:
                return 2
            if self.error > 0:
                return 1
            return 2
        if self.error == 0 and self.skipped == 0:
            return 0
        if self.ok == 0 and self.error > 0:
            return 2
        if self.error > 0:
            return 1
        return 0

    def to_dict(self) -> dict:
        return {
            "ok": self.ok,
            "error": self.error,
            "skipped": self.skipped,
            "planned": self.planned,
            "dry_run": self.dry_run,
            "total": self.total,
            "jobs": [asdict(job) for job in self.jobs],
        }


def discover_inputs(input_path: str | Path) -> list[Path]:
    """Return sorted project files from a file or directory."""
    path = Path(input_path)
    if path.is_file():
        if path.suffix.lower() not in _INPUT_SUFFIXES:
            raise ValueError(f"Unsupported input type: {path.suffix}")
        return [path]
    if not path.is_dir():
        raise FileNotFoundError(f"Input not found: {path}")

    found = [
        candidate
        for candidate in sorted(path.iterdir())
        if candidate.is_file() and candidate.suffix.lower() in _INPUT_SUFFIXES
    ]
    return found


def load_path_list(list_path: str | Path) -> list[Path]:
    """Load explicit project paths from a text file (one path per line).

    Blank lines and ``#`` comments are ignored. Relative paths resolve against
    the list file's parent directory.
    """
    path = Path(list_path)
    if not path.is_file():
        raise FileNotFoundError(f"Path list not found: {path}")

    base = path.parent
    found: list[Path] = []
    seen: set[Path] = set()
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        candidate = Path(line)
        if not candidate.is_absolute():
            candidate = (base / candidate).resolve()
        else:
            candidate = candidate.resolve()
        if candidate.suffix.lower() not in _INPUT_SUFFIXES:
            raise ValueError(f"Unsupported input type in list: {candidate}")
        if not candidate.is_file():
            raise FileNotFoundError(f"Listed input not found: {candidate}")
        if candidate not in seen:
            seen.add(candidate)
            found.append(candidate)
    return found


def resolve_inputs(
    *,
    input_path: str | Path | None = None,
    list_path: str | Path | None = None,
) -> list[Path]:
    """Union of directory/file discovery and an optional explicit path list."""
    if input_path is None and list_path is None:
        raise ValueError("Provide --input and/or --list")

    found: list[Path] = []
    seen: set[Path] = set()
    if input_path is not None:
        for path in discover_inputs(input_path):
            resolved = path.resolve()
            if resolved not in seen:
                seen.add(resolved)
                found.append(resolved)
    if list_path is not None:
        for path in load_path_list(list_path):
            resolved = path.resolve()
            if resolved not in seen:
                seen.add(resolved)
                found.append(resolved)
    return found


def _prepare_solution(solution, *, include_offcuts: bool):
    if include_offcuts:
        return solution
    return replace(solution, offcuts=())


def _write_exports(
    *,
    output_dir: Path,
    project,
    solutions: list,
    profile: BatchProfile,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    if not solutions:
        (output_dir / "NO_SOLUTIONS").write_text(
            "No valid solutions for this project.\n",
            encoding="utf-8",
        )
        return

    best = _prepare_solution(solutions[0], include_offcuts=profile.include_offcuts)
    for fmt in profile.formats:
        name = fmt.lower().strip()
        if name not in _BATCH_FORMATS:
            raise ValueError(f"Unsupported export format: {fmt}")
        if name == "json":
            (output_dir / "solution.json").write_text(
                v1.export_json(
                    best,
                    project,
                    strategy_name=profile.strategy,
                    solution_index=0,
                    include_metrics=profile.include_metrics,
                    include_explanation=profile.include_explanation,
                    include_offcuts=profile.include_offcuts,
                ),
                encoding="utf-8",
            )
        elif name == "csv":
            (output_dir / "placements.csv").write_text(
                v1.export_csv(best),
                encoding="utf-8",
            )
        elif name == "svg":
            (output_dir / "solution.svg").write_text(
                v1.export_svg(best, project),
                encoding="utf-8",
            )
        elif name == "dxf":
            (output_dir / "solution.dxf").write_text(
                solution_to_dxf(best, project),
                encoding="utf-8",
            )
        elif name == "pdf":
            (output_dir / "solution.pdf").write_bytes(solution_to_pdf(best, project))


def _dispatch_batch_hooks(
    job: BatchJobResult,
    *,
    profile: BatchProfile,
    hooks: HookConfig | None,
) -> None:
    if hooks is None or not hooks.enabled:
        return
    if job.status not in {"ok", "error"}:
        return
    payload = JobHookPayload(
        source=job.source,
        status=job.status,
        channel="batch",
        strategy=profile.strategy,
        formats=list(profile.formats),
        solutions=job.solutions,
        output_dir=job.output_dir,
        export_files=list_export_files(job.output_dir),
        error=job.error,
    )
    job.hooks = dispatch_job_hooks(payload, config=hooks).to_dict()


def run_batch(
    *,
    input_path: str | Path | None = None,
    list_path: str | Path | None = None,
    output_dir: str | Path,
    profile: BatchProfile | None = None,
    dry_run: bool = False,
    hooks: HookConfig | None = None,
) -> BatchReport:
    """Solve every discovered project and write exports under ``output_dir``.

    With ``dry_run=True``, only lists inputs and writes a planned
    ``manifest.json`` (no solve / no exports).

    When ``hooks`` is omitted, env-based ``load_hook_config()`` is used.
    Pass ``HookConfig()`` (empty) to disable hooks for a call.
    """
    profile = profile or BatchProfile()
    hook_config = load_hook_config() if hooks is None else hooks
    out_root = Path(output_dir)
    out_root.mkdir(parents=True, exist_ok=True)

    report = BatchReport(dry_run=dry_run)
    try:
        inputs = resolve_inputs(input_path=input_path, list_path=list_path)
    except (OSError, ValueError) as exc:
        report.jobs.append(
            BatchJobResult(
                source=str(input_path or list_path),
                status="error",
                error=str(exc),
            )
        )
        report.error = 1
        _write_manifest(out_root, report)
        return report

    if not inputs:
        report.jobs.append(
            BatchJobResult(
                source=str(input_path or list_path),
                status="skipped",
                error="No .csv or .bcproj files found",
            )
        )
        report.skipped = 1
        _write_manifest(out_root, report)
        return report

    if dry_run:
        for source in inputs:
            job_out = out_root / source.stem
            report.jobs.append(
                BatchJobResult(
                    source=str(source),
                    status="planned",
                    output_dir=str(job_out),
                )
            )
            report.planned += 1
        _write_manifest(out_root, report)
        return report

    for source in inputs:
        job_out = out_root / source.stem
        try:
            project = v1.load_project(source)
            solutions = v1.solve(
                project,
                strategy=profile.strategy,
                top=profile.top,
            )
            _write_exports(
                output_dir=job_out,
                project=project,
                solutions=solutions,
                profile=profile,
            )
            job = BatchJobResult(
                source=str(source),
                status="ok",
                output_dir=str(job_out),
                solutions=len(solutions),
            )
            _dispatch_batch_hooks(job, profile=profile, hooks=hook_config)
            report.jobs.append(job)
            report.ok += 1
        except Exception as exc:  # noqa: BLE001 — batch must continue
            job = BatchJobResult(
                source=str(source),
                status="error",
                output_dir=str(job_out),
                error=f"{exc}\n{traceback.format_exc()}",
            )
            report.error += 1
            job_out.mkdir(parents=True, exist_ok=True)
            (job_out / "ERROR.txt").write_text(
                f"{exc}\n\n{traceback.format_exc()}",
                encoding="utf-8",
            )
            _dispatch_batch_hooks(job, profile=profile, hooks=hook_config)
            report.jobs.append(job)

    _write_manifest(out_root, report)
    return report


def _write_manifest(out_root: Path, report: BatchReport) -> None:
    (out_root / "manifest.json").write_text(
        json.dumps(report.to_dict(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
