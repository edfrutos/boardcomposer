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
    QInputDialog,
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

from boardcomposer.export import solution_to_svg
from studio.export_options import render_export
from dataclasses import replace as dataclass_replace
from studio.commands import (
    DeletePieceCommand,
    ImportBoardsCommand,
    ImportPiecesCommand,
    RotatePieceCommand,
)
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.project_serializer import (
    UnsupportedProjectVersionError,
    load_project,
    save_project,
)
from studio.i18n import action_keys, menu_keys, tr
from studio.workspace.board_workspace import BoardWorkspace
from studio.workspace.board_piece_item import BoardPieceItem
from studio.dialogs import (
    AboutDialog,
    ExportDialog,
    ImportBoardsPreviewDialog,
    ImportPiecesPreviewDialog,
    NewBoardDialog,
    NewPieceDialog,
    PreferencesDialog,
    ProjectTemplatePickerDialog,
    WhatsNewDialog,
)
from studio.board_csv_importer import import_boards_from_rows
from studio.piece_csv_importer import import_pieces_from_rows
from studio.import_headers import (
    BOARD_FIELD_ORDER,
    BOARD_HEADER_ALIASES,
    BOARD_REQUIRED_FIELDS,
    PIECE_FIELD_ORDER,
    PIECE_HEADER_ALIASES,
    PIECE_REQUIRED_FIELDS,
    missing_required_fields,
    resolve_header_map,
)
from studio.tabular_file import list_xlsx_sheets, load_tabular_file
from studio.dialogs.import_column_mapping_dialog import ImportColumnMappingDialog
from studio.solution_diff import (
    compare_solutions,
    compare_solutions_at_step,
    format_diff_unavailable,
)
from studio.solution_ordering import SORT_LABELS, ordered_solution_indexes
from studio.solution_thumbnail import DEFAULT_THUMBNAIL_SIZE, solution_thumbnails
from studio.units import format_length, format_size
from studio.welcome_screen import WelcomeScreen
from studio.timeline import TimelinePanel
from studio.events import catalog as events


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

        self._menus = {}
        for key in menu_keys():
            self._menus[key] = menu.addMenu("")

        self._actions = {}
        for key in action_keys():
            self._actions[key] = QAction("", self)

        self._recent_menu = self._menus["file"].addMenu("")

        self._actions["undo"].setShortcut("Ctrl+Z")
        self._actions["redo"].setShortcut("Ctrl+Shift+Z")
        self._actions["rotate_piece"].setShortcut("R")
        self._actions["delete_piece"].setShortcut("Backspace")

        self._menus["file"].addAction(self._actions["new_project"])
        self._menus["file"].addAction(self._actions["new_from_template"])
        self._menus["file"].addAction(self._actions["new_demo_project"])
        self._menus["file"].addAction(self._actions["show_welcome"])
        self._menus["file"].addSeparator()
        self._menus["file"].addAction(self._actions["open"])
        self._menus["file"].addMenu(self._recent_menu)
        self._menus["file"].addSeparator()
        self._menus["file"].addAction(self._actions["save"])
        self._menus["file"].addAction(self._actions["save_as"])
        self._menus["file"].addAction(self._actions["save_as_template"])
        self._menus["file"].addSeparator()
        self._menus["file"].addAction(self._actions["exit"])

        self._menus["edit"].addAction(self._actions["undo"])
        self._menus["edit"].addAction(self._actions["redo"])
        self._menus["edit"].addSeparator()
        self._menus["edit"].addAction(self._actions["rotate_piece"])
        self._menus["edit"].addAction(self._actions["delete_piece"])
        self._menus["edit"].addSeparator()
        self._menus["edit"].addAction(self._actions["preferences"])

        self._menus["project"].addAction(self._actions["add_board"])
        self._menus["project"].addAction(self._actions["add_piece"])
        self._menus["project"].addAction(self._actions["import_boards_csv"])
        self._menus["project"].addAction(self._actions["import_pieces_csv"])

        self._menus["export"].addAction(self._actions["export_selected"])
        self._menus["export"].addAction(self._actions["export_timeline"])

        self._menus["tools"].addAction(self._actions["solve_layout"])
        self._menus["tools"].addSeparator()
        self._menus["tools"].addAction(self._actions["previous_solution"])
        self._menus["tools"].addAction(self._actions["next_solution"])
        self._menus["tools"].addSeparator()
        self._menus["tools"].addAction(self._actions["apply_layout"])

        self._menus["help"].addAction(self._actions["whats_new"])
        self._menus["help"].addAction(self._actions["open_docs"])
        self._menus["help"].addSeparator()
        self._menus["help"].addAction(self._actions["about"])

        self._actions["open"].triggered.connect(self._open_project)
        self._actions["save"].triggered.connect(self._save_project)
        self._actions["save_as"].triggered.connect(self._save_project_as)
        self._actions["exit"].triggered.connect(self.close)
        self._actions["new_project"].triggered.connect(self._new_project)
        self._actions["new_from_template"].triggered.connect(self._new_from_template)
        self._actions["new_demo_project"].triggered.connect(self._new_demo_project)
        self._actions["show_welcome"].triggered.connect(self._show_welcome_screen)
        self._actions["save_as_template"].triggered.connect(self._save_as_template)
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
        self._actions["export_selected"].triggered.connect(
            self._export_selected_solution
        )
        self._actions["export_timeline"].triggered.connect(
            self._export_timeline_history
        )
        self._actions["whats_new"].triggered.connect(self._show_whats_new)
        self._actions["open_docs"].triggered.connect(self._open_documentation)
        self._actions["about"].triggered.connect(self._show_about)

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
        self.welcome.from_template_requested.connect(self._new_from_template)
        self.welcome.docs_requested.connect(self._open_documentation)
        self.welcome.whats_new_requested.connect(self._show_whats_new)

        self._central_stack = QStackedWidget()
        self._central_stack.addWidget(self.welcome)
        self._central_stack.addWidget(self.workspace)
        self.setCentralWidget(self._central_stack)
        self._show_welcome_screen()

    def _show_welcome_screen(self) -> None:
        self.welcome.set_recent_files(self.services.recent_files.existing_files())
        self._central_stack.setCurrentWidget(self.welcome)
        self._status("status.welcome", 2000)

    def _show_workspace(self) -> None:
        self._central_stack.setCurrentWidget(self.workspace)

    def _build_panels(self):
        self.explorer = QTreeWidget()
        self.explorer.setHeaderHidden(True)
        self.explorer.itemSelectionChanged.connect(self._on_explorer_selection_changed)

        self.explorer.itemDoubleClicked.connect(self._on_explorer_item_double_clicked)

        self.explorer_dock = QDockWidget("", self)
        self.explorer_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.explorer_dock.setWidget(self.explorer)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.explorer_dock)

        self.inspector = QTextEdit()
        self.inspector.setReadOnly(True)

        self.inspector_dock = QDockWidget("", self)
        self.inspector_dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.inspector_dock.setWidget(self.inspector)
        self.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea,
            self.inspector_dock,
        )

        self.console = TimelinePanel(
            self.services.timeline,
            language=self._ui_language(),
        )
        self.console.replay_step_changed.connect(self._on_timeline_replay_step)
        self.console.phase_step_changed.connect(self._on_timeline_phase_step)
        self.console.entry_selected.connect(self._on_timeline_entry_selected)
        self.console.export_requested.connect(self._export_timeline_history)

        self.console_dock = QDockWidget("", self)
        self.console_dock.setAllowedAreas(Qt.DockWidgetArea.BottomDockWidgetArea)
        self.console_dock.setWidget(self.console)

        self.addDockWidget(
            Qt.DockWidgetArea.BottomDockWidgetArea,
            self.console_dock,
        )

        self.solutions_table = QTableWidget()
        self.solutions_table.setColumnCount(7)
        self.solutions_table.cellDoubleClicked.connect(
            self._on_solution_table_double_clicked
        )
        self.solutions_table.cellClicked.connect(
            lambda row, column: self._select_solution_from_table(row)
        )

        self.comparator_sort = QComboBox()
        self.comparator_sort.currentIndexChanged.connect(
            self._on_comparator_sort_changed
        )

        self.comparator_complete_only = QCheckBox()
        self.comparator_complete_only.toggled.connect(
            self._on_comparator_filter_toggled
        )

        controls = QHBoxLayout()
        self.comparator_sort_label = QLabel()
        controls.addWidget(self.comparator_sort_label)
        controls.addWidget(self.comparator_sort)
        controls.addWidget(self.comparator_complete_only)
        controls.addStretch(1)

        self.pin_reference_button = QPushButton()
        self.pin_reference_button.clicked.connect(self._pin_selected_as_reference)
        controls.addWidget(self.pin_reference_button)

        self.solutions_outdated_banner = QLabel()
        self.solutions_outdated_banner.setWordWrap(True)
        self.solutions_outdated_banner.setObjectName("solutionsOutdatedBanner")
        self.solutions_outdated_banner.hide()

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
        self.solution_differences.setMaximumHeight(140)

        comparator_panel = QWidget()
        comparator_layout = QVBoxLayout(comparator_panel)
        comparator_layout.setContentsMargins(0, 0, 0, 0)
        comparator_layout.addWidget(self.solutions_outdated_banner)
        comparator_layout.addLayout(controls)
        comparator_layout.addWidget(self.solution_thumbnails)
        comparator_layout.addWidget(self.solutions_table)
        self.comparator_diff_label = QLabel()
        comparator_layout.addWidget(self.comparator_diff_label)
        comparator_layout.addWidget(self.solution_differences)

        self.solutions_dock = QDockWidget("", self)
        self.tabifyDockWidget(self.console_dock, self.solutions_dock)
        self.console_dock.raise_()
        self.solutions_dock.setAllowedAreas(Qt.DockWidgetArea.BottomDockWidgetArea)
        self.solutions_dock.setWidget(comparator_panel)
        self.addDockWidget(
            Qt.DockWidgetArea.BottomDockWidgetArea,
            self.solutions_dock,
        )

        self.clear_inspector()

    def _build_statusbar(self):
        status = QStatusBar(self)
        self.setStatusBar(status)
        status.showMessage(self._tr("status.ready"))

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
            boards_root = QTreeWidgetItem([self._tr("explorer.boards")])
            pieces_root = QTreeWidgetItem([self._tr("explorer.pieces")])
            solutions_root = QTreeWidgetItem([self._tr("explorer.solutions")])
            selected_solution_item = None

            for board in project.boards:
                board_label = (
                    f"{board.board_id} — "
                    f"{self._format_size(board.length_mm, board.width_mm, thickness_mm=board.thickness_mm)} "
                    f"— {board.quantity} {self._tr('explorer.units')}"
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
                    f"{piece.piece_id} — "
                    f"{self._format_size(piece.length_mm, piece.width_mm)}"
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
                        f"{prefix}"
                        + self._tr(
                            "explorer.solution",
                            n=index + 1,
                            pieces=len(solution.placements),
                            waste=f"{solution.waste_ratio:.1%}",
                        )
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
            self.clear_inspector()
            return

        item = selected[0]
        data = item.data(0, Qt.ItemDataRole.UserRole)
        project = self.services.projects.current_project

        if project is None or data is None:
            self.inspector.setText(f"{self._tr('inspector.title')}\n\n{item.text(0)}")
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
                f"{self._tr('inspector.title')}\n\n"
                f"{self._tr('inspector.board')}: {board.board_id}\n"
                f"{self._tr('inspector.dimensions')}: "
                f"{self._format_size(board.length_mm, board.width_mm)}\n"
                f"{self._tr('inspector.thickness')}: "
                f"{self._format_length(board.thickness_mm)}\n"
                f"{self._tr('inspector.quantity')}: {board.quantity}\n"
                f"{self._tr('inspector.material')}: {board.material}"
            )
            return

        if kind == "piece":
            piece = project.piece_by_id(object_id)
            self.services.selection.select_one(object_id)
            self.workspace.select_piece(object_id)
            self.inspector.setText(
                f"{self._tr('inspector.title')}\n\n"
                f"{self._tr('inspector.piece')}: {piece.piece_id}\n"
                f"{self._tr('inspector.dimensions')}: "
                f"{self._format_size(piece.length_mm, piece.width_mm)}\n"
                f"{self._tr('inspector.material')}: {piece.material}"
            )

    def _new_project(self):
        if not self._confirm_discard_unsaved_changes():
            return

        self._load_empty_project()
        self._show_workspace()
        self._emit(events.PROJECT_CREATED, kind="empty")
        self._status("status.new_empty")

    def _new_demo_project(self):
        if not self._confirm_discard_unsaved_changes():
            return

        self._load_demo_project()
        self.services.layout.clear_solutions()
        self._show_workspace()
        self._emit(events.PROJECT_CREATED, kind="demo")
        self._status("status.demo_created")

    def _new_from_template(self):
        if not self._confirm_discard_unsaved_changes():
            return

        manager = self.services.project_templates
        manager.refresh()
        templates = manager.list()
        if not templates:
            self._status("status.template_empty")
            QMessageBox.information(
                self,
                self._tr("template.pick_title"),
                self._tr("status.template_empty"),
            )
            return

        dialog = ProjectTemplatePickerDialog(
            templates,
            language=self._ui_language(),
            parent=self,
        )
        if dialog.exec() != dialog.DialogCode.Accepted:
            return
        name = dialog.selected_name()
        if not name:
            return

        project = manager.instantiate(name, include_placements=False)
        self.services.projects.new_project(project)
        self.services.layout.clear_solutions()
        self.workspace.reload_project()
        self._reload_explorer()
        self._reload_solution_table()
        self.update_window_title()
        self._show_workspace()
        self._emit(events.PROJECT_CREATED, kind="template", name=name)
        self._status("status.template_loaded", name=name)

    def _save_as_template(self):
        project = self.services.projects.current_project
        if project is None:
            self._status("status.template_missing_project")
            return

        name, accepted = QInputDialog.getText(
            self,
            self._tr("template.save_title"),
            self._tr("template.save_prompt"),
            text=project.name,
        )
        if not accepted:
            return
        name = name.strip()
        if not name:
            QMessageBox.warning(
                self,
                self._tr("template.save_title"),
                self._tr("template.empty_name"),
            )
            return

        include = False
        if project.placements:
            answer = QMessageBox.question(
                self,
                self._tr("template.save_title"),
                self._tr("template.save_placements"),
            )
            include = answer == QMessageBox.StandardButton.Yes

        self.services.project_templates.save_from_project(
            name,
            project,
            include_placements=include,
        )
        self._status("status.template_saved", name=name)

    def _show_whats_new(self) -> None:
        dialog = WhatsNewDialog(language=self._ui_language(), parent=self)
        dialog.exec()

    def _show_about(self) -> None:
        dialog = AboutDialog(language=self._ui_language(), parent=self)
        dialog.exec()

    def _open_documentation(self) -> None:
        from PySide6.QtCore import QUrl
        from PySide6.QtGui import QDesktopServices

        from studio.whats_new import documentation_paths

        path = documentation_paths()["masterplan"]
        if not path.is_file():
            path = documentation_paths()["readme"]
        if not path.is_file():
            QMessageBox.warning(
                self,
                self._tr("action.open_docs"),
                self._tr("help.docs_missing", path=str(path)),
            )
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(path.resolve())))
        self._status("status.docs_opened")

    def _add_board(self):
        project = self.services.projects.current_project

        if project is None:
            self._load_empty_project()
            project = self.services.projects.current_project

        if project is None:
            return

        dialog = NewBoardDialog(
            self, units=self._display_units(), language=self._ui_language()
        )

        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        data = dialog.board_data()

        if any(board.board_id == data["board_id"] for board in project.boards):
            self._status("status.board_id_exists", id=data["board_id"])
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

        self._mark_project_modified()
        self.workspace.reload_project()
        self._reload_explorer()
        self.update_window_title()

        self._status("status.board_added")

    def _import_boards_from_csv(self) -> None:
        project = self.services.projects.current_project

        if project is None:
            self._load_empty_project()
            project = self.services.projects.current_project

        if project is None:
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self._tr("dialog.import_boards"),
            "",
            self._tr("dialog.filter_csv_excel"),
        )

        if not file_path:
            return

        existing_ids = {board.board_id.casefold() for board in project.boards}
        sheet = self._prompt_xlsx_sheet(file_path)
        if sheet is False:
            return
        loaded = load_tabular_file(file_path, sheet=sheet)
        if not loaded.ok:
            QMessageBox.warning(
                self,
                self._tr("dialog.import_boards_short"),
                "\n".join(loaded.errors),
            )
            return

        header_map = resolve_header_map(loaded.fieldnames, BOARD_HEADER_ALIASES)
        missing = missing_required_fields(header_map, BOARD_REQUIRED_FIELDS)
        if missing:
            mapped = self._prompt_column_mapping(
                fieldnames=loaded.fieldnames,
                field_order=BOARD_FIELD_ORDER,
                required_fields=BOARD_REQUIRED_FIELDS,
                initial_map=header_map,
                missing_fields=missing,
            )
            if mapped is None:
                return
            header_map = mapped

        result = import_boards_from_rows(
            loaded.fieldnames,
            loaded.rows,
            existing_ids=existing_ids,
            header_map=header_map,
        )

        if result.file_errors:
            QMessageBox.warning(
                self,
                self._tr("dialog.import_boards_short"),
                "\n".join(result.file_errors),
            )
            return

        dialog = ImportBoardsPreviewDialog(result, self, language=self._ui_language())

        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        boards = list(result.valid_boards)
        if not boards:
            self._status("status.boards_imported", 5000, n=0)
            return

        command = ImportBoardsCommand(self.services, boards)
        self.services.commands.execute(command)

        self._mark_project_modified(reason="boards_imported")
        self.workspace.reload_project()
        self._reload_explorer()
        self.update_window_title()
        self.update_undo_redo()
        self._emit(events.CSV_IMPORTED, kind="boards", count=len(boards))
        self._status("status.boards_imported", 5000, n=len(boards))

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
            self._tr("dialog.import_pieces"),
            "",
            self._tr("dialog.filter_csv_excel"),
        )

        if not file_path:
            return

        existing_ids = {piece.piece_id.casefold() for piece in project.pieces}
        sheet = self._prompt_xlsx_sheet(file_path)
        if sheet is False:
            return
        loaded = load_tabular_file(file_path, sheet=sheet)
        if not loaded.ok:
            QMessageBox.warning(
                self,
                self._tr("dialog.import_pieces_short"),
                "\n".join(loaded.errors),
            )
            return

        header_map = resolve_header_map(loaded.fieldnames, PIECE_HEADER_ALIASES)
        missing = missing_required_fields(header_map, PIECE_REQUIRED_FIELDS)
        if missing:
            mapped = self._prompt_column_mapping(
                fieldnames=loaded.fieldnames,
                field_order=PIECE_FIELD_ORDER,
                required_fields=PIECE_REQUIRED_FIELDS,
                initial_map=header_map,
                missing_fields=missing,
            )
            if mapped is None:
                return
            header_map = mapped

        result = import_pieces_from_rows(
            loaded.fieldnames,
            loaded.rows,
            existing_ids=existing_ids,
            header_map=header_map,
        )

        if result.file_errors:
            QMessageBox.warning(
                self,
                self._tr("dialog.import_pieces_short"),
                "\n".join(result.file_errors),
            )
            return

        dialog = ImportPiecesPreviewDialog(result, self, language=self._ui_language())

        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        pieces = list(result.valid_pieces)
        if not pieces:
            self._status("status.pieces_imported", 5000, n=0)
            return

        placements: list[StudioPlacement] = []
        for piece in pieces:
            x_mm, y_mm = self._find_free_piece_position(
                piece.length_mm,
                piece.width_mm,
            )
            placements.append(
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

        command = ImportPiecesCommand(self.services, pieces, placements)
        self.services.commands.execute(command)

        self._mark_project_modified(reason="pieces_imported")
        self.workspace.reload_project()
        self._reload_explorer()
        self.update_window_title()
        self.update_undo_redo()
        self._emit(events.CSV_IMPORTED, kind="pieces", count=len(pieces))
        self._status("status.pieces_imported", 5000, n=len(pieces))

    def _prompt_xlsx_sheet(self, file_path: str) -> str | None | bool:
        """Return sheet name, None for default/first, or False if cancelled."""
        suffix = Path(file_path).suffix.casefold()
        if suffix not in {".xlsx", ".xlsm"}:
            return None
        sheets = list_xlsx_sheets(file_path)
        if len(sheets) <= 1:
            return None
        names = [sheet.name for sheet in sheets]
        choice, ok = QInputDialog.getItem(
            self,
            self._tr("import.sheet_title"),
            self._tr("import.sheet_label"),
            names,
            0,
            False,
        )
        if not ok:
            return False
        return choice

    def _prompt_column_mapping(
        self,
        *,
        fieldnames: list[str] | tuple[str, ...],
        field_order: tuple[str, ...],
        required_fields: tuple[str, ...],
        initial_map: dict[str, str],
        missing_fields: list[str],
    ) -> dict[str, str] | None:
        """Ask the user to map file headers; return None if cancelled."""
        dialog = ImportColumnMappingDialog(
            fieldnames=fieldnames,
            field_order=field_order,
            required_fields=required_fields,
            initial_map=initial_map,
            missing_fields=missing_fields,
            language=self._ui_language(),
            parent=self,
        )
        if dialog.exec() != dialog.DialogCode.Accepted:
            return None
        mapped = dialog.header_map()
        still_missing = missing_required_fields(mapped, required_fields)
        if still_missing:
            QMessageBox.warning(
                self,
                self._tr("import.mapping_title"),
                self._tr(
                    "import.mapping_incomplete",
                    fields=", ".join(still_missing),
                ),
            )
            return None
        return mapped

    def _add_piece(self):
        project = self.services.projects.current_project

        if project is None:
            self._load_empty_project()
            project = self.services.projects.current_project

        if project is None:
            return

        dialog = NewPieceDialog(
            self, units=self._display_units(), language=self._ui_language()
        )

        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        data = dialog.piece_data()

        new_piece_id = data["piece_id"].strip()

        if not new_piece_id:
            self._status("status.piece_id_empty")
            return

        existing_ids = {piece.piece_id.strip().casefold() for piece in project.pieces}

        quantity = data.get("quantity", 1)
        piece_ids = self._generate_piece_ids(new_piece_id, quantity, existing_ids)

        if piece_ids is None:
            self._status("status.piece_id_exists", id=new_piece_id)
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

        self._mark_project_modified()
        self.workspace.reload_project()
        self._reload_explorer()
        self.update_window_title()

        if len(piece_ids) > 1:
            self._status("status.pieces_added", n=len(piece_ids))
        else:
            self._status("status.piece_added")

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

    def _panel_info_text(self, project, placement) -> str:
        """Return a human-readable label for a placement's physical panel."""
        if placement is None or placement.board_id is None:
            return self._tr("inspector.no_panel")

        board = next(
            (board for board in project.boards if board.board_id == placement.board_id),
            None,
        )
        quantity = board.quantity if board is not None else 1

        if quantity > 1:
            return self._tr(
                "inspector.panel_instance",
                board=placement.board_id,
                instance=placement.board_instance + 1,
                quantity=quantity,
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
                f"{self._tr('inspector.title')}\n\n"
                f"{self._tr('inspector.piece')}: {piece.piece_id}\n"
                f"{self._tr('inspector.dimensions')}: "
                f"{self._format_size(piece.length_mm, piece.width_mm)}\n"
                f"{self._tr('inspector.material')}: {piece.material}\n"
                f"{self._tr('inspector.unplaced')}"
            )
            return

        self.inspector.setText(
            f"{self._tr('inspector.title')}\n\n"
            f"{self._tr('inspector.piece')}: {piece.piece_id}\n"
            f"{self._tr('inspector.dimensions')}: "
            f"{self._format_size(piece.length_mm, piece.width_mm)}\n"
            f"{self._tr('inspector.position')}: "
            f"{self._format_length(placement.x_mm)}, "
            f"{self._format_length(placement.y_mm)}\n"
            f"{self._tr('inspector.board')}: "
            f"{self._panel_info_text(project, placement)}\n"
            f"{self._tr('inspector.material')}: {piece.material}"
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
            self._status("status.cannot_rotate")
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
        self._mark_project_modified()
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

        self._mark_project_modified(reason="piece_deleted")
        self._refresh_solutions_outdated_banner()
        self.update_window_title()
        self.update_undo_redo()

    def _open_preferences(self) -> None:
        dialog = PreferencesDialog(self.services.preferences.current, self)
        if dialog.exec() != PreferencesDialog.DialogCode.Accepted:
            return
        self.services.preferences.update(dialog.preferences())
        self._apply_preferences()
        self._status("status.prefs_saved")

    def _display_units(self) -> str:
        return self.services.preferences.current.units

    def _format_size(
        self,
        length_mm: float,
        width_mm: float,
        *,
        thickness_mm: float | None = None,
    ) -> str:
        return format_size(
            length_mm,
            width_mm,
            self._display_units(),
            thickness_mm=thickness_mm,
        )

    def _format_length(self, value_mm: float) -> str:
        return format_length(value_mm, self._display_units())

    def _ui_language(self) -> str:
        return self.services.preferences.current.language

    def _tr(self, key: str, **kwargs: object) -> str:
        return tr(key, self._ui_language(), **kwargs)

    def _emit(self, event_name: str, **payload: object) -> None:
        self.services.events.publish(event_name, dict(payload))

    def _mark_project_modified(self, **payload: object) -> None:
        marked = self.services.mark_project_modified(**payload)
        self._refresh_solutions_outdated_banner()
        if marked:
            self._status("status.solutions_outdated", 5000)

    def _refresh_solutions_outdated_banner(self) -> None:
        outdated = self.services.layout.solutions_outdated
        banner = self.solutions_outdated_banner
        if outdated:
            banner.setText(self._tr("comparator.solutions_outdated"))
            banner.show()
        else:
            banner.hide()
            banner.clear()

    def _status(self, key: str, timeout: int = 3000, **kwargs: object) -> None:
        self.statusBar().showMessage(self._tr(key, **kwargs), timeout)

    def clear_inspector(self) -> None:
        """Show the empty Inspector state in the active language."""
        self.inspector.setText(
            f"{self._tr('inspector.title')}\n\n{self._tr('inspector.none')}"
        )

    def _retranslate_ui(self) -> None:
        """Refresh menus, docks, comparator chrome and explorer labels."""
        for key, menu in self._menus.items():
            menu.setTitle(self._tr(f"menu.{key}"))
        for key, action in self._actions.items():
            action.setText(self._tr(f"action.{key}"))
        self._recent_menu.setTitle(self._tr("menu.recent"))

        self.explorer_dock.setWindowTitle(self._tr("dock.explorer"))
        self.inspector_dock.setWindowTitle(self._tr("dock.inspector"))
        self.console_dock.setWindowTitle(self._tr("dock.timeline"))
        self.solutions_dock.setWindowTitle(self._tr("dock.comparator"))
        self.console.retranslate(self._ui_language())

        self.solutions_table.setHorizontalHeaderLabels(
            [
                "#",
                self._tr("comparator.pieces"),
                self._tr("comparator.waste"),
                self._tr("comparator.board_free"),
                self._tr("comparator.length"),
                self._tr("comparator.width"),
                self._tr("comparator.score"),
            ]
        )

        current_sort = self.comparator_sort.currentData() or self._comparator_sort_by
        self.comparator_sort.blockSignals(True)
        self.comparator_sort.clear()
        for key, _label in SORT_LABELS:
            self.comparator_sort.addItem(self._tr(f"sort.{key}"), key)
        index = self.comparator_sort.findData(current_sort)
        self.comparator_sort.setCurrentIndex(index if index >= 0 else 0)
        self.comparator_sort.blockSignals(False)

        self.comparator_sort_label.setText(self._tr("comparator.sort_by"))
        self.comparator_complete_only.setText(self._tr("comparator.complete_only"))
        self.pin_reference_button.setText(self._tr("comparator.pin_reference"))
        self.comparator_diff_label.setText(self._tr("comparator.diff_title"))
        self._refresh_solutions_outdated_banner()
        self.solution_differences.setPlaceholderText(
            self._tr("comparator.diff_placeholder")
        )

        self._reload_recent_files_menu()

    def _apply_preferences(self) -> None:
        from PySide6.QtWidgets import QApplication

        from studio.theme import apply_theme

        app = QApplication.instance()
        if app is not None:
            apply_theme(app, self.services.preferences.current.theme)
        self._retranslate_ui()
        self.welcome.apply_language(self.services.preferences.current.language)
        self.workspace.reload_project()
        self._reload_explorer()
        self.welcome.set_recent_files(self.services.recent_files.existing_files())
        if self.services.layout.selected_solution is not None:
            self._show_layout_solution(self.services.layout.selected_solution)
        else:
            self.workspace.selection.sync_inspector(self)
        self._reload_solution_table()

    def _solve_layout(self):
        from studio.solve_worker import run_solve_with_progress

        self._status("status.layout_computing", 0)
        self._emit(
            events.SOLUTION_GENERATION_STARTED,
            strategy=self.services.layout.strategy_name
            or self.services.preferences.current.strategy_name,
        )
        try:
            solution = run_solve_with_progress(
                parent=self,
                layout_service=self.services.layout,
                label=self._tr("progress.layout_label"),
                title=self._tr("progress.layout_title"),
                cancel_text=self._tr("progress.layout_cancel"),
            )
        except RuntimeError as exc:
            self._publish_solve_trace()
            self._emit(events.SOLUTION_GENERATED, status="error", detail=str(exc))
            self._status("status.layout_error", error=str(exc))
            return

        self._comparator_reference_index = None
        self._publish_solve_trace()

        if self.services.layout.stats.cancelled:
            self._reload_solution_table()
            self.inspector.setText(self._tr("inspector.layout_cancelled"))
            self._emit(events.SOLUTION_GENERATED, status="cancelled")
            self._refresh_solutions_outdated_banner()
            self._status("status.layout_cancelled")
            return

        if solution is None:
            self._show_no_solution_diagnosis()
            self._emit(events.SOLUTION_GENERATED, status="none", count=0)
            self._refresh_solutions_outdated_banner()
            self._status("status.layout_failed")
            return

        self._reload_solution_table()
        self._show_layout_solution(solution)
        self._reload_explorer()
        self._refresh_solutions_outdated_banner()

        solution_count = len(self.services.layout.solutions)
        self._emit(
            events.SOLUTION_GENERATED,
            status="ok" if solution.is_complete else "partial",
            count=solution_count,
        )

        if not solution.is_complete:
            self._status(
                "status.layout_partial",
                5000,
                omitted=len(solution.omitted_piece_ids),
                total=solution_count,
            )
            return

        self._status("status.layout_ok", n=solution_count)

    def _publish_solve_trace(self) -> None:
        from studio.solve_trace_publisher import publish_solve_trace

        publish_solve_trace(self.services.events, self.services.layout.trace)
        self.console.set_phase_trace(self.services.layout.trace)

    def _show_no_solution_diagnosis(self) -> None:
        lines = [self._tr("inspector.no_solution"), ""]
        lines.extend(self.services.layout.stats_summary_lines(self._ui_language()))
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
        if not solutions:
            self.console.set_replay_solution(None)
            self.console.set_phase_trace(None)
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
                placed_label += self._tr(
                    "comparator.unplaced_suffix",
                    n=len(solution.omitted_piece_ids),
                )

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
            highlight_text = self._tr(
                "comparator.best_in",
                items=", ".join(self._tr(key) for key in row_highlights),
            )

            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                if row_highlights:
                    item.setToolTip(highlight_text)
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
                thumb.setToolTip(highlight_text)
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
            self._status("status.select_solution_first")
            return
        self._comparator_reference_index = selected
        self._reload_solution_differences()
        self._status("status.reference_pinned", n=selected + 1)

    def _reload_solution_differences(self) -> None:
        solutions = self.services.layout.solutions
        language = self._ui_language()
        if len(solutions) < 2:
            self.solution_differences.setPlainText(
                "\n".join(format_diff_unavailable("diff.need_two", language))
            )
            return

        candidate_index = self.services.layout.selected_solution_index
        if candidate_index < 0 or candidate_index >= len(solutions):
            self.solution_differences.setPlainText(
                "\n".join(format_diff_unavailable("diff.select_solution", language))
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
            language=language,
        )
        self.solution_differences.setPlainText("\n".join(diff.summary_lines()))

    def _show_layout_solution(self, solution):
        solution_count = len(self.services.layout.solutions)
        selected_index = self.services.layout.selected_solution_index + 1
        strategy_name = self.services.layout.strategy_name or self._tr(
            "inspector.strategy_unknown"
        )

        lines = [
            self._tr("inspector.layout_title"),
            "",
            self._tr(
                "inspector.solution",
                current=selected_index,
                total=solution_count,
            ),
            self._tr("inspector.strategy", name=strategy_name),
            self._tr("inspector.placed", n=len(solution.placements)),
            self._tr(
                "inspector.total_length",
                value=f"{solution.total_length_mm:.0f}",
            ),
            self._tr(
                "inspector.total_width",
                value=f"{solution.total_width_mm:.0f}",
            ),
            self._tr(
                "inspector.internal_waste",
                value=f"{solution.waste_ratio:.1%}",
            ),
            self._tr(
                "inspector.free_material",
                value=f"{self.services.layout.board_waste_ratio(solution):.1%}",
            ),
        ]

        if not solution.is_complete:
            lines.append(
                self._tr(
                    "inspector.omitted",
                    ids=", ".join(solution.omitted_piece_ids),
                )
            )

        if solution.offcuts:
            lines.append(
                self._tr(
                    "inspector.offcuts",
                    n=len(solution.offcuts),
                    area=f"{solution.total_offcut_area_mm2:.0f}",
                )
            )

        if self.services.layout.solutions_outdated:
            lines.append("")
            lines.append(self._tr("inspector.solutions_outdated"))

        highlights = self.services.layout.solution_highlights.get(
            self.services.layout.selected_solution_index
        )
        if highlights:
            lines.append(
                self._tr(
                    "inspector.highlights",
                    items=", ".join(self._tr(key) for key in highlights),
                )
            )

        if solution.explanation.strengths or solution.explanation.weaknesses:
            lines.append("")
            lines.extend(f"+ {strength}" for strength in solution.explanation.strengths)
            lines.extend(
                f"- {weakness}" for weakness in solution.explanation.weaknesses
            )

        stats_lines = self.services.layout.stats_summary_lines(self._ui_language())

        if stats_lines:
            lines.extend(["", *stats_lines])

        self.inspector.setText("\n".join(lines))
        self.console.set_replay_solution(solution)

    def _on_timeline_replay_step(self, solution, reveal_count: int) -> None:
        if solution is None:
            return
        self.workspace.preview_solution(solution, reveal_count=reveal_count)
        total = len(solution.placements)
        if reveal_count <= 0:
            self._reload_solution_differences_at_step(0)
        elif reveal_count >= total:
            self._reload_solution_differences()
            if total > 0:
                last_id = solution.placements[total - 1].board_id
                self.workspace.select_piece(last_id)
        else:
            self._reload_solution_differences_at_step(reveal_count)
            last_id = solution.placements[reveal_count - 1].board_id
            self.workspace.select_piece(last_id)

        self._status(
            "status.timeline_replay",
            2000,
            current=reveal_count,
            total=total,
        )

    def _on_timeline_phase_step(self, event, step: int) -> None:
        """React to algorithm-phase replay without mutating the project."""
        total = self.console.phase_replay_total
        if event is None:
            self._status(
                "status.timeline_phase",
                2000,
                current=step,
                total=total,
                detail=self._tr("timeline.phase_idle_detail"),
            )
            return

        self._apply_timeline_context(event.payload)
        detail = tr(
            f"timeline.phase.{event.kind}",
            self._ui_language(),
        )
        algorithm = event.payload.get("algorithm")
        piece = event.payload.get("piece")
        if isinstance(algorithm, str) and algorithm:
            detail = f"{detail} · {algorithm}"
        if isinstance(piece, str) and piece:
            detail = f"{detail} · {piece}"
        duration = event.payload.get("duration_ms")
        if isinstance(duration, int):
            detail = f"{detail} · {duration} ms"

        self._status(
            "status.timeline_phase",
            2500,
            current=step,
            total=total,
            detail=detail,
        )

    def _on_timeline_entry_selected(self, entry) -> None:
        """Seek Workspace/Comparator context from a clicked Timeline fact."""
        self._apply_timeline_context(entry.payload)
        if entry.event_name == events.SOLUTION_SELECTED:
            index = entry.payload.get("index")
            if isinstance(index, int) and index >= 1:
                self._select_layout_solution(index - 1)

        label = tr(
            f"timeline.event.{entry.event_name}",
            self._ui_language(),
        )
        detail_parts: list[str] = [label]
        note = entry.payload.get("note")
        if isinstance(note, str) and note:
            detail_parts.append(note)
        algorithm = entry.payload.get("algorithm")
        if isinstance(algorithm, str) and algorithm:
            detail_parts.append(algorithm)
        piece = entry.payload.get("piece")
        if isinstance(piece, str) and piece:
            detail_parts.append(piece)
        self._status(
            "status.timeline_seek",
            3000,
            detail=" · ".join(detail_parts),
        )

    def _apply_timeline_context(self, payload: dict) -> None:
        """Select solution/piece hinted by a Timeline or SolveTrace payload."""
        algorithm = payload.get("algorithm")
        if isinstance(algorithm, str) and algorithm:
            self._select_solution_for_algorithm(algorithm)

        piece = payload.get("piece")
        if isinstance(piece, str) and piece:
            self.workspace.select_piece(piece)

    def _select_solution_for_algorithm(self, algorithm: str) -> None:
        """Select the first cached solution produced by ``algorithm``."""
        for index, solution in enumerate(self.services.layout.solutions):
            notes = solution.explanation.notes
            if notes and notes[0] == algorithm:
                if index != self.services.layout.selected_solution_index:
                    self._select_layout_solution(index)
                return

    def _reload_solution_differences_at_step(self, step: int) -> None:
        """Update the diff panel for Timeline-synced placement replay."""
        solutions = self.services.layout.solutions
        language = self._ui_language()
        if len(solutions) < 1:
            return

        candidate_index = self.services.layout.selected_solution_index
        if candidate_index < 0 or candidate_index >= len(solutions):
            return

        reference_index = self._comparator_reference_index
        if reference_index is None or reference_index >= len(solutions):
            reference_index = 0 if candidate_index != 0 else min(1, len(solutions) - 1)
            if reference_index >= len(solutions):
                reference_index = candidate_index
            self._comparator_reference_index = reference_index

        lines = compare_solutions_at_step(
            solutions[reference_index],
            solutions[candidate_index],
            step,
            reference_index=reference_index,
            candidate_index=candidate_index,
            language=language,
        )
        self.solution_differences.setPlainText("\n".join(lines))
        self.solutions_dock.raise_()

    def _apply_layout(self):
        if self.services.layout.solutions_outdated:
            answer = QMessageBox.question(
                self,
                self._tr("dialog.outdated_solutions_title"),
                self._tr("dialog.outdated_solutions_apply"),
            )
            if answer != QMessageBox.StandardButton.Yes:
                return

        if not self.services.layout.apply_last_solution_to_current_project():
            self._status("status.calculate_layout_first")
            return

        self.workspace.reload_project()
        self.services.selection.clear()
        self._reload_explorer()
        self.update_undo_redo()
        self.update_window_title()

        selected_index = self.services.layout.selected_solution_index + 1
        solution_count = len(self.services.layout.solutions)

        self._status(
            "status.solution_applied",
            current=selected_index,
            total=solution_count,
        )
        self._emit(
            events.WORKSPACE_UPDATED,
            reason="apply_layout",
            index=selected_index,
        )

    def _previous_layout_solution(self):
        solution = self.services.layout.select_previous_solution()

        if solution is None:
            self._status("status.no_solutions")
            return

        self.workspace.preview_solution(solution)
        self._reload_solution_table()
        self._show_layout_solution(solution)
        self._reload_explorer()
        self._reload_solution_table()

        index = self.services.layout.selected_solution_index + 1
        total = len(self.services.layout.solutions)

        self._status(
            "status.previewing_solution",
            5000,
            current=index,
            total=total,
        )
        self._emit(events.SOLUTION_SELECTED, index=index, total=total)

    def _next_layout_solution(self):
        solution = self.services.layout.select_next_solution()

        if solution is None:
            self._status("status.no_solutions")
            return

        self.workspace.preview_solution(solution)
        self._show_layout_solution(solution)
        self._reload_explorer()

        index = self.services.layout.selected_solution_index + 1
        total = len(self.services.layout.solutions)

        self._status(
            "status.previewing_solution",
            5000,
            current=index,
            total=total,
        )
        self._emit(events.SOLUTION_SELECTED, index=index, total=total)

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

    def _export_timeline_history(self) -> None:
        from studio.timeline.export import timeline_to_csv, timeline_to_json

        store = self.services.timeline
        event_filter = self.console.current_filter_event()
        algo_filter = self.console.current_filter_algorithm()
        since_filter = self.console.current_filter_since()
        period_seconds = self.console.current_filter_period_seconds()
        entries = store.filtered(
            event_filter,
            algorithm=algo_filter,
            since=since_filter,
        )
        if not entries:
            self._status("status.timeline_export_empty")
            return

        path, selected_filter = QFileDialog.getSaveFileName(
            self,
            self._tr("dialog.export_timeline"),
            "boardcomposer-timeline.json",
            self._tr("dialog.filter_timeline"),
        )
        if not path:
            return

        use_csv = path.lower().endswith(".csv") or "CSV" in (selected_filter or "")
        if use_csv and not path.lower().endswith(".csv"):
            path = f"{path}.csv"
        elif not use_csv and not path.lower().endswith(".json"):
            path = f"{path}.json"

        try:
            if use_csv:
                payload = timeline_to_csv(
                    store,
                    event_name=event_filter,
                    algorithm=algo_filter,
                    since=since_filter,
                )
            else:
                payload = timeline_to_json(
                    store,
                    event_name=event_filter,
                    algorithm=algo_filter,
                    since=since_filter,
                    period_seconds=period_seconds,
                )
            Path(path).write_text(payload, encoding="utf-8")
        except OSError as exc:
            self._status("status.timeline_export_failed", 5000, error=exc)
            return

        self._status("status.timeline_exported", 5000, path=path)

    def _export_selected_solution(self):
        solution = self.services.layout.selected_solution

        if solution is None:
            self._status("status.calculate_layout_first")
            return

        prefs = self.services.preferences.current
        dialog = ExportDialog(
            solution,
            self.services.layout.solved_project,
            prefs.export_options(),
            templates=self.services.export_templates,
            strategy_name=self.services.layout.strategy_name,
            solution_index=self.services.layout.selected_solution_index,
            language=self._ui_language(),
            parent=self,
        )
        if dialog.exec() != ExportDialog.DialogCode.Accepted:
            return

        options = dialog.options()
        selected_index = self.services.layout.selected_solution_index + 1
        default_filename = (
            f"boardcomposer-solution-{selected_index}.{options.extension}"
        )

        path, _selected_filter = QFileDialog.getSaveFileName(
            self,
            self._tr("dialog.export_selected"),
            default_filename,
            options.file_filter,
        )
        if not path:
            return

        try:
            payload = render_export(
                solution,
                self.services.layout.solved_project,
                options,
                strategy_name=self.services.layout.strategy_name,
                solution_index=self.services.layout.selected_solution_index,
            )
            if isinstance(payload, bytes):
                Path(path).write_bytes(payload)
            else:
                Path(path).write_text(payload, encoding="utf-8")
        except OSError as exc:
            self._status(
                "status.export_failed",
                5000,
                format=options.label,
                error=exc,
            )
            return

        updated = dataclass_replace(
            prefs,
            export_format=options.format,
            export_include_metrics=options.include_metrics,
            export_include_explanation=options.include_explanation,
            export_include_offcuts=options.include_offcuts,
        )
        self.services.preferences.update(updated)

        self._emit(
            events.EXPORT_COMPLETED,
            format=options.label,
            path=path,
        )
        self._status("status.exported", 5000, format=options.label, path=path)

    def _save_project(self):
        project = self.services.projects.current_project

        if project is None:
            self._status("status.nothing_to_save")
            return

        filename = self.services.projects.filename

        if filename is None:
            self._save_project_as()
            return

        try:
            save_project(project, filename)
        except OSError as exc:
            self._status("status.save_failed", 5000, error=exc)
            return

        self.services.projects.mark_saved(filename)
        self._reload_recent_files_menu()
        self.services.recent_files.add(filename)
        self.update_window_title()
        self._emit(events.PROJECT_SAVED, path=str(filename))
        self._status("status.project_saved", 5000, path=filename)

    def _save_project_as(self):
        project = self.services.projects.current_project

        if project is None:
            self._status("status.nothing_to_save")
            return

        path, _selected_filter = QFileDialog.getSaveFileName(
            self,
            self._tr("dialog.save_project"),
            "boardcomposer-project.bcproj",
            self._tr("dialog.filter_bcproj"),
        )

        if not path:
            return

        try:
            save_project(project, path)
        except OSError as exc:
            self._status("status.save_failed", 5000, error=exc)
            return

        self.services.projects.mark_saved(path)
        self._reload_recent_files_menu()
        self.services.recent_files.add(path)
        self.update_window_title()
        self._emit(events.PROJECT_SAVED, path=str(path))
        self._status("status.project_saved", 5000, path=path)

    def _open_project(self):
        if not self._confirm_discard_unsaved_changes():
            return

        path, _selected_filter = QFileDialog.getOpenFileName(
            self,
            self._tr("dialog.open_project"),
            "",
            self._tr("dialog.filter_bcproj"),
        )

        if not path:
            return

        try:
            project = load_project(path)
        except UnsupportedProjectVersionError as error:
            QMessageBox.warning(self, self._tr("dialog.open_project"), str(error))
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

        self._emit(events.PROJECT_OPENED, path=str(path))
        self._status("status.project_opened", path=path)

    def _reload_recent_files_menu(self):
        self._recent_menu.clear()
        if hasattr(self, "welcome"):
            self.welcome.set_recent_files(self.services.recent_files.existing_files())

        if not self.services.recent_files.files:
            empty_action = QAction(self._tr("action.no_recent"), self)
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
            QMessageBox.warning(self, self._tr("dialog.open_project"), str(error))
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

        self._emit(events.PROJECT_OPENED, path=str(path))
        self._status("status.project_opened", path=path)

    def _confirm_discard_unsaved_changes(self) -> bool:
        if not self.services.projects.is_modified:
            return True

        result = QMessageBox.question(
            self,
            self._tr("dialog.unsaved_title"),
            self._tr("dialog.unsaved_body"),
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

        self._status(
            "status.previewing_solution",
            5000,
            current=selected_index,
            total=total,
        )
        self._emit(events.SOLUTION_SELECTED, index=selected_index, total=total)

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
            title=self._tr("dialog.edit_board"),
            units=self._display_units(),
            language=self._ui_language(),
        )

        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        data = dialog.board_data()
        new_board_id = data["board_id"]

        if new_board_id != board_id and any(
            existing.board_id == new_board_id for existing in project.boards
        ):
            self._status("status.board_id_exists", id=new_board_id)
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

        self._mark_project_modified(reason="board_edited")

        self.workspace.reload_project()
        self._reload_explorer()
        self._reload_solution_table()
        self.update_window_title()

        if not self.services.layout.solutions_outdated:
            self._status("status.board_updated")

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
            title=self._tr("dialog.edit_piece"),
            show_quantity=False,
            units=self._display_units(),
            language=self._ui_language(),
        )

        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        data = dialog.piece_data()
        new_piece_id = data["piece_id"].strip()

        if not new_piece_id:
            self._status("status.piece_id_empty")
            return

        normalized_id = new_piece_id.casefold()

        if any(
            existing.piece_id != piece_id
            and existing.piece_id.strip().casefold() == normalized_id
            for existing in project.pieces
        ):
            self._status("status.piece_id_exists", id=new_piece_id)
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

        self._mark_project_modified(reason="piece_edited")

        self.workspace.reload_project()
        self._reload_explorer()
        self._reload_solution_table()

        self.services.selection.select_one(new_piece_id)
        self.workspace.select_piece(new_piece_id)

        position_text = ""
        panel_text = ""
        if placement is not None:
            position_text = (
                f"{self._tr('inspector.position')}: "
                f"{self._format_length(placement.x_mm)}, "
                f"{self._format_length(placement.y_mm)}\n"
            )
            panel_text = (
                f"{self._tr('inspector.board')}: "
                f"{self._panel_info_text(project, placement)}\n"
            )

        self.inspector.setText(
            f"{self._tr('inspector.title')}\n\n"
            f"{self._tr('inspector.piece')}: {updated_piece.piece_id}\n"
            f"{self._tr('inspector.dimensions')}: "
            f"{self._format_size(updated_piece.length_mm, updated_piece.width_mm)}\n"
            f"{position_text}"
            f"{panel_text}"
            f"{self._tr('inspector.material')}: {updated_piece.material}"
        )

        self.update_window_title()
        if not self.services.layout.solutions_outdated:
            self._status("status.piece_updated")
