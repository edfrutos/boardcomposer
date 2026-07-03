from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from PySide6.QtWidgets import (
    QDockWidget,
    QMainWindow,
    QMenuBar,
    QStatusBar,
    QTextEdit,
)

from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.workspace.board_workspace import BoardWorkspace


class MainWindow(QMainWindow):
    def __init__(self, services):
        super().__init__()
        self.services = services
        self.setWindowTitle("BoardComposer Studio")
        self.resize(1400, 900)

        self._build_menu()
        self._build_workspace()
        self._load_demo_project()
        self._build_panels()
        self._build_statusbar()

    def _build_menu(self):
        menu = QMenuBar(self)
        self.setMenuBar(menu)

        menus = {}

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
            menus[name] = menu.addMenu(name)

        new_action = QAction("Nuevo proyecto", self)
        open_action = QAction("Abrir…", self)
        save_action = QAction("Guardar", self)
        exit_action = QAction("Salir", self)

        menus["Archivo"].addAction(new_action)
        menus["Archivo"].addSeparator()
        menus["Archivo"].addAction(open_action)
        menus["Archivo"].addAction(save_action)
        menus["Archivo"].addSeparator()
        menus["Archivo"].addAction(exit_action)

        exit_action.triggered.connect(self.close)

    def _build_workspace(self):
        self.workspace = BoardWorkspace(self.services)
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
        self.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea,
            inspector_dock,
        )

        console = QTextEdit()
        console.setReadOnly(True)
        console.setText("Timeline / Consola / Eventos")

        console_dock = QDockWidget("Timeline", self)
        console_dock.setWidget(console)
        self.addDockWidget(
            Qt.DockWidgetArea.BottomDockWidgetArea,
            console_dock,
        )

    def _build_statusbar(self):
        status = QStatusBar(self)
        status.showMessage("BoardComposer Studio listo")
        self.setStatusBar(status)

    def _load_demo_project(self):
        project = StudioProject(
            project_id="PRJ-DEMO-001",
            name="Proyecto demo",
            boards=[StudioBoard("TAB-001", 3000, 1000)],
            pieces=[
                StudioPiece("P-001", 700, 300),
                StudioPiece("P-002", 520, 360),
                StudioPiece("P-003", 820, 240),
            ],
            placements=[
                StudioPlacement("P-001", 120, 120),
                StudioPlacement("P-002", 900, 120),
                StudioPlacement("P-003", 1500, 120),
            ],
        )

        self.services.projects.new_project(project)
        self.workspace.reload_project()
        self.setWindowTitle(f"BoardComposer Studio — {project.name}")

    def _new_project(self):
        self._load_demo_project()
        self.statusBar().showMessage("Nuevo proyecto creado", 3000)
