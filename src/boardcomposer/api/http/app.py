"""Flask app: thin HTTP surface over ``boardcomposer.api.v1`` (EP-003)."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from flask import Flask, Response, jsonify, request

from boardcomposer.api import v1
from boardcomposer.api.http.auth import ENV_API_KEY, configured_api_key, require_api_key
from boardcomposer.integration.hooks import JobHookPayload, dispatch_job_hooks

ENV_MAX_UPLOAD = "BOARDCOMPOSER_MAX_UPLOAD_BYTES"
_DEFAULT_MAX_UPLOAD = 5 * 1024 * 1024
_ALLOWED_SUFFIXES = {".csv", ".bcproj"}


def _max_upload_bytes() -> int:
    raw = os.environ.get(ENV_MAX_UPLOAD, "").strip()
    if not raw:
        return _DEFAULT_MAX_UPLOAD
    try:
        return max(1, int(raw))
    except ValueError:
        return _DEFAULT_MAX_UPLOAD


def create_app() -> Flask:
    """Build the HTTP adapter app (no global Flask state)."""
    app = Flask("boardcomposer.api.http")
    app.config["MAX_CONTENT_LENGTH"] = _max_upload_bytes()

    @app.get("/health")
    def health():
        return jsonify(
            {
                "status": "ok",
                "service": "boardcomposer-http",
                "api_version": v1.API_VERSION,
                "auth_required": configured_api_key() is not None,
            }
        )

    @app.get("/v1/openapi.json")
    def openapi():
        return jsonify(_openapi_document())

    @app.post("/v1/run")
    @require_api_key
    def run_job():
        """Upload a CSV/``.bcproj``, solve, and return JSON or an export body."""
        upload = request.files.get("file") or request.files.get("project")
        if upload is None or not upload.filename:
            return jsonify(
                {"error": "missing_file", "detail": "Send multipart field 'file'"}
            ), 400

        suffix = Path(upload.filename).suffix.lower()
        if suffix not in _ALLOWED_SUFFIXES:
            return jsonify(
                {
                    "error": "unsupported_type",
                    "detail": f"Expected .csv or .bcproj, got {suffix or '(none)'}",
                }
            ), 400

        strategy = (request.form.get("strategy") or "balanced").strip()
        try:
            top = int(request.form.get("top") or "1")
        except ValueError:
            return jsonify(
                {"error": "bad_top", "detail": "top must be an integer"}
            ), 400

        fmt = (request.form.get("format") or "json").strip().lower()
        if fmt not in {"json", "csv", "svg"}:
            return jsonify(
                {
                    "error": "bad_format",
                    "detail": "format must be one of: json, csv, svg",
                }
            ), 400

        with tempfile.TemporaryDirectory(prefix="bc-http-") as tmp:
            path = Path(tmp) / f"project{suffix}"
            upload.save(path)
            try:
                project, solutions = v1.run(path, strategy=strategy, top=top)
            except Exception as exc:  # noqa: BLE001 — map to HTTP 400
                return jsonify({"error": "solve_failed", "detail": str(exc)}), 400

            if not solutions:
                return jsonify(
                    {
                        "error": "no_solutions",
                        "detail": "Solver returned no valid solutions",
                        "api_version": v1.API_VERSION,
                    }
                ), 422

            best = solutions[0]
            if fmt == "json":
                body = v1.export_json(
                    best,
                    project,
                    strategy_name=strategy,
                    solution_index=0,
                )
                _fire_http_hooks(
                    source=upload.filename,
                    status="ok",
                    strategy=strategy,
                    fmt=fmt,
                    solutions=len(solutions),
                )
                return Response(body, mimetype="application/json")
            if fmt == "csv":
                body = v1.export_csv(best)
                _fire_http_hooks(
                    source=upload.filename,
                    status="ok",
                    strategy=strategy,
                    fmt=fmt,
                    solutions=len(solutions),
                )
                return Response(
                    body,
                    mimetype="text/csv",
                    headers={
                        "Content-Disposition": "attachment; filename=placements.csv"
                    },
                )
            body = v1.export_svg(best, project)
            _fire_http_hooks(
                source=upload.filename,
                status="ok",
                strategy=strategy,
                fmt=fmt,
                solutions=len(solutions),
            )
            return Response(
                body,
                mimetype="image/svg+xml",
                headers={"Content-Disposition": "attachment; filename=solution.svg"},
            )

    return app


def _fire_http_hooks(
    *,
    source: str,
    status: str,
    strategy: str,
    fmt: str,
    solutions: int,
    error: str | None = None,
) -> None:
    dispatch_job_hooks(
        JobHookPayload(
            source=source,
            status=status,
            channel="http",
            strategy=strategy,
            formats=[fmt],
            solutions=solutions,
            error=error,
        )
    )


def _openapi_document() -> dict:
    return {
        "openapi": "3.0.3",
        "info": {
            "title": "BoardComposer HTTP API",
            "version": v1.API_VERSION,
            "description": (
                "Optional thin adapter over boardcomposer.api.v1 (EP-003). "
                f"When {ENV_API_KEY} is set, send X-API-Key or Authorization: Bearer."
            ),
        },
        "paths": {
            "/health": {
                "get": {
                    "summary": "Liveness",
                    "responses": {"200": {"description": "OK"}},
                }
            },
            "/v1/run": {
                "post": {
                    "summary": "Solve uploaded CSV/.bcproj and export",
                    "security": [{"ApiKeyAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "multipart/form-data": {
                                "schema": {
                                    "type": "object",
                                    "required": ["file"],
                                    "properties": {
                                        "file": {
                                            "type": "string",
                                            "format": "binary",
                                        },
                                        "strategy": {
                                            "type": "string",
                                            "default": "balanced",
                                        },
                                        "top": {"type": "integer", "default": 1},
                                        "format": {
                                            "type": "string",
                                            "enum": ["json", "csv", "svg"],
                                            "default": "json",
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "responses": {
                        "200": {"description": "Export body"},
                        "400": {"description": "Bad request"},
                        "401": {"description": "Unauthorized"},
                        "422": {"description": "No solutions"},
                    },
                }
            },
        },
        "components": {
            "securitySchemes": {
                "ApiKeyAuth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-API-Key",
                }
            }
        },
    }
