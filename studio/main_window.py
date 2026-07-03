from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from PySide6.QtWidgets import (
    QDockWidget,
    QMainWindow,
    QMenuBar,
    QStatusBar,
    QTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
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
        self._build_panels()
        self._build_statusbar()
        self._load_demo_project()

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

        self._actions = {}

        self._actions["new_project"] = QAction("Nuevo proyecto", self)
        self._actions["open"] = QAction("Abrir…", self)
        self._actions["save"] = QAction("Guardar", self)
        self._actions["exit"] = QAction("Salir", self)

        menus["Archivo"].addAction(self._actions["new_project"])
        menus["Archivo"].addSeparator()
        menus["Archivo"].addAction(self._actions["open"])
        menus["Archivo"].addAction(self._actions["save"])
        menus["Archivo"].addSeparator()
        menus["Archivo"].addAction(self._actions["exit"])

        self._actions["exit"].triggered.connect(self.close)
        self._actions["new_project"].triggered.connect(self._new_project)

    def _build_workspace(self):
        self.workspace = BoardWorkspace(self.services)
        self.setCentralWidget(self.workspace)

    def _build_panels(self):
        self.explorer = QTreeWidget()
        self.explorer.setHeaderHidden(True)
        self.explorer.itemSelectionChanged.connect(
            self._on_explorer_selection_changed
        )

        explorer_dock = QDockWidget("Explorer", self)
        explorer_dock.setWidget(self.explorer)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, explorer_dock)

        self.inspector = QTextEdit()
        self.inspector.setReadOnly(True)
        self.inspector.setText("Inspector\n\nSin selección")

        inspector_dock = QDockWidget("Inspector", self)
        inspector_dock.setWidget(self.inspector)
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
        self._reload_explorer()
        self.setWindowTitle(f"BoardComposer Studio — {project.name}")

    def _reload_explorer(self):
        project = self.services.projects.current_project
        self.explorer.clear()

        if project is None:
            return

        root = QTreeWidgetItem([project.name])
        boards_root = QTreeWidgetItem(["Tableros"])
        pieces_root = QTreeWidgetItem(["Piezas"])
        solutions_root = QTreeWidgetItem(["Soluciones"])

        for board in project.boards:
            item = QTreeWidgetItem(
                [f"{board.board_id} — {board.length_mm:g} x {board.width_mm:g} mm"]
            )
            item.setData(0, Qt.ItemDataRole.UserRole,
                         f"board:{board.board_id}")
            boards_root.addChild(item)

        for piece in project.pieces:
            item = QTreeWidgetItem(
                [f"{piece.piece_id} — {piece.length_mm:g} x {piece.width_mm:g} mm"]
            )
            item.setData(0, Qt.ItemDataRole.UserRole,
                         f"piece:{piece.piece_id}")
            pieces_root.addChild(item)

        root.addChild(boards_root)
        root.addChild(pieces_root)
        root.addChild(solutions_root)
        self.explorer.addTopLevelItem(root)
        self.explorer.expandAll()

    def _on_explorer_selection_changed(self):
        selected = self.explorer.selectedItems()

        if not selected:
            self.inspector.setText("Inspector\n\nSin selección")
            return

        item = selected[0]
        data = item.data(0, Qt.ItemDataRole.UserRole)
        project = self.services.projects.current_project

        if project is None or data is None:
            self.inspector.setText(f"Inspector\n\n{item.text(0)}")
            return

        kind, object_id = data.split(":", 1)

        if kind == "board":
            board = next(
                board for board in project.boards if board.board_id == object_id
            )
            self.inspector.setText(
                "Inspector\n\n"
                f"Tablero: {board.board_id}\n"
                f"Dimensiones: {board.length_mm:g} x {board.width_mm:g} mm\n"
                f"Material: {board.material}"
            )
            return

        if kind == "piece":
            piece = project.piece_by_id(object_id)
            self.services.selection.select_one(object_id)
            self.workspace.select_piece(object_id)
            self.inspector.setText(
                "Inspector\n\n"
                f"Pieza: {piece.piece_id}\n"
                f"Dimensiones: {piece.length_mm:g} x {piece.width_mm:g} mm\n"
                f"Material: {piece.material}"
            )

    def _new_project(self):
        self._load_demo_project()
        self.statusBar().showMessage("Nuevo proyecto creado", 3000)

    def refresh_inspector_for_piece(self, piece_id: str):
        project = self.services.projects.current_project
        if project is None:
            return

        piece = project.piece_by_id(piece_id)
        placement = next(
            placement for placement in project.placements
            if placement.piece_id == piece_id
        )

        self.inspector.setText(
            "Inspector\n\n"
            f"Pieza: {piece.piece_id}\n"
            f"Dimensiones: {piece.length_mm:g} x {piece.width_mm:g} mm\n"
            f"Posición: {placement.x_mm:g}, {placement.y_mm:g} mm\n"
            f"Material: {piece.material}"
        )
