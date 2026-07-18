"""Helpers for the unsaved-changes confirmation dialog (FLW-006)."""

from __future__ import annotations

from pathlib import Path

from studio.i18n import DEFAULT_LANGUAGE, tr


def unsaved_changes_message(
    project_name: str,
    filename: str | Path | None,
    *,
    language: str = DEFAULT_LANGUAGE,
) -> str:
    """Build the body text for the unsaved-changes dialog."""
    name = project_name.strip() or tr("dialog.unsaved_unnamed", language)
    if filename:
        location = tr(
            "dialog.unsaved_location_file",
            language,
            path=str(filename),
        )
    else:
        location = tr("dialog.unsaved_location_new", language)
    return tr(
        "dialog.unsaved_body",
        language,
        name=name,
        location=location,
    )
