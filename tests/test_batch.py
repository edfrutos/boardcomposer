"""Headless batch jobs (EP-002)."""

from __future__ import annotations

import json
from pathlib import Path

from boardcomposer.batch import (
    BatchProfile,
    discover_inputs,
    load_path_list,
    resolve_inputs,
    run_batch,
)
from boardcomposer.batch_cli import main as batch_main


SAMPLES = Path("data/samples")
BATCH_INBOX = SAMPLES / "batch_inbox"
BATCH_LIST = SAMPLES / "batch_jobs.list"


def test_discover_inputs_from_directory():
    found = discover_inputs(BATCH_INBOX)
    suffixes = {path.suffix.lower() for path in found}
    assert ".csv" in suffixes
    assert ".bcproj" in suffixes
    assert all(path.is_file() for path in found)


def test_load_path_list_resolves_relative_and_comments():
    found = load_path_list(BATCH_LIST)
    assert len(found) == 2
    stems = {path.stem for path in found}
    assert stems == {"basic_boards", "multipanel_demo"}


def test_resolve_inputs_unions_input_and_list(tmp_path):
    listing = tmp_path / "jobs.list"
    listing.write_text(
        f"{(SAMPLES / 'multipanel_demo.bcproj').resolve()}\n",
        encoding="utf-8",
    )
    found = resolve_inputs(
        input_path=BATCH_INBOX / "basic_boards.csv",
        list_path=listing,
    )
    stems = {path.stem for path in found}
    assert stems == {"basic_boards", "multipanel_demo"}


def test_run_batch_writes_exports_and_manifest(tmp_path):
    out = tmp_path / "batch-out"
    report = run_batch(
        input_path=BATCH_INBOX / "basic_boards.csv",
        output_dir=out,
        profile=BatchProfile(strategy="balanced", top=1, formats=("json", "csv")),
    )

    assert report.ok == 1
    assert report.error == 0
    assert report.exit_code() == 0
    job_dir = out / "basic_boards"
    assert (job_dir / "solution.json").is_file()
    assert (job_dir / "placements.csv").is_file()
    manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["ok"] == 1
    assert manifest["jobs"][0]["status"] == "ok"


def test_run_batch_dry_run_plans_without_exports(tmp_path):
    out = tmp_path / "dry-out"
    report = run_batch(
        list_path=BATCH_LIST,
        output_dir=out,
        dry_run=True,
    )

    assert report.dry_run is True
    assert report.planned == 2
    assert report.ok == 0
    assert report.exit_code() == 0
    assert not (out / "basic_boards").exists()
    assert not (out / "multipanel_demo").exists()
    manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["dry_run"] is True
    assert manifest["planned"] == 2
    assert {job["status"] for job in manifest["jobs"]} == {"planned"}


def test_run_batch_continues_after_error(tmp_path):
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    (inbox / "good.csv").write_text(
        "id,length_mm,width_mm,thickness_mm\nA,100,50,19\n",
        encoding="utf-8",
    )
    (inbox / "bad.csv").write_text(
        "id,length_mm\nA,100\n",
        encoding="utf-8",
    )

    out = tmp_path / "out"
    report = run_batch(
        input_path=inbox,
        output_dir=out,
        profile=BatchProfile(formats=("json",)),
    )

    assert report.ok == 1
    assert report.error == 1
    assert report.exit_code() == 1
    assert (out / "bad" / "ERROR.txt").is_file()
    assert (out / "manifest.json").is_file()


def test_batch_profile_load(tmp_path):
    path = tmp_path / "profile.json"
    path.write_text(
        json.dumps({"strategy": "material", "top": 2, "formats": "json,svg"}),
        encoding="utf-8",
    )
    profile = BatchProfile.load(path)
    assert profile.strategy == "material"
    assert profile.top == 2
    assert profile.formats == ("json", "svg")


def test_batch_cli_main_success(tmp_path):
    # Prefer tracked sample under data/samples/ (not only batch_inbox copy).
    bcproj = SAMPLES / "multipanel_demo.bcproj"
    assert bcproj.is_file(), f"missing sample {bcproj}"
    out = tmp_path / "cli-out"
    code = batch_main(
        [
            "--input",
            str(bcproj),
            "--output",
            str(out),
            "--formats",
            "json",
        ]
    )
    assert code == 0
    assert (out / "multipanel_demo" / "solution.json").is_file()


def test_batch_cli_list_and_dry_run(tmp_path):
    out = tmp_path / "cli-dry"
    code = batch_main(
        [
            "--list",
            str(BATCH_LIST),
            "--output",
            str(out),
            "--dry-run",
        ]
    )
    assert code == 0
    assert (out / "manifest.json").is_file()
    assert not any(out.glob("*/solution.json"))


def test_batch_cli_requires_input_or_list(tmp_path):
    code = batch_main(["--output", str(tmp_path / "o")])
    assert code == 2


def test_batch_cli_missing_profile(tmp_path):
    code = batch_main(
        [
            "--input",
            str(BATCH_INBOX / "basic_boards.csv"),
            "--output",
            str(tmp_path / "o"),
            "--profile",
            str(tmp_path / "missing.json"),
        ]
    )
    assert code == 2
