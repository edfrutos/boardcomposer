"""Minimal API-key auth for the HTTP adapter (EP-003)."""

from __future__ import annotations

import os
from functools import wraps

from flask import Request, jsonify, request


ENV_API_KEY = "BOARDCOMPOSER_API_KEY"


def configured_api_key() -> str | None:
    value = os.environ.get(ENV_API_KEY, "").strip()
    return value or None


def extract_api_key(req: Request) -> str | None:
    header = req.headers.get("X-API-Key", "").strip()
    if header:
        return header
    auth = req.headers.get("Authorization", "").strip()
    if auth.lower().startswith("bearer "):
        return auth[7:].strip() or None
    return None


def require_api_key(view):
    """Enforce API key when ``BOARDCOMPOSER_API_KEY`` is set."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        expected = configured_api_key()
        if expected is None:
            return view(*args, **kwargs)
        provided = extract_api_key(request)
        if provided != expected:
            return jsonify({"error": "unauthorized", "detail": "Invalid API key"}), 401
        return view(*args, **kwargs)

    return wrapped
