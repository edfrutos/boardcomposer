"""Helpers for Explorer tree roles and context actions."""

from __future__ import annotations


def parse_explorer_role(role: object) -> tuple[str, str] | None:
    """Split ``kind:id`` explorer UserRole data."""
    if not isinstance(role, str) or ":" not in role:
        return None
    kind, object_id = role.split(":", 1)
    if not kind or not object_id:
        return None
    return kind, object_id


def explorer_context_actions(role: object) -> tuple[str, ...]:
    """Return context-menu action keys for an explorer item role."""
    parsed = parse_explorer_role(role)
    if parsed is None:
        return ()
    kind, object_id = parsed
    if kind == "piece":
        return ("edit", "duplicate", "delete")
    if kind == "board":
        return ("edit",)
    if kind == "category" and object_id == "boards":
        return ("add_board",)
    if kind == "category" and object_id == "pieces":
        return ("add_piece",)
    if kind == "solution":
        return ("preview_solution",)
    return ()
