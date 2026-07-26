"""Headless batch solve/export for folders of CSV / ``.bcproj`` (EP-002)."""

from __future__ import annotations

import json
import traceback
from dataclasses import asdict, dataclass, field
from pathlib import Path

from boardcomposer.api import v1

_INPUT_SUFFIXES = {".csv", ".bcproj"}
_DEFAULT_FORMATS = ("json",)


@dataclass(frozen=True)
class BatchProfile:
    """Headless profile: strategy, ranking depth, and export formats."""

    strategy: str = "balanced"
    top: int = 1
    formats: tuple[str, ...] = _DEFAULT_FORMATS

    @classmethod
    def from_dict(cls, data: dict) -> BatchProfile:
        formats = data.get("formats", list(_DEFAULT_FORMATS))
        if isinstance(formats, str):
            formats = [part.strip() for part in formats.split(",") if part.strip()]
        return cls(
            strategy=str(data.get("strategy", "balanced")),
            top=int(data.get("top", 1)),
            formats=tuple(formats) or _DEFAULT_FORMATS,
        )

    @classmethod
    def load(cls, path: str | Path) -> BatchProfile:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("Batch profile must be a JSON object")
        return cls.from_dict(payload)


@dataclass
class BatchJobResult:
    source: str
    status: str  # ok | error | skipped | planned
    output_dir: str | None = None
    solutions: int = 0
    error: str | None = None


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


def _write_exports(
    *,
    output_dir: Path,
    project,
    solutions: list,
    strategy: str,
    formats: tuple[str, ...],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    if not solutions:
        (output_dir / "NO_SOLUTIONS").write_text(
            "No valid solutions for this project.\n",
            encoding="utf-8",
        )
        return

    best = solutions[0]
    for fmt in formats:
        name = fmt.lower().strip()
        if name == "json":
            (output_dir / "solution.json").write_text(
                v1.export_json(
                    best,
                    project,
                    strategy_name=strategy,
                    solution_index=0,
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
        else:
            raise ValueError(f"Unsupported export format: {fmt}")


def run_batch(
    *,
    input_path: str | Path | None = None,
    list_path: str | Path | None = None,
    output_dir: str | Path,
    profile: BatchProfile | None = None,
    dry_run: bool = False,
) -> BatchReport:
    """Solve every discovered project and write exports under ``output_dir``.

    With ``dry_run=True``, only lists inputs and writes a planned
    ``manifest.json`` (no solve / no exports).
    """
    profile = profile or BatchProfile()
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
                strategy=profile.strategy,
                formats=profile.formats,
            )
            report.jobs.append(
                BatchJobResult(
                    source=str(source),
                    status="ok",
                    output_dir=str(job_out),
                    solutions=len(solutions),
                )
            )
            report.ok += 1
        except Exception as exc:  # noqa: BLE001 — batch must continue
            report.jobs.append(
                BatchJobResult(
                    source=str(source),
                    status="error",
                    output_dir=str(job_out),
                    error=f"{exc}\n{traceback.format_exc()}",
                )
            )
            report.error += 1
            job_out.mkdir(parents=True, exist_ok=True)
            (job_out / "ERROR.txt").write_text(
                f"{exc}\n\n{traceback.format_exc()}",
                encoding="utf-8",
            )

    _write_manifest(out_root, report)
    return report


def _write_manifest(out_root: Path, report: BatchReport) -> None:
    (out_root / "manifest.json").write_text(
        json.dumps(report.to_dict(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
