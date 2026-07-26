"""Post-job hooks (EP-003 SPR-002)."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from threading import Thread

from boardcomposer.batch import BatchProfile, run_batch
from boardcomposer.integration.hooks import (
    HookConfig,
    JobHookPayload,
    dispatch_job_hooks,
    load_hook_config,
)

SAMPLES = Path("data/samples")
CSV = SAMPLES / "batch_inbox" / "basic_boards.csv"


def test_load_hook_config_from_env(monkeypatch, tmp_path):
    monkeypatch.setenv("BOARDCOMPOSER_HOOK_DIR", str(tmp_path / "hooks"))
    monkeypatch.setenv("BOARDCOMPOSER_WEBHOOK_URL", "http://example.test/hook")
    monkeypatch.setenv("BOARDCOMPOSER_WEBHOOK_SECRET", "s3cret")
    cfg = load_hook_config()
    assert cfg.enabled
    assert cfg.hook_dir == tmp_path / "hooks"
    assert cfg.webhook_url == "http://example.test/hook"
    assert cfg.webhook_secret == "s3cret"


def test_dispatch_writes_folder_and_copies_exports(tmp_path):
    out = tmp_path / "job-out"
    out.mkdir()
    (out / "solution.json").write_text('{"ok": true}\n', encoding="utf-8")
    hook_root = tmp_path / "hooks"
    result = dispatch_job_hooks(
        JobHookPayload(
            source=str(CSV),
            status="ok",
            channel="batch",
            strategy="balanced",
            formats=["json"],
            solutions=1,
            output_dir=str(out),
            export_files=["solution.json"],
        ),
        config=HookConfig(hook_dir=hook_root),
    )
    assert result.folder_ok is True
    job_dir = Path(result.folder_path)
    assert (job_dir / "job.json").is_file()
    assert (job_dir / "exports" / "solution.json").is_file()
    payload = json.loads((job_dir / "job.json").read_text(encoding="utf-8"))
    assert payload["channel"] == "batch"
    assert payload["status"] == "ok"


def test_dispatch_webhook_posts_json(tmp_path):
    received: list[dict] = []

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):  # noqa: N802
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length)
            received.append(
                {
                    "secret": self.headers.get("X-BoardComposer-Secret"),
                    "payload": json.loads(body.decode("utf-8")),
                }
            )
            self.send_response(204)
            self.end_headers()

        def log_message(self, *_args):
            return

    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        result = dispatch_job_hooks(
            JobHookPayload(
                source="demo.csv",
                status="ok",
                channel="http",
                formats=["json"],
                solutions=1,
            ),
            config=HookConfig(
                webhook_url=f"http://127.0.0.1:{port}/hook",
                webhook_secret="token",
                webhook_timeout=2.0,
            ),
        )
    finally:
        server.shutdown()

    assert result.webhook_ok is True
    assert result.webhook_status == 204
    assert received[0]["secret"] == "token"
    assert received[0]["payload"]["channel"] == "http"


def test_webhook_failure_does_not_raise():
    result = dispatch_job_hooks(
        JobHookPayload(source="x.csv", status="ok", channel="batch"),
        config=HookConfig(
            webhook_url="http://127.0.0.1:1/nope",
            webhook_timeout=0.2,
        ),
    )
    assert result.webhook_ok is False
    assert result.webhook_error


def test_batch_run_records_hooks(tmp_path):
    hook_root = tmp_path / "hooks"
    out = tmp_path / "batch"
    report = run_batch(
        input_path=CSV,
        output_dir=out,
        profile=BatchProfile(formats=("json",)),
        hooks=HookConfig(hook_dir=hook_root),
    )
    assert report.ok == 1
    assert report.jobs[0].hooks is not None
    assert report.jobs[0].hooks["folder_ok"] is True
    assert any(hook_root.iterdir())
