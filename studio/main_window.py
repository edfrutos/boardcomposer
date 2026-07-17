"""Main window for BoardComposer Studio."""

from pathlib import Path
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QCloseEvent, QIcon
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QDockWidget,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMenuBar,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from boardcomposer.export import (
    solution_to_csv,
    solution_to_dxf,
    solution_to_json,
    solution_to_pdf,
    solution_to_svg,
)
from studio.commands import DeletePieceCommand, RotatePieceCommand
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.project_serializer import (
    UnsupportedProjectVersionError,
    load_project,
    save_project,
)
from studio.workspace.board_workspace import BoardWorkspace
from studio.workspace.board_piece_item import BoardPieceItem
from studio.dialogs import (
    ImportBoardsPreviewDialog,
    ImportPiecesPreviewDialog,
    NewBoardDialog,
    NewPieceDialog,
    PreferencesDialog,
)
from studio.board_csv_importer import import_boards_from_file
from studio.piece_csv_importer import import_pieces_from_file
from studio.solution_diff import compare_solutions, format_diff_unavailable
from studio.solution_ordering import SORT_LABELS, ordered_solution_indexes
from studio.solution_thumbnail import DEFAULT_THUMBNAIL_SIZE, solution_thumbnails
from studio.welcome_screen import WelcomeScreen


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self, services):
        super().__init__()
        self.services = services
        self.current_project_path = None
        self._solution_display_indexes: list[int] = []
        self._comparator_sort_by = "ranking"
        self._comparator_complete_only = False
        self._comparator_reference_index: int | None = None
        self.setWindowTitle("BoardComposer Studio")
        self.resize(1400, 900)

        self._build_menu()
        self._build_workspace()
        self._build_panels()
        self._build_statusbar()
        self._reload_explorer()
        self._reload_solution_table()
        self.update_window_title()
        self._apply_preferences()

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
        self._actions["new_demo_project"] = QAction("Nuevo proyecto demo", self)
        self._actions["show_welcome"] = QAction("Pantalla de inicio", self)
        self._actions["open"] = QAction("Abrir…", self)
        self._actions["save"] = QAction("Guardar", self)
        self._actions["save_as"] = QAction("Guardar como…", self)
        self._actions["add_board"] = QAction("Añadir tablero…", self)
        self._actions["add_piece"] = QAction("Añadir pieza…", self)
        self._actions["import_boards_csv"] = QAction(
            "Importar inventario de tableros (CSV/Excel)…", self
        )
        self._actions["import_pieces_csv"] = QAction(
            "Importar piezas (CSV/Excel)…", self
        )
        self._actions["export_selected_svg"] = QAction(
            "Exportar solución seleccionada a SVG…",
            self,
        )
        self._actions["export_selected_dxf"] = QAction(
            "Exportar solución seleccionada a DXF…",
            self,
        )
        self._actions["export_selected_pdf"] = QAction(
            "Exportar solución seleccionada a PDF…",
            self,
        )
        self._actions["export_selected_json"] = QAction(
            "Exportar solución seleccionada a JSON…",
            self,
        )
        self._actions["export_selected_csv"] = QAction(
            "Exportar solución seleccionada a CSV…",
            self,
        )
        self._actions["exit"] = QAction("Salir", self)
        self._actions["undo"] = QAction("Deshacer", self)
        self._actions["redo"] = QAction("Rehacer", self)
        self._actions["rotate_piece"] = QAction("Rotar 90°", self)
        self._actions["delete_piece"] = QAction("Eliminar pieza", self)
        self._actions["preferences"] = QAction("Preferencias…", self)
        self._actions["solve_layout"] = QAction("Calcular layout", self)
        self._actions["previous_solution"] = QAction("Solución anterior", self)
        self._actions["next_solution"] = QAction("Solución siguiente", self)
        self._actions["apply_layout"] = QAction("Aplicar layout calculado", self)

        self._recent_menu = menus["Archivo"].addMenu("Abrir recientes")

        self._actions["undo"].setShortcut("Ctrl+Z")
        self._actions["redo"].setShortcut("Ctrl+Shift+Z")
        self._actions["rotate_piece"].setShortcut("R")
        self._actions["delete_piece"].setShortcut("Backspace")

        menus["Archivo"].addAction(self._actions["new_project"])
        menus["Archivo"].addAction(self._actions["new_demo_project"])
        menus["Archivo"].addAction(self._actions["show_welcome"])
        menus["Archivo"].addSeparator()
        menus["Archivo"].addAction(self._actions["open"])
        menus["Archivo"].addMenu(self._recent_menu)
        menus["Archivo"].addSeparator()
        menus["Archivo"].addAction(self._actions["save"])
        menus["Archivo"].addAction(self._actions["save_as"])
        menus["Archivo"].addSeparator()
        menus["Archivo"].addAction(self._actions["exit"])

        menus["Editar"].addAction(self._actions["undo"])
        menus["Editar"].addAction(self._actions["redo"])
        menus["Editar"].addSeparator()
        menus["Editar"].addAction(self._actions["rotate_piece"])
        menus["Editar"].addAction(self._actions["delete_piece"])
        menus["Editar"].addSeparator()
        menus["Editar"].addAction(self._actions["preferences"])

        menus["Proyecto"].addAction(self._actions["add_board"])
        menus["Proyecto"].addAction(self._actions["add_piece"])
        menus["Proyecto"].addAction(self._actions["import_boards_csv"])
        menus["Proyecto"].addAction(self._actions["import_pieces_csv"])

        menus["Exportar"].addAction(self._actions["export_selected_svg"])
        menus["Exportar"].addAction(self._actions["export_selected_dxf"])
        menus["Exportar"].addAction(self._actions["export_selected_pdf"])
        menus["Exportar"].addAction(self._actions["export_selected_json"])
        menus["Exportar"].addAction(self._actions["export_selected_csv"])

        menus["Herramientas"].addAction(self._actions["solve_layout"])
        menus["Herramientas"].addSeparator()
        menus["Herramientas"].addAction(self._actions["previous_solution"])
        menus["Herramientas"].addAction(self._actions["next_solution"])
        menus["Herramientas"].addSeparator()
        menus["Herramientas"].addAction(self._actions["apply_layout"])

        self._actions["open"].triggered.connect(self._open_project)
        self._actions["save"].triggered.connect(self._save_project)
        self._actions["save_as"].triggered.connect(self._save_project_as)
        self._actions["exit"].triggered.connect(self.close)
        self._actions["new_project"].triggered.connect(self._new_project)
        self._actions["new_demo_project"].triggered.connect(self._new_demo_project)
        self._actions["show_welcome"].triggered.connect(self._show_welcome_screen)
        self._actions["add_board"].triggered.connect(self._add_board)
        self._actions["add_piece"].triggered.connect(self._add_piece)
        self._actions["import_boards_csv"].triggered.connect(
            self._import_boards_from_csv
        )
        self._actions["import_pieces_csv"].triggered.connect(
            self._import_pieces_from_csv
        )

        self._actions["undo"].triggered.connect(self._undo)
        self._actions["redo"].triggered.connect(self._redo)
        self._actions["rotate_piece"].triggered.connect(self._rotate_selected_piece)
        self._actions["delete_piece"].triggered.connect(self._delete_selected_piece)
        self._actions["preferences"].triggered.connect(self._open_preferences)
        self._actions["solve_layout"].triggered.connect(self._solve_layout)
        self._actions["previous_solution"].triggered.connect(
            self._previous_layout_solution
        )
        self._actions["next_solution"].triggered.connect(self._next_layout_solution)
        self._actions["apply_layout"].triggered.connect(self._apply_layout)
        self._actions["export_selected_svg"].triggered.connect(
            self._export_selected_solution_svg
        )
        self._actions["export_selected_dxf"].triggered.connect(
            self._export_selected_solution_dxf
        )
        self._actions["export_selected_pdf"].triggered.connect(
            self._export_selected_solution_pdf
        )
        self._actions["export_selected_json"].triggered.connect(
            self._export_selected_solution_json
        )
        self._actions["export_selected_csv"].triggered.connect(
            self._export_selected_solution_csv
        )

        self._reload_recent_files_menu()

    def _build_workspace(self):
        self.workspace = BoardWorkspace(self.services)
        self.welcome = WelcomeScreen()
        self.welcome.new_project_requested.connect(self._new_project)
        self.welcome.open_project_requested.connect(self._open_project)
        self.welcome.open_recent_requested.connect(self._open_recent_project)
        self.welcome.import_pieces_requested.connect(self._import_pieces_from_csv)
        self.welcome.preferences_requested.connect(self._open_preferences)
        self.welcome.demo_project_requested.connect(self._new_demo_project)

        self._central_stack = QStackedWidget()
        self._central_stack.addWidget(self.welcome)
        self._central_stack.addWidget(self.workspace)
        self.setCentralWidget(self._central_stack)
        self._show_welcome_screen()

    def _show_welcome_screen(self) -> None:
        self.welcome.set_recent_files(self.services.recent_files.existing_files())
        self._central_stack.setCurrentWidget(self.welcome)
        self.statusBar().showMessage("Pantalla de inicio", 2000)

    def _show_workspace(self) -> None:
        self._central_stack.setCurrentWidget(self.workspace)

    def _build_panels(self):
        self.explorer = QTreeWidget()
        self.explorer.setHeaderHidden(True)
        self.explorer.itemSelectionChanged.connect(self._on_explorer_selection_changed)

        self.explorer.itemDoubleClicked.connect(self._on_explorer_item_double_clicked)

        explorer_dock = QDockWidget("Explorer", self)
        explorer_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        explorer_dock.setWidget(self.explorer)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, explorer_dock)

        self.inspector = QTextEdit()
        self.inspector.setReadOnly(True)
        self.inspector.setText("Inspector\n\nSin selección")

        inspector_dock = QDockWidget("Inspector", self)
        inspector_dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        inspector_dock.setWidget(self.inspector)
        self.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea,
            inspector_dock,
        )

        console = QTextEdit()
        console.setReadOnly(True)
        console.setText("Timeline / Consola / Eventos")

        console_dock = QDockWidget("Timeline", self)
        console_dock.setAllowedAreas(Qt.DockWidgetArea.BottomDockWidgetArea)
        console_dock.setWidget(console)

        self.addDockWidget(
            Qt.DockWidgetArea.BottomDockWidgetArea,
            console_dock,
        )

        self.solutions_table = QTableWidget()
        self.solutions_table.setColumnCount(7)
        self.solutions_table.setHorizontalHeaderLabels(
            [
                "#",
                "Piezas",
                "Huecos",
                "Tablero libre",
                "Largo",
                "Ancho",
                "Score",
            ]
        )
        self.solutions_table.cellDoubleClicked.connect(
            self._on_solution_table_double_clicked
        )
        self.solutions_table.cellClicked.connect(
            lambda row, column: self._select_solution_from_table(row)
        )

        self.comparator_sort = QComboBox()
        for key, label in SORT_LABELS:
            self.comparator_sort.addItem(label, key)
        self.comparator_sort.currentIndexChanged.connect(
            self._on_comparator_sort_changed
        )

        self.comparator_complete_only = QCheckBox("Solo soluciones completas")
        self.comparator_complete_only.toggled.connect(
            self._on_comparator_filter_toggled
        )

        controls = QHBoxLayout()
        controls.addWidget(QLabel("Ordenar por:"))
        controls.addWidget(self.comparator_sort)
        controls.addWidget(self.comparator_complete_only)
        controls.addStretch(1)

        self.pin_reference_button = QPushButton("Fijar como referencia")
        self.pin_reference_button.clicked.connect(self._pin_selected_as_reference)
        controls.addWidget(self.pin_reference_button)

        self.solution_thumbnails = QListWidget()
        self.solution_thumbnails.setViewMode(QListWidget.ViewMode.IconMode)
        self.solution_thumbnails.setFlow(QListWidget.Flow.LeftToRight)
        self.solution_thumbnails.setWrapping(False)
        self.solution_thumbnails.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.solution_thumbnails.setMovement(QListWidget.Movement.Static)
        self.solution_thumbnails.setIconSize(DEFAULT_THUMBNAIL_SIZE)
        self.solution_thumbnails.setSpacing(8)
        self.solution_thumbnails.setMaximumHeight(DEFAULT_THUMBNAIL_SIZE.height() + 48)
        self.solution_thumbnails.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.solution_thumbnails.itemClicked.connect(
            self._on_solution_thumbnail_clicked
        )

        self.solution_differences = QTextEdit()
        self.solution_differences.setReadOnly(True)
        self.solution_differences.setPlaceholderText(
            "Diferencias respecto a la solución de referencia"
        )
        self.solution_differences.setMaximumHeight(140)

        comparator_panel = QWidget()
        comparator_layout = QVBoxLayout(comparator_panel)
        comparator_layout.setContentsMargins(0, 0, 0, 0)
        comparator_layout.addLayout(controls)
        comparator_layout.addWidget(self.solution_thumbnails)
        comparator_layout.addWidget(self.solutions_table)
        comparator_layout.addWidget(QLabel("Diferencias vs referencia"))
        comparator_layout.addWidget(self.solution_differences)

        solutions_dock = QDockWidget("Comparador de soluciones", self)
        self.tabifyDockWidget(console_dock, solutions_dock)
        console_dock.raise_()
        solutions_dock.setAllowedAreas(Qt.DockWidgetArea.BottomDockWidgetArea)
        solutions_dock.setWidget(comparator_panel)
        self.addDockWidget(
            Qt.DockWidgetArea.BottomDockWidgetArea,
            solutions_dock,
        )

    def _build_statusbar(self):
        status = QStatusBar(self)
        status.showMessage("BoardComposer Studio listo")
        self.setStatusBar(status)

    def _load_empty_project(self):
        project = StudioProject(
            project_id="PRJ-UNTITLED",
            name="Proyecto sin título",
            boards=[],
            pieces=[],
            placements=[],
        )

        self.services.projects.new_project(project)
        self.services.layout.clear_solutions()
        self.workspace.reload_project()
        self._reload_explorer()
        self._reload_solution_table()
        self.update_window_title()

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
        self.update_window_title()

    def _reload_explorer(self):
        project = self.services.projects.current_project
        previous_signal_state = self.explorer.blockSignals(True)

        try:
            self.explorer.clear()

            if project is None:
                return

            root = QTreeWidgetItem([project.name])
            boards_root = QTreeWidgetItem(["Tableros"])
            pieces_root = QTreeWidgetItem(["Piezas"])
            solutions_root = QTreeWidgetItem(["Soluciones"])
            selected_solution_item = None

            for board in project.boards:
                board_label = (
                    f"{board.board_id} — {board.length_mm:g} x {board.width_mm:g} "
                    f"x {board.thickness_mm:g} mm — {board.quantity} ud."
                )
                item = QTreeWidgetItem([board_label])
                item.setData(
                    0,
                    Qt.ItemDataRole.UserRole,
                    f"board:{board.board_id}",
                )
                boards_root.addChild(item)

            for piece in project.pieces:
                piece_label = (
                    f"{piece.piece_id} — {piece.length_mm:g} x {piece.width_mm:g} mm"
                )
                item = QTreeWidgetItem([piece_label])
                item.setData(
                    0,
                    Qt.ItemDataRole.UserRole,
                    f"piece:{piece.piece_id}",
                )
                pieces_root.addChild(item)

            selected_solution_index = self.services.layout.selected_solution_index

            for index, solution in enumerate(self.services.layout.solutions):
                prefix = "✓ " if index == selected_solution_index else ""

                item = QTreeWidgetItem(
                    [
                        f"{prefix}Solución {index + 1} — "
                        f"{len(solution.placements)} piezas — "
                        f"{solution.waste_ratio:.1%} huecos"
                    ]
                )

                item.setData(
                    0,
                    Qt.ItemDataRole.UserRole,
                    f"solution:{index}",
                )

                solutions_root.addChild(item)

                if index == selected_solution_index:
                    selected_solution_item = item

            root.addChild(boards_root)
            root.addChild(pieces_root)
            root.addChild(solutions_root)

            self.explorer.addTopLevelItem(root)
            self.explorer.expandAll()

            if selected_solution_item is not None:
                self.explorer.setCurrentItem(selected_solution_item)

        finally:
            self.explorer.blockSignals(previous_signal_state)

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

        if kind == "solution":
            self._select_layout_solution(int(object_id))
            return

        if kind == "board":
            board = next(
                board for board in project.boards if board.board_id == object_id
            )
            self.inspector.setText(
                "Inspector\n\n"
                f"Tablero: {board.board_id}\n"
                f"Dimensiones: {board.length_mm:g} x "
                f"{board.width_mm:g} mm\n"
                f"Espesor: {board.thickness_mm:g} mm\n"
                f"Cantidad: {board.quantity}\n"
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
                f"Dimensiones: {piece.length_mm:g} x "
                f"{piece.width_mm:g} mm\n"
                f"Material: {piece.material}"
            )

    def _new_project(self):
        if not self._confirm_discard_unsaved_changes():
            return

        self._load_empty_project()
        self._show_workspace()
        self.statusBar().showMessage("Nuevo proyecto vacío creado", 3000)

    def _new_demo_project(self):
        if not self._confirm_discard_unsaved_changes():
            return

        self._load_demo_project()
        self.services.layout.clear_solutions()
        self._show_workspace()
        self.statusBar().showMessage("Proyecto demo creado", 3000)

    def _add_board(self):
        project = self.services.projects.current_project

        if project is None:
            self._load_empty_project()
            project = self.services.projects.current_project

        if project is None:
            return

        dialog = NewBoardDialog(self)

        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        data = dialog.board_data()

        if any(board.board_id == data["board_id"] for board in project.boards):
            self.statusBar().showMessage(
                f"Ya existe un tablero con id {data['board_id']}",
                3000,
            )
            return

        project.boards.append(
            StudioBoard(
                board_id=data["board_id"],
                length_mm=data["length_mm"],
                width_mm=data["width_mm"],
                material=data["material"],
                thickness_mm=data["thickness_mm"],
                quantity=data["quantity"],
            )
        )

        self.services.projects.mark_modified()
        self.workspace.reload_project()
        self._reload_explorer()
        self.update_window_title()

        self.statusBar().showMessage("Tablero añadido", 3000)

    def _import_boards_from_csv(self) -> None:
        project = self.services.projects.current_project

        if project is None:
            self._load_empty_project()
            project = self.services.projects.current_project

        if project is None:
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Importar inventario de tableros (CSV/Excel)",
            "",
            "CSV / Excel (*.csv *.xlsx);;CSV (*.csv);;Excel (*.xlsx);;"
            "Todos los archivos (*)",
        )

        if not file_path:
            return

        existing_ids = {board.board_id.casefold() for board in project.boards}
        result = import_boards_from_file(file_path, existing_ids=existing_ids)

        if result.file_errors:
            QMessageBox.warning(
                self,
                "Importar inventario de tableros",
                "\n".join(result.file_errors),
            )
            return

        dialog = ImportBoardsPreviewDialog(result, self)

        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        for board in result.valid_boards:
            project.boards.append(board)

        self.services.projects.mark_modified()
        self.workspace.reload_project()
        self._reload_explorer()
        self.update_window_title()

        self.statusBar().showMessage(
            f"{len(result.valid_boards)} tablero(s) importado(s)",
            5000,
        )

    def _import_pieces_from_csv(self) -> None:
        project = self.services.projects.current_project

        if project is None:
            self._load_empty_project()
            project = self.services.projects.current_project

        if project is None:
            return

        self._show_workspace()

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Importar piezas (CSV/Excel)",
            "",
            "CSV / Excel (*.csv *.xlsx);;CSV (*.csv);;Excel (*.xlsx);;"
            "Todos los archivos (*)",
        )

        if not file_path:
            return

        existing_ids = {piece.piece_id.casefold() for piece in project.pieces}
        result = import_pieces_from_file(file_path, existing_ids=existing_ids)

        if result.file_errors:
            QMessageBox.warning(
                self,
                "Importar piezas",
                "\n".join(result.file_errors),
            )
            return

        dialog = ImportPiecesPreviewDialog(result, self)

        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        for piece in result.valid_pieces:
            project.pieces.append(piece)
            x_mm, y_mm = self._find_free_piece_position(
                piece.length_mm,
                piece.width_mm,
            )
            project.placements.append(
                StudioPlacement(
                    piece_id=piece.piece_id,
                    x_mm=x_mm,
                    y_mm=y_mm,
                    rotated=False,
                    rotation=0,
                    board_id=project.boards[0].board_id if project.boards else None,
                    board_instance=0,
                    stock_panel_index=0 if project.boards else None,
                )
            )

        self.services.projects.mark_modified()
        self.workspace.reload_project()
        self._reload_explorer()
        self.update_window_title()

        self.statusBar().showMessage(
            f"{len(result.valid_pieces)} pieza(s) importada(s)",
            5000,
        )

    def _add_piece(self):
        project = self.services.projects.current_project

        if project is None:
            self._load_empty_project()
            project = self.services.projects.current_project

        if project is None:
            return

        dialog = NewPieceDialog(self)

        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        data = dialog.piece_data()

        new_piece_id = data["piece_id"].strip()

        if not new_piece_id:
            self.statusBar().showMessage(
                "El identificador de la pieza no puede estar vacío",
                3000,
            )
            return

        existing_ids = {piece.piece_id.strip().casefold() for piece in project.pieces}

        quantity = data.get("quantity", 1)
        piece_ids = self._generate_piece_ids(new_piece_id, quantity, existing_ids)

        if piece_ids is None:
            self.statusBar().showMessage(
                f"Ya existe una pieza con id {new_piece_id}",
                3000,
            )
            return

        for piece_id in piece_ids:
            project.pieces.append(
                StudioPiece(
                    piece_id=piece_id,
                    length_mm=data["length_mm"],
                    width_mm=data["width_mm"],
                    material=data["material"],
                    thickness_mm=data["thickness_mm"],
                )
            )

            x_mm, y_mm = self._find_free_piece_position(
                data["length_mm"],
                data["width_mm"],
            )

            project.placements.append(
                StudioPlacement(
                    piece_id=piece_id,
                    x_mm=x_mm,
                    y_mm=y_mm,
                    rotated=False,
                    rotation=0,
                    board_id=project.boards[0].board_id if project.boards else None,
                    board_instance=0,
                    stock_panel_index=0 if project.boards else None,
                )
            )

        self.services.projects.mark_modified()
        self.workspace.reload_project()
        self._reload_explorer()
        self.update_window_title()

        if len(piece_ids) > 1:
            self.statusBar().showMessage(f"{len(piece_ids)} piezas añadidas", 3000)
        else:
            self.statusBar().showMessage("Pieza añadida", 3000)

    @staticmethod
    def _generate_piece_ids(
        base_id: str,
        quantity: int,
        existing_ids: set[str],
    ) -> list[str] | None:
        """Generate `quantity` unique piece ids derived from `base_id`.

        For quantity 1, `base_id` is used verbatim (and must be free).
        For quantity > 1, ids are suffixed as `base-1`, `base-2`, etc.,
        skipping any suffix that collides with an existing id.
        Returns None if `base_id` itself already collides with an existing id.
        """
        if base_id.casefold() in existing_ids:
            return None

        if quantity <= 1:
            return [base_id]

        generated_ids: list[str] = []
        reserved = set(existing_ids)
        suffix = 1

        while len(generated_ids) < quantity:
            candidate = f"{base_id}-{suffix}"
            suffix += 1
            if candidate.casefold() in reserved:
                continue
            reserved.add(candidate.casefold())
            generated_ids.append(candidate)

        return generated_ids

    @staticmethod
    def _panel_info_text(project, placement) -> str:
        """Return a human-readable label for a placement's physical panel."""
        if placement is None or placement.board_id is None:
            return "Sin tablero asignado"

        board = next(
            (board for board in project.boards if board.board_id == placement.board_id),
            None,
        )
        quantity = board.quantity if board is not None else 1

        if quantity > 1:
            return (
                f"{placement.board_id} · instancia "
                f"{placement.board_instance + 1}/{quantity}"
            )

        return placement.board_id

    def refresh_inspector_for_piece(self, piece_id: str):
        """Refresh inspector panel for the selected piece."""
        project = self.services.projects.current_project
        if project is None:
            return

        piece = project.piece_by_id(piece_id)
        placement = next(
            (
                placement
                for placement in project.placements
                if placement.piece_id == piece_id
            ),
            None,
        )

        if placement is None:
            self.inspector.setText(
                "Inspector\n\n"
                f"Pieza: {piece.piece_id}\n"
                f"Dimensiones: {piece.length_mm:g} x {piece.width_mm:g} mm\n"
                f"Material: {piece.material}\n"
                "Sin colocar en el Workspace"
            )
            return

        self.inspector.setText(
            "Inspector\n\n"
            f"Pieza: {piece.piece_id}\n"
            f"Dimensiones: {piece.length_mm:g} x {piece.width_mm:g} mm\n"
            f"Posición: {placement.x_mm:g}, {placement.y_mm:g} mm\n"
            f"Tablero: {self._panel_info_text(project, placement)}\n"
            f"Material: {piece.material}"
        )

    def update_window_title(self):
        """Update the window title from the current project state."""
        project = self.services.projects.current_project
        marker = "● " if self.services.projects.is_modified else ""

        if project is None:
            self.setWindowTitle("BoardComposer Studio")
            return

        self.setWindowTitle(f"{marker}BoardComposer Studio — {project.name}")

    def update_undo_redo(self):
        """Refresh the enabled state of undo and redo actions."""
        self._actions["undo"].setEnabled(self.services.commands.can_undo())
        self._actions["redo"].setEnabled(self.services.commands.can_redo())

        self._actions["undo"].setShortcut("Ctrl+Z")
        self._actions["redo"].setShortcut("Ctrl+Shift+Z")

    def _undo(self):
        self.services.commands.undo()
        self.workspace.reload_project()
        self.update_undo_redo()

    def _redo(self):
        self.services.commands.redo()
        self.workspace.reload_project()
        self.update_undo_redo()

    def _rotate_selected_piece(self):
        selected = self.workspace.scene().selectedItems()

        if len(selected) != 1:
            return

        item = selected[0]

        if not isinstance(item, BoardPieceItem):
            return

        piece_id = item.piece_id
        project = self.services.projects.current_project

        if project is None:
            return

        placement = project.placement_by_piece_id(piece_id)
        if placement is None:
            return

        old_rotation = placement.rotation
        new_rotation = 90 if old_rotation == 0 else 0

        if not self.workspace.can_rotate_item(item, new_rotation):
            self.statusBar().showMessage(
                "La pieza no puede rotarse en esa posición",
                3000,
            )
            return

        command = RotatePieceCommand(
            self.services,
            piece_id,
            old_rotation,
            new_rotation,
        )

        self.services.commands.execute(command)

        self.workspace.reload_project()
        self.workspace.select_piece(piece_id)
        self.refresh_inspector_for_piece(piece_id)
        self.services.projects.mark_modified()
        self.update_window_title()
        self.update_undo_redo()

    def _delete_selected_piece(self):
        piece_id = self.workspace.selection.current()
        if piece_id is None:
            return

        command = DeletePieceCommand(self.services, piece_id)

        self.services.commands.execute(command)

        self.workspace.selection.clear()
        self.services.selection.clear()

        self.services.layout.clear_solutions()
        self.workspace.reload_project()
        self._reload_explorer()
        self._reload_solution_table()

        self.workspace.selection.sync_inspector(self)

        self.services.projects.mark_modified()
        self.update_window_title()
        self.update_undo_redo()

    def _open_preferences(self) -> None:
        dialog = PreferencesDialog(self.services.preferences.current, self)
        if dialog.exec() != PreferencesDialog.DialogCode.Accepted:
            return
        self.services.preferences.update(dialog.preferences())
        self._apply_preferences()
        self.statusBar().showMessage("Preferencias guardadas", 3000)

    def _apply_preferences(self) -> None:
        from PySide6.QtWidgets import QApplication

        from studio.theme import apply_theme

        app = QApplication.instance()
        if app is not None:
            apply_theme(app, self.services.preferences.current.theme)
        self.workspace.reload_project()
        self._reload_explorer()

    def _solve_layout(self):
        solution = self.services.layout.solve_current_project()
        self._comparator_reference_index = None

        if solution is None:
            self._show_no_solution_diagnosis()
            self.statusBar().showMessage("No se pudo calcular layout", 3000)
            return

        self._reload_solution_table()
        self._show_layout_solution(solution)
        self._reload_explorer()

        solution_count = len(self.services.layout.solutions)

        if not solution.is_complete:
            self.statusBar().showMessage(
                f"Layout parcial: {len(solution.omitted_piece_ids)} pieza(s) "
                f"sin colocar de {solution_count} soluciones",
                5000,
            )
            return

        self.statusBar().showMessage(
            f"Layout calculado: {solution_count} soluciones",
            3000,
        )

    def _show_no_solution_diagnosis(self) -> None:
        lines = ["Sin solución", ""]
        lines.extend(self.services.layout.stats_summary_lines())
        self.inspector.setText("\n".join(lines))

    def _on_comparator_sort_changed(self, index: int) -> None:
        del index
        self._comparator_sort_by = self.comparator_sort.currentData() or "ranking"
        self._reload_solution_table()

    def _on_comparator_filter_toggled(self, checked: bool) -> None:
        self._comparator_complete_only = checked
        self._reload_solution_table()

    def _reload_solution_table(self):
        self.solutions_table.setRowCount(0)
        self.solution_thumbnails.clear()
        solutions = self.services.layout.solutions
        highlights = self.services.layout.solution_highlights
        self._solution_display_indexes = ordered_solution_indexes(
            solutions,
            sort_by=self._comparator_sort_by,
            complete_only=self._comparator_complete_only,
            board_waste=self.services.layout.board_waste_ratio,
        )

        project = self.services.layout.solved_project
        svgs = [
            solution_to_svg(solutions[index], project)
            for index in self._solution_display_indexes
        ]
        pixmaps = solution_thumbnails(svgs, box=DEFAULT_THUMBNAIL_SIZE)

        for row, solution_index in enumerate(self._solution_display_indexes):
            solution = solutions[solution_index]
            self.solutions_table.insertRow(row)

            placed_label = str(len(solution.placements))
            if not solution.is_complete:
                placed_label += f" ({len(solution.omitted_piece_ids)} sin colocar)"

            values = [
                str(solution_index + 1),
                placed_label,
                f"{solution.waste_ratio:.1%}",
                f"{self.services.layout.board_waste_ratio(solution):.1%}",
                f"{solution.total_length_mm:.0f}",
                f"{solution.total_width_mm:.0f}",
                f"{solution.score.total:.2f}",
            ]

            row_highlights = highlights.get(solution_index, [])

            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                if row_highlights:
                    item.setToolTip("Mejor en: " + ", ".join(row_highlights))
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)
                self.solutions_table.setItem(row, column, item)

            thumb = QListWidgetItem(f"#{solution_index + 1}")
            thumb.setData(Qt.ItemDataRole.UserRole, solution_index)
            thumb.setIcon(QIcon(pixmaps[row]))
            thumb.setSizeHint(
                QSize(
                    DEFAULT_THUMBNAIL_SIZE.width() + 16,
                    DEFAULT_THUMBNAIL_SIZE.height() + 28,
                )
            )
            if row_highlights:
                thumb.setToolTip("Mejor en: " + ", ".join(row_highlights))
            self.solution_thumbnails.addItem(thumb)

        self.solutions_table.resizeColumnsToContents()

        selected = self.services.layout.selected_solution_index
        if selected in self._solution_display_indexes:
            display_row = self._solution_display_indexes.index(selected)
            self.solutions_table.selectRow(display_row)
            self.solution_thumbnails.setCurrentRow(display_row)

        self._reload_solution_differences()

    def _pin_selected_as_reference(self) -> None:
        solutions = self.services.layout.solutions
        selected = self.services.layout.selected_solution_index
        if not solutions or selected < 0 or selected >= len(solutions):
            self.statusBar().showMessage("Primero selecciona una solución", 3000)
            return
        self._comparator_reference_index = selected
        self._reload_solution_differences()
        self.statusBar().showMessage(
            f"Referencia fijada en solución #{selected + 1}",
            3000,
        )

    def _reload_solution_differences(self) -> None:
        solutions = self.services.layout.solutions
        if len(solutions) < 2:
            self.solution_differences.setPlainText(
                "\n".join(
                    format_diff_unavailable(
                        "Se necesitan al menos dos soluciones para comparar "
                        "diferencias."
                    )
                )
            )
            return

        candidate_index = self.services.layout.selected_solution_index
        if candidate_index < 0 or candidate_index >= len(solutions):
            self.solution_differences.setPlainText(
                "\n".join(
                    format_diff_unavailable("Selecciona una solución en el comparador.")
                )
            )
            return

        reference_index = self._comparator_reference_index
        if reference_index is None or reference_index >= len(solutions):
            reference_index = 0 if candidate_index != 0 else min(1, len(solutions) - 1)
            self._comparator_reference_index = reference_index

        reference = solutions[reference_index]
        candidate = solutions[candidate_index]
        layout = self.services.layout
        diff = compare_solutions(
            reference,
            candidate,
            reference_index=reference_index,
            candidate_index=candidate_index,
            board_waste_reference=layout.board_waste_ratio(reference),
            board_waste_candidate=layout.board_waste_ratio(candidate),
        )
        self.solution_differences.setPlainText("\n".join(diff.summary_lines()))

    def _show_layout_solution(self, solution):
        solution_count = len(self.services.layout.solutions)
        selected_index = self.services.layout.selected_solution_index + 1
        strategy_name = self.services.layout.strategy_name or "desconocida"

        lines = [
            "Layout calculado",
            "",
            f"Solución: {selected_index} / {solution_count}",
            f"Estrategia: {strategy_name}",
            f"Piezas colocadas: {len(solution.placements)}",
            f"Largo total: {solution.total_length_mm:.0f} mm",
            f"Ancho total: {solution.total_width_mm:.0f} mm",
            f"Huecos internos: {solution.waste_ratio:.1%}",
            f"Material libre: {self.services.layout.board_waste_ratio(solution):.1%}",
        ]

        if not solution.is_complete:
            lines.append("Piezas omitidas: " + ", ".join(solution.omitted_piece_ids))

        if solution.offcuts:
            lines.append(
                f"Retales aprovechables: {len(solution.offcuts)} "
                f"(área total {solution.total_offcut_area_mm2:.0f} mm²)"
            )

        highlights = self.services.layout.solution_highlights.get(
            self.services.layout.selected_solution_index
        )
        if highlights:
            lines.append("Puntos clave: " + ", ".join(highlights))

        if solution.explanation.strengths or solution.explanation.weaknesses:
            lines.append("")
            lines.extend(f"+ {strength}" for strength in solution.explanation.strengths)
            lines.extend(
                f"- {weakness}" for weakness in solution.explanation.weaknesses
            )

        stats_lines = self.services.layout.stats_summary_lines()

        if stats_lines:
            lines.extend(["", *stats_lines])

        self.inspector.setText("\n".join(lines))

    def _apply_layout(self):
        if not self.services.layout.apply_last_solution_to_current_project():
            self.statusBar().showMessage("Primero calcula un layout", 3000)
            return

        self.workspace.reload_project()
        self.services.selection.clear()
        self._reload_explorer()
        self.update_undo_redo()
        self.update_window_title()

        selected_index = self.services.layout.selected_solution_index + 1
        solution_count = len(self.services.layout.solutions)

        self.statusBar().showMessage(
            f"Solución {selected_index}/{solution_count} aplicada al proyecto",
            3000,
        )

    def _previous_layout_solution(self):
        solution = self.services.layout.select_previous_solution()

        if solution is None:
            self.statusBar().showMessage("No hay soluciones calculadas", 3000)
            return

        self.workspace.preview_solution(solution)
        self._reload_solution_table()
        self._show_layout_solution(solution)
        self._reload_explorer()
        self._reload_solution_table()

        index = self.services.layout.selected_solution_index + 1
        total = len(self.services.layout.solutions)

        self.statusBar().showMessage(
            f"Previsualizando solución {index}/{total}. "
            "Pulsa 'Aplicar layout calculado' para conservarla.",
            5000,
        )

    def _next_layout_solution(self):
        solution = self.services.layout.select_next_solution()

        if solution is None:
            self.statusBar().showMessage("No hay soluciones calculadas", 3000)
            return

        self.workspace.preview_solution(solution)
        self._show_layout_solution(solution)
        self._reload_explorer()

        index = self.services.layout.selected_solution_index + 1
        total = len(self.services.layout.solutions)

        self.statusBar().showMessage(
            f"Previsualizando solución {index}/{total}. "
            "Pulsa 'Aplicar layout calculado' para conservarla.",
            5000,
        )

    def _on_solution_table_double_clicked(self, row: int, column: int):
        del column
        self._select_solution_from_table(row)

    def _select_solution_from_table(self, row: int):
        if row < 0 or row >= len(self._solution_display_indexes):
            return
        self._select_layout_solution(self._solution_display_indexes[row])

    def _on_solution_thumbnail_clicked(self, item: QListWidgetItem) -> None:
        solution_index = item.data(Qt.ItemDataRole.UserRole)
        if solution_index is None:
            return
        self._select_layout_solution(int(solution_index))

    def _export_selected_solution_svg(self):
        solution = self.services.layout.selected_solution

        if solution is None:
            self.statusBar().showMessage("Primero calcula un layout", 3000)
            return

        selected_index = self.services.layout.selected_solution_index + 1
        default_filename = f"boardcomposer-solution-{selected_index}.svg"

        path, _selected_filter = QFileDialog.getSaveFileName(
            self,
            "Exportar solución seleccionada",
            default_filename,
            "SVG (*.svg)",
        )

        if not path:
            return

        try:
            Path(path).write_text(
                solution_to_svg(solution, self.services.layout.solved_project),
                encoding="utf-8",
            )
        except OSError as exc:
            self.statusBar().showMessage(f"No se pudo exportar SVG: {exc}", 5000)
            return

        self.statusBar().showMessage(f"SVG exportado: {path}", 5000)

    def _export_selected_solution_dxf(self):
        solution = self.services.layout.selected_solution

        if solution is None:
            self.statusBar().showMessage("Primero calcula un layout", 3000)
            return

        selected_index = self.services.layout.selected_solution_index + 1
        default_filename = f"boardcomposer-solution-{selected_index}.dxf"

        path, _selected_filter = QFileDialog.getSaveFileName(
            self,
            "Exportar solución seleccionada",
            default_filename,
            "DXF (*.dxf)",
        )

        if not path:
            return

        try:
            Path(path).write_text(
                solution_to_dxf(solution, self.services.layout.solved_project),
                encoding="utf-8",
            )
        except OSError as exc:
            self.statusBar().showMessage(f"No se pudo exportar DXF: {exc}", 5000)
            return

        self.statusBar().showMessage(f"DXF exportado: {path}", 5000)

    def _export_selected_solution_pdf(self):
        solution = self.services.layout.selected_solution

        if solution is None:
            self.statusBar().showMessage("Primero calcula un layout", 3000)
            return

        selected_index = self.services.layout.selected_solution_index + 1
        default_filename = f"boardcomposer-solution-{selected_index}.pdf"

        path, _selected_filter = QFileDialog.getSaveFileName(
            self,
            "Exportar solución seleccionada",
            default_filename,
            "PDF (*.pdf)",
        )

        if not path:
            return

        try:
            Path(path).write_bytes(
                solution_to_pdf(solution, self.services.layout.solved_project)
            )
        except OSError as exc:
            self.statusBar().showMessage(f"No se pudo exportar PDF: {exc}", 5000)
            return

        self.statusBar().showMessage(f"PDF exportado: {path}", 5000)

    def _export_selected_solution_json(self):
        solution = self.services.layout.selected_solution

        if solution is None:
            self.statusBar().showMessage("Primero calcula un layout", 3000)
            return

        selected_index = self.services.layout.selected_solution_index + 1
        default_filename = f"boardcomposer-solution-{selected_index}.json"

        path, _selected_filter = QFileDialog.getSaveFileName(
            self,
            "Exportar solución seleccionada",
            default_filename,
            "JSON (*.json)",
        )

        if not path:
            return

        try:
            Path(path).write_text(
                solution_to_json(
                    solution,
                    self.services.layout.solved_project,
                    strategy_name=self.services.layout.strategy_name,
                    solution_index=self.services.layout.selected_solution_index,
                ),
                encoding="utf-8",
            )
        except OSError as exc:
            self.statusBar().showMessage(f"No se pudo exportar JSON: {exc}", 5000)
            return

        self.statusBar().showMessage(f"JSON exportado: {path}", 5000)

    def _export_selected_solution_csv(self):
        solution = self.services.layout.selected_solution

        if solution is None:
            self.statusBar().showMessage("Primero calcula un layout", 3000)
            return

        selected_index = self.services.layout.selected_solution_index + 1
        default_filename = f"boardcomposer-solution-{selected_index}.csv"

        path, _selected_filter = QFileDialog.getSaveFileName(
            self,
            "Exportar solución seleccionada",
            default_filename,
            "CSV (*.csv)",
        )

        if not path:
            return

        try:
            Path(path).write_text(solution_to_csv(solution), encoding="utf-8")
        except OSError as exc:
            self.statusBar().showMessage(f"No se pudo exportar CSV: {exc}", 5000)
            return

        self.statusBar().showMessage(f"CSV exportado: {path}", 5000)

    def _save_project(self):
        project = self.services.projects.current_project

        if project is None:
            self.statusBar().showMessage("No hay proyecto para guardar", 3000)
            return

        filename = self.services.projects.filename

        if filename is None:
            self._save_project_as()
            return

        try:
            save_project(project, filename)
        except OSError as exc:
            self.statusBar().showMessage(f"No se pudo guardar: {exc}", 5000)
            return

        self.services.projects.mark_saved(filename)
        self._reload_recent_files_menu()
        self.services.recent_files.add(filename)
        self.update_window_title()
        self.statusBar().showMessage(f"Proyecto guardado: {filename}", 5000)

    def _save_project_as(self):
        project = self.services.projects.current_project

        if project is None:
            self.statusBar().showMessage("No hay proyecto para guardar", 3000)
            return

        path, _selected_filter = QFileDialog.getSaveFileName(
            self,
            "Guardar proyecto",
            "boardcomposer-project.bcproj",
            "BoardComposer Project (*.bcproj)",
        )

        if not path:
            return

        try:
            save_project(project, path)
        except OSError as exc:
            self.statusBar().showMessage(f"No se pudo guardar: {exc}", 5000)
            return

        self.services.projects.mark_saved(path)
        self._reload_recent_files_menu()
        self.services.recent_files.add(path)
        self.update_window_title()
        self.statusBar().showMessage(f"Proyecto guardado: {path}", 5000)

    def _open_project(self):
        if not self._confirm_discard_unsaved_changes():
            return

        path, _selected_filter = QFileDialog.getOpenFileName(
            self,
            "Abrir proyecto",
            "",
            "BoardComposer Project (*.bcproj)",
        )

        if not path:
            return

        try:
            project = load_project(path)
        except UnsupportedProjectVersionError as error:
            QMessageBox.warning(self, "Abrir proyecto", str(error))
            return

        self.services.projects.open_project(project, path)
        self.services.recent_files.add(path)
        self._reload_recent_files_menu()
        self.services.layout.clear_solutions()

        self._show_workspace()
        self.workspace.reload_project()
        self._reload_explorer()
        self._reload_solution_table()
        self.update_window_title()

        self.statusBar().showMessage(f"Proyecto abierto: {path}", 3000)

    def _reload_recent_files_menu(self):
        self._recent_menu.clear()
        self.welcome.set_recent_files(self.services.recent_files.existing_files())

        if not self.services.recent_files.files:
            empty_action = QAction("Sin archivos recientes", self)
            empty_action.setEnabled(False)
            self._recent_menu.addAction(empty_action)
            return

        for filename in self.services.recent_files.files:
            action = QAction(filename, self)
            action.triggered.connect(
                lambda checked=False, path=filename: self._open_recent_project(path)
            )
            self._recent_menu.addAction(action)

    def _open_recent_project(self, path: str):
        if not self._confirm_discard_unsaved_changes():
            return

        try:
            project = load_project(path)
        except (UnsupportedProjectVersionError, OSError) as error:
            QMessageBox.warning(self, "Abrir proyecto", str(error))
            return

        self.services.projects.open_project(project, path)
        self.services.recent_files.add(path)
        self._reload_recent_files_menu()
        self.services.layout.clear_solutions()

        self._show_workspace()
        self.workspace.reload_project()
        self._reload_explorer()
        self._reload_solution_table()
        self.update_window_title()

        self.statusBar().showMessage(f"Proyecto abierto: {path}", 3000)

    def _confirm_discard_unsaved_changes(self) -> bool:
        if not self.services.projects.is_modified:
            return True

        result = QMessageBox.question(
            self,
            "Cambios sin guardar",
            "El proyecto tiene cambios sin guardar.\n\n"
            "¿Quieres guardarlos antes de continuar?",
            QMessageBox.StandardButton.Save
            | QMessageBox.StandardButton.Discard
            | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Save,
        )

        if result == QMessageBox.StandardButton.Cancel:
            return False

        if result == QMessageBox.StandardButton.Discard:
            return True

        self._save_project()
        return not self.services.projects.is_modified

    def _close_event(self, event):
        if not self._confirm_discard_unsaved_changes():
            event.ignore()
        else:
            event.accept()

    def closeEvent(  # pylint: disable=invalid-name
        self,
        event: QCloseEvent,
    ) -> None:
        """Handle the Qt window close event."""
        self._close_event(event)

    def _on_explorer_item_double_clicked(self, item, _column):
        data = item.data(0, Qt.ItemDataRole.UserRole)

        if not data:
            return

        kind, object_id = data.split(":", 1)

        if kind == "board":
            self._edit_board(object_id)
            return

        if kind == "piece":
            self._edit_piece(object_id)

    def _find_free_piece_position(
        self,
        length_mm: float,
        width_mm: float,
    ) -> tuple[float, float]:
        project = self.services.projects.current_project

        if project is None or not project.boards:
            return 0.0, 0.0

        board = project.boards[0]
        margin = 20.0
        x = margin
        y = margin
        row_height = 0.0

        for placement in project.placements:
            piece = project.piece_by_id(placement.piece_id)

            placed_width = (
                piece.width_mm if placement.rotation in (90, 270) else piece.length_mm
            )
            placed_height = (
                piece.length_mm if placement.rotation in (90, 270) else piece.width_mm
            )

            if x + placed_width > board.length_mm - margin:
                x = margin
                y += row_height + margin
                row_height = 0.0

            x += placed_width + margin
            row_height = max(row_height, placed_height)

        if x + length_mm > board.length_mm - margin:
            x = margin
            y += row_height + margin

        if y + width_mm > board.width_mm - margin:
            return margin, margin

        return x, y

    def _select_layout_solution(self, index: int) -> None:
        solution = self.services.layout.select_solution(index)

        if solution is None:
            return

        self.workspace.preview_solution(solution)
        self._show_layout_solution(solution)
        self._reload_explorer()
        self._reload_solution_table()

        selected_index = self.services.layout.selected_solution_index + 1
        total = len(self.services.layout.solutions)

        self.statusBar().showMessage(
            f"Previsualizando solución {selected_index}/{total}. "
            "Pulsa 'Aplicar layout calculado' para conservarla.",
            5000,
        )

    def _edit_board(self, board_id: str) -> None:
        project = self.services.projects.current_project
        if project is None:
            return

        board = next(board for board in project.boards if board.board_id == board_id)
        board_index = project.boards.index(board)

        dialog = NewBoardDialog(
            self,
            board_id=board.board_id,
            length_mm=int(board.length_mm),
            width_mm=int(board.width_mm),
            thickness_mm=int(board.thickness_mm),
            quantity=board.quantity,
            material=board.material,
            title="Editar tablero",
        )

        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        data = dialog.board_data()
        new_board_id = data["board_id"]

        if new_board_id != board_id and any(
            existing.board_id == new_board_id for existing in project.boards
        ):
            self.statusBar().showMessage(
                f"Ya existe un tablero con id {new_board_id}",
                3000,
            )
            return

        project.boards[board_index] = StudioBoard(
            board_id=new_board_id,
            length_mm=data["length_mm"],
            width_mm=data["width_mm"],
            material=data["material"],
            thickness_mm=data["thickness_mm"],
            quantity=data["quantity"],
        )

        for placement in project.placements:
            if placement.board_id == board_id:
                placement.board_id = new_board_id
                placement.board_instance = min(
                    placement.board_instance,
                    data["quantity"] - 1,
                )

        self.services.layout.clear_solutions()
        self.services.projects.mark_modified()

        self.workspace.reload_project()
        self._reload_explorer()
        self._reload_solution_table()
        self.update_window_title()

        self.statusBar().showMessage("Tablero actualizado", 3000)

    def _edit_piece(self, piece_id: str) -> None:
        project = self.services.projects.current_project
        if project is None:
            return

        piece = project.piece_by_id(piece_id)
        piece_index = project.pieces.index(piece)

        dialog = NewPieceDialog(
            self,
            piece_id=piece.piece_id,
            length_mm=int(piece.length_mm),
            width_mm=int(piece.width_mm),
            thickness_mm=int(piece.thickness_mm),
            material=piece.material,
            title="Editar pieza",
            show_quantity=False,
        )

        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        data = dialog.piece_data()
        new_piece_id = data["piece_id"].strip()

        if not new_piece_id:
            self.statusBar().showMessage(
                "El identificador de la pieza no puede estar vacío",
                3000,
            )
            return

        normalized_id = new_piece_id.casefold()

        if any(
            existing.piece_id != piece_id
            and existing.piece_id.strip().casefold() == normalized_id
            for existing in project.pieces
        ):
            self.statusBar().showMessage(
                f"Ya existe una pieza con id {new_piece_id}",
                3000,
            )
            return

        placement = project.placement_by_piece_id(piece_id)

        updated_piece = StudioPiece(
            piece_id=new_piece_id,
            length_mm=data["length_mm"],
            width_mm=data["width_mm"],
            material=data["material"],
            thickness_mm=data["thickness_mm"],
        )

        project.pieces[piece_index] = updated_piece

        if placement is not None:
            placement.piece_id = new_piece_id

        self.services.layout.clear_solutions()
        self.services.projects.mark_modified()

        self.workspace.reload_project()
        self._reload_explorer()
        self._reload_solution_table()

        self.services.selection.select_one(new_piece_id)
        self.workspace.select_piece(new_piece_id)

        position_text = ""
        panel_text = ""
        if placement is not None:
            position_text = f"Posición: {placement.x_mm:g}, {placement.y_mm:g} mm\n"
            panel_text = f"Tablero: {self._panel_info_text(project, placement)}\n"

        self.inspector.setText(
            "Inspector\n\n"
            f"Pieza: {updated_piece.piece_id}\n"
            f"Dimensiones: {updated_piece.length_mm:g} x "
            f"{updated_piece.width_mm:g} mm\n"
            f"{position_text}"
            f"{panel_text}"
            f"Material: {updated_piece.material}"
        )

        self.update_window_title()
        self.statusBar().showMessage("Pieza actualizada", 3000)
