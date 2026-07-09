"""Main window for BoardComposer Studio."""

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QDockWidget,
    QFileDialog,
    QMainWindow,
    QMenuBar,
    QMessageBox,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
)

from boardcomposer.export import solution_to_svg
from studio.commands import DeletePieceCommand, RotatePieceCommand
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.project_serializer import load_project, save_project
from studio.workspace.board_workspace import BoardWorkspace


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self, services):
        super().__init__()
        self.services = services
        self.current_project_path = None
        self.setWindowTitle("BoardComposer Studio")
        self.resize(1400, 900)

        self._build_menu()
        self._build_workspace()
        self._build_panels()
        self._build_statusbar()
        self._reload_explorer()
        self._reload_solution_table()
        self._update_window_title()

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
        self._actions["open"] = QAction("Abrir…", self)
        self._recent_menu = menus["Archivo"].addMenu("Abrir recientes")
        self._actions["open"].triggered.connect(self._open_project)
        self._actions["save"] = QAction("Guardar", self)
        self._actions["save_as"] = QAction("Guardar como…", self)
        self._actions["export_selected_svg"] = QAction(
            "Exportar solución seleccionada a SVG…",
            self,
        )
        menus["Exportar"].addAction(self._actions["export_selected_svg"])
        self._actions["export_selected_svg"].triggered.connect(
            self._export_selected_solution_svg
        )
        self._actions["exit"] = QAction("Salir", self)
        self._actions["undo"] = QAction("Deshacer", self)
        self._actions["redo"] = QAction("Rehacer", self)
        self._actions["undo"].setShortcut("Ctrl+Z")
        self._actions["redo"].setShortcut("Ctrl+Shift+Z")

        menus["Editar"].addAction(self._actions["undo"])
        menus["Editar"].addAction(self._actions["redo"])
        self._actions["rotate_piece"] = QAction("Rotar 90°", self)
        self._actions["rotate_piece"].setShortcut("R")
        menus["Editar"].addSeparator()
        menus["Editar"].addAction(self._actions["rotate_piece"])
        self._actions["delete_piece"] = QAction("Eliminar pieza", self)
        self._actions["delete_piece"].setShortcut("Backspace")
        menus["Editar"].addAction(self._actions["delete_piece"])
        self._actions["delete_piece"].triggered.connect(self._delete_selected_piece)
        self._actions["rotate_piece"].triggered.connect(self._rotate_selected_piece)
        self._actions["solve_layout"] = QAction("Calcular layout", self)
        menus["Herramientas"].addAction(self._actions["solve_layout"])
        self._actions["solve_layout"].triggered.connect(self._solve_layout)
        menus["Herramientas"].addSeparator()

        self._actions["previous_solution"] = QAction("Solución anterior", self)
        menus["Herramientas"].addAction(self._actions["previous_solution"])
        self._actions["previous_solution"].triggered.connect(
            self._previous_layout_solution
        )

        self._actions["next_solution"] = QAction("Solución siguiente", self)
        menus["Herramientas"].addAction(self._actions["next_solution"])
        self._actions["next_solution"].triggered.connect(self._next_layout_solution)

        menus["Herramientas"].addSeparator()
        self._actions["apply_layout"] = QAction("Aplicar layout calculado", self)
        menus["Herramientas"].addAction(self._actions["apply_layout"])
        self._actions["apply_layout"].triggered.connect(self._apply_layout)

        self._actions["undo"].triggered.connect(self._undo)
        self._actions["redo"].triggered.connect(self._redo)

        menus["Archivo"].addAction(self._actions["new_project"])
        menus["Archivo"].addAction(self._actions["new_demo_project"])
        menus["Archivo"].addSeparator()
        menus["Archivo"].addAction(self._actions["open"])
        menus["Archivo"].addMenu(self._recent_menu)
        menus["Archivo"].addSeparator()
        menus["Archivo"].addAction(self._actions["save"])
        menus["Archivo"].addAction(self._actions["save_as"])
        menus["Archivo"].addSeparator()
        menus["Archivo"].addAction(self._actions["exit"])

        self._actions["exit"].triggered.connect(self.close)
        self._actions["new_project"].triggered.connect(self._new_project)
        self._actions["new_demo_project"].triggered.connect(self._new_demo_project)
        self._actions["save"].triggered.connect(self._save_project)
        self._actions["save_as"].triggered.connect(self._save_project_as)
        self._reload_recent_files_menu()

    def _build_workspace(self):
        self.workspace = BoardWorkspace(self.services)
        self.setCentralWidget(self.workspace)

    def _build_panels(self):
        self.explorer = QTreeWidget()
        self.explorer.setHeaderHidden(True)
        self.explorer.itemSelectionChanged.connect(self._on_explorer_selection_changed)

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
        self.solutions_table.setColumnCount(6)
        self.solutions_table.setHorizontalHeaderLabels(
            ["#", "Piezas", "Desperdicio", "Largo", "Ancho", "Score"]
        )
        self.solutions_table.cellDoubleClicked.connect(
            self._on_solution_table_double_clicked
        )
        self.solutions_table.cellClicked.connect(
            lambda row, column: self._select_solution_from_table(row)
        )
        solutions_dock = QDockWidget("Comparador de soluciones", self)
        self.tabifyDockWidget(console_dock, solutions_dock)
        console_dock.raise_()
        solutions_dock.setAllowedAreas(Qt.DockWidgetArea.BottomDockWidgetArea)
        solutions_dock.setWidget(self.solutions_table)
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
        self._update_window_title()

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
        self._update_window_title()

    def _reload_explorer(self):
        project = self.services.projects.current_project
        previous_signal_state = self.explorer.blockSignals(True)
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
                f"{board.board_id} — {board.length_mm:g} x {board.width_mm:g} mm"
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
                    f"{solution.waste_ratio:.1%} desperdicio"
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

        if kind == "solution":
            solution = self.services.layout.select_solution(int(object_id))
            if solution is None:
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
        if not self._confirm_discard_unsaved_changes():
            return

        self._load_empty_project()
        self.statusBar().showMessage("Nuevo proyecto vacío creado", 3000)

    def _new_demo_project(self):
        if not self._confirm_discard_unsaved_changes():
            return

        self._load_demo_project()
        self.services.layout.clear_solutions()
        self.statusBar().showMessage("Proyecto demo creado", 3000)

    def refresh_inspector_for_piece(self, piece_id: str):
        """Refresh inspector panel for the selected piece."""
        project = self.services.projects.current_project
        if project is None:
            return

        piece = project.piece_by_id(piece_id)
        placement = next(
            placement
            for placement in project.placements
            if placement.piece_id == piece_id
        )

        self.inspector.setText(
            "Inspector\n\n"
            f"Pieza: {piece.piece_id}\n"
            f"Dimensiones: {piece.length_mm:g} x {piece.width_mm:g} mm\n"
            f"Posición: {placement.x_mm:g}, {placement.y_mm:g} mm\n"
            f"Material: {piece.material}"
        )

    def _update_window_title(self):
        project = self.services.projects.current_project
        marker = "● " if self.services.projects.is_modified else ""

        if project is None:
            self.setWindowTitle("BoardComposer Studio")
            return

        self.setWindowTitle(f"{marker}BoardComposer Studio — {project.name}")

    def _update_undo_redo(self):
        self._actions["undo"].setEnabled(self.services.commands.can_undo())
        self._actions["redo"].setEnabled(self.services.commands.can_redo())

        self._actions["undo"].setShortcut("Ctrl+Z")
        self._actions["redo"].setShortcut("Ctrl+Shift+Z")

    def _undo(self):
        self.services.commands.undo()
        self.workspace.reload_project()
        self._update_undo_redo()

    def _redo(self):
        self.services.commands.redo()
        self.workspace.reload_project()
        self._update_undo_redo()

    def _rotate_selected_piece(self):
        selected = self.workspace.scene().selectedItems()
        if not selected:
            return

        piece_id = selected[0].piece_id
        project = self.services.projects.current_project

        if project is None:
            return

        placement = project.placement_by_piece_id(piece_id)
        if placement is None:
            return

        old_rotation = placement.rotation
        new_rotation = 90 if old_rotation == 0 else 0

        item = self.workspace.piece_item_by_id(piece_id)
        if item is None:
            return

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
        self._update_window_title()
        self._update_undo_redo()

    def _delete_selected_piece(self):
        piece_id = self.workspace.selection.current()
        if piece_id is None:
            return

        command = DeletePieceCommand(self.services, piece_id)
        self.services.commands.execute(command)

        self.workspace.reload_project()
        self.workspace.selection.clear()
        self.workspace.selection.sync_inspector(self)

        self.services.projects.mark_modified()
        self._update_window_title()
        self._update_undo_redo()

    def _solve_layout(self):
        solution = self.services.layout.solve_current_project()

        if solution is None:
            self.statusBar().showMessage("No se pudo calcular layout", 3000)
            return

        self._reload_solution_table()
        self._show_layout_solution(solution)
        self._reload_explorer()

        solution_count = len(self.services.layout.solutions)
        self.statusBar().showMessage(
            f"Layout calculado: {solution_count} soluciones",
            3000,
        )

    def _reload_solution_table(self):
        self.solutions_table.setRowCount(0)

        for row, solution in enumerate(self.services.layout.solutions):
            self.solutions_table.insertRow(row)

            values = [
                str(row + 1),
                str(len(solution.placements)),
                f"{solution.waste_ratio:.1%}",
                f"{solution.total_length_mm:.0f}",
                f"{solution.total_width_mm:.0f}",
                f"{solution.score.total:.2f}",
            ]

            for column, value in enumerate(values):
                self.solutions_table.setItem(
                    row,
                    column,
                    QTableWidgetItem(value),
                )

        self.solutions_table.resizeColumnsToContents()

        selected_row = self.services.layout.selected_solution_index
        if self.services.layout.solutions:
            self.solutions_table.selectRow(selected_row)

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
            f"Desperdicio: {solution.waste_ratio:.1%}",
        ]

        self.inspector.setText("\n".join(lines))

    def _apply_layout(self):
        if not self.services.layout.apply_last_solution_to_current_project():
            self.statusBar().showMessage("Primero calcula un layout", 3000)
            return

        self.workspace.reload_project()
        self.services.selection.clear()
        self._reload_explorer()
        self._update_undo_redo()
        self._update_window_title()

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
        solution = self.services.layout.select_solution(row)
        if solution is None:
            return

        self.workspace.preview_solution(solution)
        self._show_layout_solution(solution)
        self._reload_solution_table()
        self._reload_explorer()

        index = row + 1
        total = len(self.services.layout.solutions)

        self.statusBar().showMessage(
            f"Previsualizando solución {index}/{total}",
            3000,
        )

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
                solution_to_svg(solution),
                encoding="utf-8",
            )
        except OSError as exc:
            self.statusBar().showMessage(f"No se pudo exportar SVG: {exc}", 5000)
            return

        self.statusBar().showMessage(f"SVG exportado: {path}", 5000)

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
        self._update_window_title()
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
        self._update_window_title()
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

        project = load_project(path)
        self.services.projects.open_project(project, path)
        self._reload_recent_files_menu()
        self.services.recent_files.add(path)
        self.services.layout.clear_solutions()

        self.workspace.reload_project()
        self._reload_explorer()
        self._reload_solution_table()
        self._update_window_title()

        self.statusBar().showMessage("Proyecto abierto", 3000)

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

    def closeEvent(self, event):
        self._close_event(event)

    def _reload_recent_files_menu(self):
        self._recent_menu.clear()

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

        project = load_project(path)
        self.services.projects.open_project(project, path)
        self.services.recent_files.add(path)
        self._reload_recent_files_menu()
        self.services.layout.clear_solutions()

        self.workspace.reload_project()
        self._reload_explorer()
        self._reload_solution_table()
        self._update_window_title()

        self.statusBar().showMessage(f"Proyecto abierto: {path}", 3000)
