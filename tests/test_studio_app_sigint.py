"""Studio app entry should quit cleanly on SIGINT."""

import signal

from PySide6.QtWidgets import QApplication

from studio.app import _install_sigint_handler


def test_sigint_handler_installs_polling_timer(qapp):
    del qapp
    app = QApplication.instance()
    assert app is not None

    previous = signal.getsignal(signal.SIGINT)
    timer = _install_sigint_handler(app)
    try:
        assert timer.isActive()
        assert callable(signal.getsignal(signal.SIGINT))
    finally:
        timer.stop()
        signal.signal(signal.SIGINT, previous)
