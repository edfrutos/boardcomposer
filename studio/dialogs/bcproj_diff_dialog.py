"""Studio UI for structural ``.bcproj`` diffs (FLW-006 / ``diff_bcproj``)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from boardcomposer.io.bcproj_diff import diff_bcproj
from boardcomposer.io.bcproj_revisions import list_revisions
from studio.dialogs.dialog_chrome import (
    polish_dialog_button_box,
    polish_primary_button,
    polish_secondary_button,
)
from studio.i18n import DEFAULT_LANGUAGE, tr


class BcprojDiffDialog(QDialog):
    """Compare two ``.bcproj`` revisions (or the open project vs a file)."""

    def __init__(
        self,
        parent=None,
        *,
        language: str = DEFAULT_LANGUAGE,
        current_project: dict[str, Any] | None = None,
        current_label: str | None = None,
        project_path: str | None = None,
        start_dir: str | None = None,
    ) -> None:
        super().__init__(parent)
        self._language = language
        self._current_project = current_project
        self._current_label = current_label or tr(
            "diff_bcproj.current_project", language
        )
        self._project_path = project_path
        self._start_dir = start_dir or str(Path.home())
        self._revisions = list_revisions(project_path) if project_path else []
        self.restore_path: Path | None = None

        self.setWindowTitle(tr("diff_bcproj.title", language))
        self.setMinimumSize(640, 460)

        intro = QLabel(tr("diff_bcproj.intro", language))
        intro.setWordWrap(True)

        self.left_path = QLineEdit()
        self.right_path = QLineEdit()
        browse_tip = tr("diff_bcproj.browse_tip", language)
        left_browse = polish_secondary_button(
            QPushButton(tr("diff_bcproj.browse", language)),
            tip=browse_tip,
        )
        right_browse = polish_secondary_button(
            QPushButton(tr("diff_bcproj.browse", language)),
            tip=browse_tip,
        )
        left_browse.clicked.connect(lambda: self._browse(self.left_path))
        right_browse.clicked.connect(lambda: self._browse(self.right_path))
        self.left_browse_button = left_browse
        self.right_browse_button = right_browse

        left_row = QHBoxLayout()
        left_row.addWidget(self.left_path)
        left_row.addWidget(left_browse)
        right_row = QHBoxLayout()
        right_row.addWidget(self.right_path)
        right_row.addWidget(right_browse)

        form = QFormLayout()
        form.addRow(tr("diff_bcproj.left", language), left_row)
        form.addRow(tr("diff_bcproj.right", language), right_row)

        self.revision_combo = QComboBox()
        self.revision_combo.addItem(tr("diff_bcproj.revision_none", language), None)
        for rev in self._revisions:
            self.revision_combo.addItem(rev.name, str(rev))
        self.revision_combo.setEnabled(bool(self._revisions))
        form.addRow(tr("diff_bcproj.revision", language), self.revision_combo)

        self.use_current_left = QCheckBox(tr("diff_bcproj.use_current", language))
        self.use_current_left.setEnabled(current_project is not None)
        self.use_current_left.toggled.connect(self._on_use_current_left_toggled)

        self.use_current_right = QCheckBox(
            tr("diff_bcproj.use_current_right", language)
        )
        self.use_current_right.setEnabled(current_project is not None)
        self.use_current_right.toggled.connect(self._on_use_current_right_toggled)

        # Prefer: last revision (left) vs open project (right) when available.
        if self._revisions and current_project is not None:
            self.revision_combo.setCurrentIndex(1)
            self.use_current_right.setChecked(True)
        elif current_project is not None:
            self.use_current_left.setChecked(True)

        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setPlaceholderText(tr("diff_bcproj.placeholder", language))

        compare_btn = polish_primary_button(
            QPushButton(tr("diff_bcproj.compare", language)),
            tip=tr("diff_bcproj.compare_tip", language),
            min_height=36,
        )
        compare_btn.setDefault(True)
        compare_btn.clicked.connect(self._run_diff)
        self.compare_button = compare_btn

        self.restore_button = polish_secondary_button(
            QPushButton(tr("diff_bcproj.restore", language)),
            tip=tr("diff_bcproj.restore_tip", language),
        )
        self.restore_button.clicked.connect(self._request_restore)
        self.left_path.textChanged.connect(self._sync_restore_enabled)
        self.use_current_left.toggled.connect(self._sync_restore_enabled)
        self.revision_combo.currentIndexChanged.connect(self._on_revision_chosen)

        actions_row = QHBoxLayout()
        actions_row.addWidget(compare_btn)
        actions_row.addWidget(self.restore_button)
        actions_row.addStretch(1)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        polish_dialog_button_box(buttons)
        buttons.rejected.connect(self.reject)
        buttons.accepted.connect(self.accept)

        layout = QVBoxLayout(self)
        layout.addWidget(intro)
        layout.addLayout(form)
        layout.addWidget(self.use_current_left)
        layout.addWidget(self.use_current_right)
        layout.addLayout(actions_row)
        layout.addWidget(self.result, stretch=1)
        layout.addWidget(buttons)

        # Compat alias for existing tests.
        self.use_current = self.use_current_left
        if self.revision_combo.currentIndex() > 0:
            path = self.revision_combo.currentData()
            if path:
                self.use_current_left.setChecked(False)
                self.left_path.setText(str(path))
        self._sync_restore_enabled()

    def selected_revision_path(self) -> Path | None:
        """Return the ring snapshot currently selected for restore, if any."""
        data = self.revision_combo.currentData()
        if data:
            return Path(str(data))
        return None

    def _sync_restore_enabled(self) -> None:
        enabled = self.selected_revision_path() is not None
        self.restore_button.setEnabled(enabled)
        tip = tr(
            "diff_bcproj.restore_tip" if enabled else "diff_bcproj.restore_idle",
            self._language,
        )
        self.restore_button.setToolTip(tip)
        self.restore_button.setStatusTip(tip)

    def _request_restore(self) -> None:
        path = self.selected_revision_path()
        if path is None:
            return
        self.restore_path = path
        self.accept()

    def _on_revision_chosen(self, index: int) -> None:
        path = self.revision_combo.itemData(index)
        if not path:
            self._sync_restore_enabled()
            return
        self.use_current_left.setChecked(False)
        self.left_path.setText(str(path))
        self._sync_restore_enabled()

    def _on_use_current_left_toggled(self, checked: bool) -> None:
        self.left_path.setEnabled(not checked)
        if checked:
            self.use_current_right.setChecked(False)
            self.left_path.setText(self._current_label)
            self.revision_combo.blockSignals(True)
            self.revision_combo.setCurrentIndex(0)
            self.revision_combo.blockSignals(False)
        self._sync_restore_enabled()

    def _on_use_current_right_toggled(self, checked: bool) -> None:
        self.right_path.setEnabled(not checked)
        if checked:
            self.use_current_left.setChecked(False)
            self.right_path.setText(self._current_label)

    def _browse(self, target: QLineEdit) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            tr("diff_bcproj.open_title", self._language),
            target.text().strip() or self._start_dir,
            tr("diff_bcproj.file_filter", self._language),
        )
        if path:
            target.setText(path)

    def _resolve_left(self) -> tuple[Any, str]:
        if self.use_current_left.isChecked() and self._current_project is not None:
            return self._current_project, self._current_label
        path = self.left_path.text().strip()
        if not path:
            raise ValueError(tr("diff_bcproj.need_left", self._language))
        return path, path

    def _resolve_right(self) -> tuple[Any, str]:
        if self.use_current_right.isChecked() and self._current_project is not None:
            return self._current_project, self._current_label
        path = self.right_path.text().strip()
        if not path:
            raise ValueError(tr("diff_bcproj.need_right", self._language))
        return path, path

    def _run_diff(self) -> None:
        try:
            left, left_label = self._resolve_left()
            right, right_label = self._resolve_right()
            report = diff_bcproj(
                left,
                right,
                left_label=left_label,
                right_label=right_label,
            )
        except Exception as exc:  # noqa: BLE001 — surface parse/IO to user
            QMessageBox.warning(
                self,
                tr("diff_bcproj.error_title", self._language),
                str(exc),
            )
            return
        self.result.setPlainText("\n".join(report.summary_lines()))
