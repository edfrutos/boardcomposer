"""Helpers for Studio project identifiers (ADR-006)."""

from __future__ import annotations

import uuid


def new_project_id() -> str:
    """Return a short unique project id such as ``PRJ-A1B2C3D4``."""
    return f"PRJ-{uuid.uuid4().hex[:8].upper()}"
