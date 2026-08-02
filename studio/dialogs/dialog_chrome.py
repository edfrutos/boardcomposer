"""Shared dialog chrome helpers (Industrial madera / a11y)."""

from __future__ import annotations

from PySide6.QtWidgets import QDialogButtonBox, QPushButton, QWidget

_SECONDARY_MIN_HEIGHT_PROP = "bcSecondaryMinHeight"


def polish_secondary_button(
    button: QPushButton,
    *,
    tip: str | None = None,
    min_height: int = 36,
) -> QPushButton:
    """Ensure a usable secondary CTA target (and optional tip).

    Stores the intended height as a dynamic property so
    :func:`repolish_secondary_buttons` can restore it after a theme switch
    (light/dark → ``system`` clears QSS and can wipe ``minimumHeight``).
    """
    button.setProperty(_SECONDARY_MIN_HEIGHT_PROP, int(min_height))
    button.setMinimumHeight(min_height)
    if tip:
        button.setToolTip(tip)
        button.setStatusTip(tip)
    return button


def repolish_secondary_buttons(root: QWidget) -> None:
    """Re-apply secondary min-heights under ``root`` after theme changes."""
    for button in root.findChildren(QPushButton):
        height = button.property(_SECONDARY_MIN_HEIGHT_PROP)
        if height is None:
            continue
        try:
            button.setMinimumHeight(int(height))
        except (TypeError, ValueError):
            continue


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
