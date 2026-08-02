"""Shared dialog chrome helpers (Industrial madera / a11y)."""

from __future__ import annotations

from PySide6.QtWidgets import QDialogButtonBox, QPushButton


def polish_secondary_button(
    button: QPushButton,
    *,
    tip: str | None = None,
    min_height: int = 36,
) -> QPushButton:
    """Ensure a usable secondary CTA target (and optional tip)."""
    button.setMinimumHeight(min_height)
    if tip:
        button.setToolTip(tip)
        button.setStatusTip(tip)
    return button


def polish_dialog_button_box(buttons: QDialogButtonBox) -> None:
    """Mark OK as primary CTA and ensure usable button targets."""
    ok = buttons.button(QDialogButtonBox.StandardButton.Ok)
    if ok is not None:
        ok.setObjectName("primaryButton")
        ok.setMinimumHeight(36)
    for role in (
        QDialogButtonBox.StandardButton.Cancel,
        QDialogButtonBox.StandardButton.Close,
        QDialogButtonBox.StandardButton.RestoreDefaults,
    ):
        button = buttons.button(role)
        if isinstance(button, QPushButton):
            polish_secondary_button(button)
