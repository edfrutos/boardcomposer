"""Studio UI for structural ``.bcproj`` diffs (FLW-006 / ``diff_bcproj``)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from PySide6.QtWidgets import (
    QCheckBox,
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
from studio.dialogs.dialog_chrome import polish_dialog_button_box
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
        start_dir: str | None = None,
    ) -> None:
        super().__init__(parent)
        self._language = language
        self._current_project = current_project
        self._current_label = current_label or tr(
            "diff_bcproj.current_project", language
        )
        self._start_dir = start_dir or str(Path.home())

        self.setWindowTitle(tr("diff_bcproj.title", language))
        self.setMinimumSize(640, 420)

        intro = QLabel(tr("diff_bcproj.intro", language))
        intro.setWordWrap(True)

        self.left_path = QLineEdit()
        self.right_path = QLineEdit()
        left_browse = QPushButton(tr("diff_bcproj.browse", language))
        right_browse = QPushButton(tr("diff_bcproj.browse", language))
        left_browse.clicked.connect(lambda: self._browse(self.left_path))
        right_browse.clicked.connect(lambda: self._browse(self.right_path))

        left_row = QHBoxLayout()
        left_row.addWidget(self.left_path)
        left_row.addWidget(left_browse)
        right_row = QHBoxLayout()
        right_row.addWidget(self.right_path)
        right_row.addWidget(right_browse)

        form = QFormLayout()
        form.addRow(tr("diff_bcproj.left", language), left_row)
        form.addRow(tr("diff_bcproj.right", language), right_row)

        self.use_current = QCheckBox(tr("diff_bcproj.use_current", language))
        self.use_current.setEnabled(current_project is not None)
        self.use_current.toggled.connect(self._on_use_current_toggled)
        if current_project is not None:
            self.use_current.setChecked(True)

        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setPlaceholderText(tr("diff_bcproj.placeholder", language))

        compare_btn = QPushButton(tr("diff_bcproj.compare", language))
        compare_btn.setDefault(True)
        compare_btn.clicked.connect(self._run_diff)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        polish_dialog_button_box(buttons)
        buttons.rejected.connect(self.reject)
        buttons.accepted.connect(self.accept)

        layout = QVBoxLayout(self)
        layout.addWidget(intro)
        layout.addLayout(form)
        layout.addWidget(self.use_current)
        layout.addWidget(compare_btn)
        layout.addWidget(self.result, stretch=1)
        layout.addWidget(buttons)

    def _on_use_current_toggled(self, checked: bool) -> None:
        self.left_path.setEnabled(not checked)
        if checked:
            self.left_path.setText(self._current_label)

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
        if self.use_current.isChecked() and self._current_project is not None:
            return self._current_project, self._current_label
        path = self.left_path.text().strip()
        if not path:
            raise ValueError(tr("diff_bcproj.need_left", self._language))
        return path, path

    def _resolve_right(self) -> tuple[Any, str]:
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
