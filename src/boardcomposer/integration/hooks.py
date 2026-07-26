"""Post-job hooks: drop folder + optional webhook (EP-003 SPR-002).

Hook failures never raise to the caller — jobs must remain successful even
when a remote ERP endpoint is down. Credentials live in env/config only.
"""

from __future__ import annotations

import json
import os
import shutil
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from boardcomposer.api import v1

ENV_HOOK_DIR = "BOARDCOMPOSER_HOOK_DIR"
ENV_WEBHOOK_URL = "BOARDCOMPOSER_WEBHOOK_URL"
ENV_WEBHOOK_SECRET = "BOARDCOMPOSER_WEBHOOK_SECRET"
ENV_WEBHOOK_TIMEOUT = "BOARDCOMPOSER_WEBHOOK_TIMEOUT"
_DEFAULT_TIMEOUT = 5.0


@dataclass(frozen=True)
class HookConfig:
    """Where to deliver post-job notifications."""

    hook_dir: Path | None = None
    webhook_url: str | None = None
    webhook_secret: str | None = None
    webhook_timeout: float = _DEFAULT_TIMEOUT
    copy_exports: bool = True

    @property
    def enabled(self) -> bool:
        return self.hook_dir is not None or bool(self.webhook_url)


@dataclass
class JobHookPayload:
    """JSON-serializable summary of one finished job."""

    source: str
    status: str
    channel: str  # batch | http
    strategy: str = "balanced"
    formats: list[str] = field(default_factory=list)
    solutions: int = 0
    output_dir: str | None = None
    export_files: list[str] = field(default_factory=list)
    error: str | None = None
    api_version: str = v1.API_VERSION
    job_id: str = field(default_factory=lambda: uuid4().hex[:12])
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class HookDispatchResult:
    folder_ok: bool | None = None
    folder_path: str | None = None
    folder_error: str | None = None
    webhook_ok: bool | None = None
    webhook_status: int | None = None
    webhook_error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_hook_config(
    *,
    hook_dir: str | Path | None = None,
    webhook_url: str | None = None,
    webhook_secret: str | None = None,
    webhook_timeout: float | None = None,
    copy_exports: bool = True,
) -> HookConfig:
    """Build config from explicit args with environment fallbacks."""
    dir_value = hook_dir if hook_dir is not None else os.environ.get(ENV_HOOK_DIR)
    url_value = (
        webhook_url if webhook_url is not None else os.environ.get(ENV_WEBHOOK_URL)
    )
    secret_value = (
        webhook_secret
        if webhook_secret is not None
        else os.environ.get(ENV_WEBHOOK_SECRET)
    )
    timeout = (
        webhook_timeout
        if webhook_timeout is not None
        else _parse_timeout(os.environ.get(ENV_WEBHOOK_TIMEOUT))
    )
    return HookConfig(
        hook_dir=Path(dir_value).expanduser() if dir_value else None,
        webhook_url=(url_value or "").strip() or None,
        webhook_secret=(secret_value or "").strip() or None,
        webhook_timeout=timeout,
        copy_exports=copy_exports,
    )


def _parse_timeout(raw: str | None) -> float:
    if not raw:
        return _DEFAULT_TIMEOUT
    try:
        return max(0.1, float(raw))
    except ValueError:
        return _DEFAULT_TIMEOUT


def list_export_files(output_dir: str | Path | None) -> list[str]:
    if not output_dir:
        return []
    root = Path(output_dir)
    if not root.is_dir():
        return []
    names = sorted(
        path.name
        for path in root.iterdir()
        if path.is_file() and path.name not in {"ERROR.txt"}
    )
    return names


def dispatch_job_hooks(
    payload: JobHookPayload,
    *,
    config: HookConfig | None = None,
) -> HookDispatchResult:
    """Deliver ``payload`` to configured folder and/or webhook.

    Never raises. Returns per-channel outcomes for logs/manifests.
    """
    cfg = config if config is not None else load_hook_config()
    result = HookDispatchResult()
    if not cfg.enabled:
        return result

    body = payload.to_dict()

    if cfg.hook_dir is not None:
        try:
            result.folder_path = str(
                _write_hook_folder(cfg.hook_dir, payload, body, cfg.copy_exports)
            )
            result.folder_ok = True
        except Exception as exc:  # noqa: BLE001 — hooks must not fail jobs
            result.folder_ok = False
            result.folder_error = str(exc)

    if cfg.webhook_url:
        try:
            status = _post_webhook(
                cfg.webhook_url,
                body,
                secret=cfg.webhook_secret,
                timeout=cfg.webhook_timeout,
            )
            result.webhook_ok = 200 <= status < 300
            result.webhook_status = status
            if not result.webhook_ok:
                result.webhook_error = f"HTTP {status}"
        except Exception as exc:  # noqa: BLE001
            result.webhook_ok = False
            result.webhook_error = str(exc)

    return result


def _write_hook_folder(
    hook_dir: Path,
    payload: JobHookPayload,
    body: dict[str, Any],
    copy_exports: bool,
) -> Path:
    hook_dir.mkdir(parents=True, exist_ok=True)
    stem = Path(payload.source).stem or "job"
    job_dir = (
        hook_dir / f"{payload.timestamp[:19].replace(':', '')}_{stem}_{payload.job_id}"
    )
    job_dir.mkdir(parents=True, exist_ok=True)
    (job_dir / "job.json").write_text(
        json.dumps(body, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    if copy_exports and payload.output_dir:
        source = Path(payload.output_dir)
        if source.is_dir():
            exports = job_dir / "exports"
            exports.mkdir(exist_ok=True)
            for name in payload.export_files or list_export_files(source):
                candidate = source / name
                if candidate.is_file():
                    shutil.copy2(candidate, exports / name)
    return job_dir


def _post_webhook(
    url: str,
    body: dict[str, Any],
    *,
    secret: str | None,
    timeout: float,
) -> int:
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": f"boardcomposer-hooks/{v1.API_VERSION}",
    }
    if secret:
        headers["X-BoardComposer-Secret"] = secret
    request = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return int(response.status)
    except urllib.error.HTTPError as exc:
        return int(exc.code)
