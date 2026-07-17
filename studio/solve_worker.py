"""Background solve worker for Studio layout generation."""

from __future__ import annotations

from PySide6.QtCore import QObject, QThread, Signal

from boardcomposer.domain import AssemblySolution
from boardcomposer.solver.cancel import CancellationToken


class SolveWorker(QObject):
    """Runs `layout.solve_current_project` on a worker thread."""

    finished = Signal(object)
    failed = Signal(str)

    def __init__(self, layout_service, cancel: CancellationToken) -> None:
        super().__init__()
        self._layout = layout_service
        self._cancel = cancel

    def run(self) -> None:
        try:
            solution = self._layout.solve_current_project(cancel=self._cancel)
        except Exception as exc:  # noqa: BLE001 — surface to UI
            self.failed.emit(str(exc))
            return
        self.finished.emit(solution)


def run_solve_with_progress(
    *,
    parent,
    layout_service,
    label: str,
    title: str,
    cancel_text: str,
) -> AssemblySolution | None:
    """Modal progress dialog with Cancel while the solver runs off-thread.

    Returns the selected solution, or ``None`` if none / cancelled / error.
    On cancel, ``layout_service.stats.cancelled`` is True.
    """
    from PySide6.QtCore import QEventLoop, Qt
    from PySide6.QtWidgets import QProgressDialog

    cancel = CancellationToken()
    thread = QThread(parent)
    worker = SolveWorker(layout_service, cancel)
    worker.moveToThread(thread)

    progress = QProgressDialog(label, cancel_text, 0, 0, parent)
    progress.setWindowTitle(title)
    progress.setWindowModality(Qt.WindowModality.WindowModal)
    progress.setMinimumDuration(0)
    progress.setAutoClose(False)
    progress.setAutoReset(False)
    progress.setValue(0)

    loop = QEventLoop(parent)
    result: dict[str, AssemblySolution | None | str] = {"solution": None, "error": None}

    def cleanup() -> None:
        thread.quit()
        thread.wait(60_000)
        worker.deleteLater()
        thread.deleteLater()

    def on_finished(solution: AssemblySolution | None) -> None:
        result["solution"] = solution
        progress.close()
        loop.quit()

    def on_failed(message: str) -> None:
        result["error"] = message
        progress.close()
        loop.quit()

    def on_canceled() -> None:
        cancel.cancel()

    thread.started.connect(worker.run)
    worker.finished.connect(on_finished)
    worker.failed.connect(on_failed)
    progress.canceled.connect(on_canceled)

    thread.start()
    progress.show()
    loop.exec()
    cleanup()

    if result["error"] is not None:
        raise RuntimeError(str(result["error"]))

    return result["solution"]  # type: ignore[return-value]
