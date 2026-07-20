"""Background solve worker for Studio layout generation."""

from __future__ import annotations

from PySide6.QtCore import QObject, QThread, Qt, Signal, Slot

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


class _SolveProgressBridge(QObject):
    """Receives worker signals on the GUI thread and unblocks the event loop.

    Plain Python callables connected with AutoConnection can run as
    DirectConnection when the worker emits from another thread, which is
    unsafe for ``QProgressDialog.close()`` and leaves the modal dialog hung.
    """

    def __init__(self, progress, loop: object) -> None:
        super().__init__()
        self._progress = progress
        self._loop = loop
        self.solution: AssemblySolution | None = None
        self.error: str | None = None

    @Slot(object)
    def on_finished(self, solution: object) -> None:
        self.solution = solution  # type: ignore[assignment]
        self._progress.close()
        self._loop.quit()

    @Slot(str)
    def on_failed(self, message: str) -> None:
        self.error = message
        self._progress.close()
        self._loop.quit()


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
    from PySide6.QtCore import QEventLoop
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
    bridge = _SolveProgressBridge(progress, loop)
    # Affinity: same thread as ``parent`` / the calling GUI thread.
    if parent is not None:
        bridge.moveToThread(parent.thread())

    def on_canceled() -> None:
        cancel.cancel()

    thread.started.connect(worker.run)
    worker.finished.connect(
        bridge.on_finished, Qt.ConnectionType.QueuedConnection
    )
    worker.failed.connect(bridge.on_failed, Qt.ConnectionType.QueuedConnection)
    progress.canceled.connect(on_canceled)

    thread.start()
    progress.show()
    loop.exec()

    thread.quit()
    thread.wait(60_000)
    worker.deleteLater()
    thread.deleteLater()
    bridge.deleteLater()

    if bridge.error is not None:
        raise RuntimeError(bridge.error)

    return bridge.solution
