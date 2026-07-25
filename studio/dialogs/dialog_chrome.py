"""Shared dialog chrome helpers (Industrial madera / a11y)."""

from __future__ import annotations

from PySide6.QtWidgets import QDialogButtonBox, QPushButton


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
            button.setMinimumHeight(36)
