from PySide6.QtCore import Qt

from studio.workspace.board_workspace import BoardWorkspace
from PySide6.QtWidgets import (
    QDockWidget,
    QMainWindow,
    QMenuBar,
    QStatusBar,
    QTextEdit,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BoardComposer Studio")
        self.resize(1400, 900)

        self._build_menu()
        self._build_workspace()
        self._build_panels()
        self._build_statusbar()

    def _build_menu(self):
        menu = QMenuBar(self)
        self.setMenuBar(menu)

        for name in (
            "Archivo",
            "Editar",
            "Ver",
            "Proyecto",
            "Generar",
            "Comparar",
            "Exportar",
            "Herramientas",
            "Ayuda",
        ):
            menu.addMenu(name)

    def _build_workspace(self):
        self.workspace = BoardWorkspace()
        self.setCentralWidget(self.workspace)

    def _build_panels(self):
        explorer = QTextEdit()
        explorer.setReadOnly(True)
        explorer.setText("Proyecto\n\n├ Tableros\n├ Piezas\n└ Soluciones")

        explorer_dock = QDockWidget("Explorer", self)
        explorer_dock.setWidget(explorer)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, explorer_dock)

        inspector = QTextEdit()
        inspector.setReadOnly(True)
        inspector.setText("Inspector\n\nSin selección")

        inspector_dock = QDockWidget("Inspector", self)
        inspector_dock.setWidget(inspector)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, inspector_dock)

        console = QTextEdit()
        console.setReadOnly(True)
        console.setText("Timeline / Consola / Eventos")

        console_dock = QDockWidget("Timeline", self)
        console_dock.setWidget(console)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, console_dock)

    def _build_statusbar(self):
        status = QStatusBar(self)
        status.showMessage("BoardComposer Studio listo")
        self.setStatusBar(status)
