"""Main window for BoardComposer Studio."""

from pathlib import Path

from PySide6.QtCore import QByteArray, QPoint, QSize, Qt, QTimer
from PySide6.QtGui import QAction, QBrush, QCloseEvent, QColor, QIcon
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
    QMenu,
    QMenuBar,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QToolBar,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)
from shiboken6 import isValid as _qt_is_valid

from boardcomposer.export import solution_to_svg
from studio.export_options import render_export
from dataclasses import replace as dataclass_replace
from studio.board_ids import allocate_unique_board_id
from studio.branding import app_icon
from studio.commands import (
    AddBoardCommand,
    AddPieceCommand,
    DeleteBoardCommand,
    DeletePieceCommand,
    DuplicateBoardCommand,
    DuplicatePieceCommand,
    EditBoardCommand,
    EditPieceCommand,
    ImportBoardsCommand,
    ImportPiecesCommand,
    PlacePieceCommand,
    RenameProjectCommand,
    RotatePieceCommand,
)
from studio.panel_compatibility import incompatibility_reason
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.project_serializer import (
    UnsupportedProjectVersionError,
    load_project,
    project_to_dict,
    save_project,
)
from studio.i18n import action_keys, menu_keys, tr
from studio.workspace.board_workspace import BoardWorkspace
from studio.dialogs import (
    AboutDialog,
    BcprojDiffDialog,
    ExportDialog,
    ImportBoardsPreviewDialog,
    ImportPiecesPreviewDialog,
    NewBoardDialog,
    NewPieceDialog,
    NewProjectDialog,
    PreferencesDialog,
    ProjectTemplatePickerDialog,
    ShortcutsDialog,
    WhatsNewDialog,
)
from studio.keyboard_shortcuts import apply_shortcuts, with_native_shortcuts
from studio.project_ids import new_project_id
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
    sanitize_header_map,
)
from studio.tabular_file import list_xlsx_sheets, load_tabular_file
from studio.piece_ids import allocate_unique_piece_id
from studio.explorer_actions import explorer_context_actions, parse_explorer_role
from studio.dialogs.import_column_mapping_dialog import ImportColumnMappingDialog
from studio.solution_diff import (
    compare_solutions,
    compare_solutions_at_step,
    format_diff_unavailable,
)
from studio.solution_thumbnail import svg_to_raster_bytes
from studio.solution_ordering import (
    SORT_LABELS,
    ordered_solution_indexes,
    step_display_index,
)
from studio.solution_thumbnail import DEFAULT_THUMBNAIL_SIZE, solution_thumbnails
from studio.units import format_length, format_size
from studio.welcome_screen import WelcomeScreen
from studio.timeline import TimelinePanel
from studio.events import catalog as events


def _qbytearray_to_bytes(value: QByteArray) -> bytes:
    """Convert ``QByteArray`` to ``bytes`` for storage / typing stubs."""
    return bytes(value.data())


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
        self._comparator_reference_pinned = False
        self.setWindowTitle("BoardComposer Studio")
        icon = app_icon()
        if not icon.isNull():
            self.setWindowIcon(icon)
        self.resize(1400, 900)

        self._build_menu()
        self._build_toolbar()
        self._build_workspace()
        self._build_panels()
        self._build_statusbar()
        self._factory_window_geometry = _qbytearray_to_bytes(self.saveGeometry())
        self._factory_window_state = _qbytearray_to_bytes(self.saveState())
        self._restore_window_layout()
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

        apply_shortcuts(self._actions)

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
        self._menus["edit"].addAction(self._actions["rename_selection"])
        self._menus["edit"].addAction(self._actions["edit_selection"])
        self._menus["edit"].addAction(self._actions["copy_selection_id"])
        self._menus["edit"].addAction(self._actions["duplicate_piece"])
        self._menus["edit"].addAction(self._actions["delete_piece"])
        self._menus["edit"].addSeparator()
        self._menus["edit"].addAction(self._actions["select_all_pieces"])
        self._menus["edit"].addAction(self._actions["deselect_pieces"])
        self._menus["edit"].addAction(self._actions["invert_selection"])
        self._menus["edit"].addSeparator()
        self._menus["edit"].addAction(self._actions["preferences"])

        self._actions["toggle_grid"].setCheckable(True)
        self._menus["view"].addAction(self._actions["fit_board"])
        self._menus["view"].addAction(self._actions["fit_selection"])
        self._menus["view"].addAction(self._actions["zoom_in"])
        self._menus["view"].addAction(self._actions["zoom_out"])
        self._menus["view"].addSeparator()
        self._menus["view"].addAction(self._actions["toggle_grid"])

        self._menus["project"].addAction(self._actions["rename_project"])
        self._menus["project"].addAction(self._actions["reveal_project_folder"])
        self._menus["project"].addAction(self._actions["diff_bcproj"])
        self._menus["project"].addSeparator()
        self._menus["project"].addAction(self._actions["add_board"])
        self._menus["project"].addAction(self._actions["add_piece"])
        self._menus["project"].addAction(self._actions["import_boards_csv"])
        self._menus["project"].addAction(self._actions["import_pieces_csv"])

        self._menus["generate"].addAction(self._actions["solve_layout"])

        self._menus["compare"].addAction(self._actions["previous_solution"])
        self._menus["compare"].addAction(self._actions["next_solution"])
        self._menus["compare"].addSeparator()
        self._menus["compare"].addAction(self._actions["apply_layout"])

        self._menus["export"].addAction(self._actions["export_selected"])
        self._menus["export"].addAction(self._actions["export_timeline"])

        self._menus["help"].addAction(self._actions["whats_new"])
        self._menus["help"].addAction(self._actions["shortcuts"])
        self._menus["help"].addAction(self._actions["open_docs"])
        self._menus["help"].addSeparator()
        self._menus["help"].addAction(self._actions["about"])

        self._actions["open"].triggered.connect(self._open_project)
        self._actions["save"].triggered.connect(self._save_project)
        self._actions["save_as"].triggered.connect(self._save_project_as)
        self._actions["exit"].triggered.connect(self.close)
        self._actions["clear_recent"].triggered.connect(self._clear_recent_files)
        self._actions["new_project"].triggered.connect(self._new_project)
        self._actions["new_from_template"].triggered.connect(self._new_from_template)
        self._actions["new_demo_project"].triggered.connect(self._new_demo_project)
        self._actions["show_welcome"].triggered.connect(self._show_welcome_screen)
        self._actions["save_as_template"].triggered.connect(self._save_as_template)
        self._actions["rename_project"].triggered.connect(self._rename_project)
        self._actions["reveal_project_folder"].triggered.connect(
            self._reveal_project_folder
        )
        self._actions["diff_bcproj"].triggered.connect(self._diff_bcproj)
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
        self._actions["rename_selection"].triggered.connect(self._rename_selection)
        self._actions["edit_selection"].triggered.connect(self._edit_selection)
        self._actions["copy_selection_id"].triggered.connect(self._copy_selection_id)
        self._actions["duplicate_piece"].triggered.connect(
            self._duplicate_selected_piece
        )
        self._actions["delete_piece"].triggered.connect(self._delete_selected_piece)
        self._actions["select_all_pieces"].triggered.connect(self._select_all_pieces)
        self._actions["deselect_pieces"].triggered.connect(self._deselect_pieces)
        self._actions["invert_selection"].triggered.connect(self._invert_selection)
        self._actions["preferences"].triggered.connect(self._open_preferences)
        self._actions["fit_board"].triggered.connect(self._fit_board)
        self._actions["fit_selection"].triggered.connect(self._fit_selection)
        self._actions["zoom_in"].triggered.connect(self._zoom_in)
        self._actions["zoom_out"].triggered.connect(self._zoom_out)
        self._actions["toggle_grid"].toggled.connect(self._toggle_grid)
        self._actions["reset_window_layout"].triggered.connect(
            self._reset_window_layout
        )
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
        self._actions["shortcuts"].triggered.connect(self._show_shortcuts)
        self._actions["open_docs"].triggered.connect(self._open_documentation)
        self._actions["about"].triggered.connect(self._show_about)

        self._reload_recent_files_menu()

    def _build_toolbar(self) -> None:
        """Primary toolbar reusing existing menu actions (SCR-002)."""
        toolbar = QToolBar(self._tr("toolbar.main"), self)
        toolbar.setObjectName("mainToolbar")
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)

        for key in ("new_project", "open", "save"):
            toolbar.addAction(self._actions[key])
        toolbar.addSeparator()
        for key in ("undo", "redo"):
            toolbar.addAction(self._actions[key])
        toolbar.addSeparator()
        for key in ("fit_board", "fit_selection", "zoom_in", "zoom_out", "toggle_grid"):
            toolbar.addAction(self._actions[key])
        toolbar.addSeparator()
        toolbar.addAction(self._actions["solve_layout"])
        toolbar.addSeparator()
        for key in ("previous_solution", "next_solution", "apply_layout"):
            toolbar.addAction(self._actions[key])
        toolbar.addSeparator()
        toolbar.addAction(self._actions["export_selected"])

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)
        self._toolbar = toolbar

        self._menus["view"].addSeparator()
        self._toolbar_toggle = toolbar.toggleViewAction()
        self._toolbar_toggle.setText(self._tr("action.toggle_toolbar"))
        tip = self._tr("tip.toggle_toolbar")
        if tip != "tip.toggle_toolbar":
            self._toolbar_toggle.setStatusTip(tip)
        self._actions["toggle_toolbar"] = self._toolbar_toggle
        apply_shortcuts(self._actions)
        self._menus["view"].addAction(self._toolbar_toggle)

    def _build_workspace(self):
        self.workspace = BoardWorkspace(self.services)
        self.workspace.add_board_requested.connect(self._add_board)
        self.workspace.add_piece_requested.connect(self._add_piece)
        self.workspace.import_boards_requested.connect(self._import_boards_from_csv)
        self.workspace.import_pieces_requested.connect(self._import_pieces_from_csv)
        self.workspace.rotate_requested.connect(self._rotate_selected_piece)
        self.workspace.selection_or_focus_changed.connect(self._sync_view_actions)
        self.workspace.selection_or_focus_changed.connect(
            self._sync_edit_selection_actions
        )
        # Ensure Edit→Rotar / R is available while the canvas has focus.
        self.workspace.addAction(self._actions["rotate_piece"])
        self.welcome = WelcomeScreen()
        self.welcome.new_project_requested.connect(self._new_project)
        self.welcome.open_project_requested.connect(self._open_project)
        self.welcome.open_recent_requested.connect(self._open_recent_project)
        self.welcome.clear_recent_requested.connect(self._clear_recent_files)
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
        if self._central_stack.currentWidget() is self.welcome:
            self._status("status.already_on_welcome")
            self._sync_welcome_action()
            return
        self.welcome.set_recent_files(self.services.recent_files.existing_files())
        self._sync_template_actions()
        self._central_stack.setCurrentWidget(self.welcome)
        self._sync_welcome_action()
        self._status("status.welcome", 2000)

    def _show_workspace(self) -> None:
        self._central_stack.setCurrentWidget(self.workspace)
        self._sync_welcome_action()
        self._emit(events.WORKSPACE_OPENED)

    def _sync_welcome_action(self) -> None:
        """Disable «Pantalla de inicio» while already on Welcome."""
        action = self._actions.get("show_welcome")
        if action is None or not hasattr(self, "welcome"):
            return
        on_welcome = self._central_stack.currentWidget() is self.welcome
        action.setEnabled(not on_welcome)
        action.setStatusTip(
            self._tr("status.already_on_welcome")
            if on_welcome
            else with_native_shortcuts(self._tr("tip.show_welcome"))
        )

    def _build_panels(self):
        self.explorer = QTreeWidget()
        self.explorer.setHeaderHidden(True)
        # Keep items stable: expand-on-double-click fights leaf activation.
        self.explorer.setExpandsOnDoubleClick(False)
        self.explorer.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.explorer.itemSelectionChanged.connect(self._on_explorer_selection_changed)
        self.explorer.itemSelectionChanged.connect(self._sync_edit_selection_actions)
        # Prefer activated (double-click or Enter) over double-clicked alone.
        self.explorer.itemActivated.connect(self._on_explorer_item_activated)
        self.explorer.customContextMenuRequested.connect(self._on_explorer_context_menu)

        self.explorer_dock = QDockWidget("", self)
        self.explorer_dock.setObjectName("explorerDock")
        self.explorer_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.explorer_dock.setWidget(self.explorer)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.explorer_dock)

        self.inspector = QTextEdit()
        self.inspector.setObjectName("inspectorPanel")
        self.inspector.setReadOnly(True)

        self.inspector_dock = QDockWidget("", self)
        self.inspector_dock.setObjectName("inspectorDock")
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
        self.console.filters_changed.connect(self._sync_timeline_actions)
        self.services.timeline.add_changed_listener(self._sync_timeline_actions)
        self._sync_timeline_actions()

        self.console_dock = QDockWidget("", self)
        self.console_dock.setObjectName("timelineDock")
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
        self.solutions_dock.setObjectName("comparatorDock")
        self.solutions_dock.setAllowedAreas(Qt.DockWidgetArea.BottomDockWidgetArea)
        self.solutions_dock.setWidget(comparator_panel)
        self.addDockWidget(
            Qt.DockWidgetArea.BottomDockWidgetArea,
            self.solutions_dock,
        )
        # tabify only after both docks are added — otherwise Qt 6.11/macOS
        # can leave a dangling dock layout and SIGSEGV on raise_().
        self.tabifyDockWidget(self.console_dock, self.solutions_dock)
        self._raise_dock(self.console_dock)

        self._menus["view"].addSeparator()
        self._dock_toggles = {
            "explorer": self.explorer_dock.toggleViewAction(),
            "inspector": self.inspector_dock.toggleViewAction(),
            "timeline": self.console_dock.toggleViewAction(),
            "comparator": self.solutions_dock.toggleViewAction(),
        }
        for key, action in self._dock_toggles.items():
            action.setText(self._tr(f"dock.{key}"))
            tip_key = f"tip.toggle_{key}"
            tip = self._tr(tip_key)
            action.setStatusTip(with_native_shortcuts(tip) if tip != tip_key else "")
            action.toggled.connect(
                lambda checked, dock_key=key: self._on_dock_toggled(dock_key, checked)
            )
            self._menus["view"].addAction(action)
        self._actions["toggle_explorer"] = self._dock_toggles["explorer"]
        self._actions["toggle_inspector"] = self._dock_toggles["inspector"]
        self._actions["toggle_timeline"] = self._dock_toggles["timeline"]
        self._actions["toggle_comparator"] = self._dock_toggles["comparator"]
        apply_shortcuts(self._actions)
        self._sync_dock_toggle_tips()

        self._menus["view"].addSeparator()
        self._menus["view"].addAction(self._actions["reset_window_layout"])

        self.clear_inspector()

    def _on_dock_toggled(self, key: str, checked: bool) -> None:
        """Announce dock visibility changes in the status bar."""
        if not _qt_is_valid(self):
            return
        self._sync_dock_toggle_tips()
        name = self._tr(f"dock.{key}")
        self._status(
            "status.dock_shown" if checked else "status.dock_hidden",
            name=name,
        )

    def _sync_dock_toggle_tips(self) -> None:
        """Tip Mostrar/Ocultar según visibilidad actual de cada dock."""
        if not _qt_is_valid(self):
            return
        toggles = getattr(self, "_dock_toggles", None)
        if not toggles:
            return
        for key, action in toggles.items():
            if not _qt_is_valid(action):
                continue
            visible = action.isChecked()
            tip_key = f"tip.toggle_{key}_{'hide' if visible else 'show'}"
            tip = self._tr(tip_key)
            if tip == tip_key:
                tip = self._tr(f"tip.toggle_{key}")
            action.setStatusTip(with_native_shortcuts(tip) if tip else "")

    def _build_statusbar(self):
        status = QStatusBar(self)
        self.setStatusBar(status)
        self._project_path_label = QLabel()
        self._project_path_label.setObjectName("statusProjectPath")
        self._project_path_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self._zoom_label = QLabel()
        self._zoom_label.setObjectName("statusZoom")
        status.addPermanentWidget(self._project_path_label, 1)
        status.addPermanentWidget(self._zoom_label)
        status.showMessage(self._tr("status.ready"))
        self.workspace.camera_changed.connect(self._update_zoom_status)
        self._update_project_path_status()
        self._update_zoom_status(self.workspace.zoom)

    def _load_empty_project(
        self,
        *,
        name: str | None = None,
        project_id: str | None = None,
    ) -> None:
        project = StudioProject(
            project_id=project_id or new_project_id(),
            name=name or self._tr("project.untitled"),
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
            root.setData(0, Qt.ItemDataRole.UserRole, "project:root")
            boards_root = QTreeWidgetItem(
                [self._tr("explorer.boards", n=len(project.boards))]
            )
            boards_root.setData(0, Qt.ItemDataRole.UserRole, "category:boards")
            pieces_root = QTreeWidgetItem(
                [self._tr("explorer.pieces", n=len(project.pieces))]
            )
            pieces_root.setData(0, Qt.ItemDataRole.UserRole, "category:pieces")
            solutions_root = QTreeWidgetItem(
                [
                    self._tr(
                        "explorer.solutions",
                        n=len(self.services.layout.solutions),
                    )
                ]
            )
            solutions_root.setData(0, Qt.ItemDataRole.UserRole, "category:solutions")
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
                placed = project.placement_by_piece_id(piece.piece_id) is not None
                piece_label = (
                    f"{piece.piece_id} — "
                    f"{self._format_size(piece.length_mm, piece.width_mm, thickness_mm=piece.thickness_mm)}"
                )
                if not placed:
                    piece_label = (
                        f"{piece_label} — {self._tr('explorer.unplaced_mark')}"
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

            piece_ids = self.workspace.selection.selected()
            if len(piece_ids) == 1:
                piece_item = self._find_explorer_item_by_role(f"piece:{piece_ids[0]}")
                if piece_item is not None:
                    self.explorer.setCurrentItem(piece_item)
            elif selected_solution_item is not None:
                self.explorer.setCurrentItem(selected_solution_item)

        finally:
            self.explorer.blockSignals(previous_signal_state)

    def _find_explorer_item_by_role(self, role: str) -> QTreeWidgetItem | None:
        """Return the first explorer item whose UserRole matches ``role``."""

        def walk(item: QTreeWidgetItem) -> QTreeWidgetItem | None:
            if item.data(0, Qt.ItemDataRole.UserRole) == role:
                return item
            for index in range(item.childCount()):
                found = walk(item.child(index))
                if found is not None:
                    return found
            return None

        for index in range(self.explorer.topLevelItemCount()):
            top = self.explorer.topLevelItem(index)
            if top is None:
                continue
            found = walk(top)
            if found is not None:
                return found
        return None

    def sync_explorer_piece_selection(self) -> None:
        """Mirror the Workspace piece selection onto the Explorador tree."""
        selected_ids = self.workspace.selection.selected()
        blocked = self.explorer.blockSignals(True)
        try:
            if len(selected_ids) == 1:
                item = self._find_explorer_item_by_role(f"piece:{selected_ids[0]}")
                if item is not None:
                    self.explorer.setCurrentItem(item)
                    self.explorer.scrollToItem(item)
                    return

            current = self.explorer.currentItem()
            if current is None:
                return
            parsed = parse_explorer_role(current.data(0, Qt.ItemDataRole.UserRole))
            if parsed is not None and parsed[0] == "piece":
                self.explorer.clearSelection()
                selection_model = self.explorer.selectionModel()
                if selection_model is not None:
                    selection_model.clearCurrentIndex()
        finally:
            self.explorer.blockSignals(blocked)

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

        parsed = parse_explorer_role(data)
        if parsed is None:
            self.inspector.setText(f"{self._tr('inspector.title')}\n\n{item.text(0)}")
            return
        kind, object_id = parsed

        if kind in {"category", "project"}:
            self.workspace.clear_piece_selection()
            self.inspector.setText(f"{self._tr('inspector.title')}\n\n{item.text(0)}")
            return

        if kind == "solution":
            self.workspace.clear_piece_selection()
            self._select_layout_solution(int(object_id))
            return

        if kind == "board":
            self.select_explorer_board(object_id)
            return

        if kind == "piece":
            # select_piece → sync_inspector → full piece Inspector (position/panel).
            self.workspace.select_piece(object_id)
            self.workspace.center_on_piece(object_id)

    def select_explorer_board(self, board_id: str) -> None:
        """Focus a board on the canvas and mirror it in Explorador + Inspector."""
        self.workspace.clear_piece_selection()
        self.workspace.focus_board(board_id)
        self._show_board_inspector(board_id)

        item = self._find_explorer_item_by_role(f"board:{board_id}")
        if item is None:
            return
        blocked = self.explorer.blockSignals(True)
        try:
            self.explorer.setCurrentItem(item)
            self.explorer.scrollToItem(item)
        finally:
            self.explorer.blockSignals(blocked)

    def _show_board_inspector(self, board_id: str) -> None:
        project = self.services.projects.current_project
        if project is None:
            return
        board = next(
            (
                candidate
                for candidate in project.boards
                if candidate.board_id == board_id
            ),
            None,
        )
        if board is None:
            return
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

    def _new_project(self):
        if not self._confirm_discard_unsaved_changes():
            return

        prefs = self.services.preferences.current
        dialog = NewProjectDialog(
            self,
            name=self._tr("project.untitled"),
            units=prefs.units,
            language=self._ui_language(),
        )
        if dialog.exec() != NewProjectDialog.DialogCode.Accepted:
            return

        data = dialog.project_data()
        if not data["name"]:
            QMessageBox.warning(
                self,
                self._tr("form.new_project"),
                self._tr("dialog.project_name_required"),
            )
            return

        if data["units"] != prefs.units:
            self.services.preferences.update(
                dataclass_replace(prefs, units=data["units"])
            )
            self._apply_preferences()

        self._load_empty_project(name=data["name"])
        self._show_workspace()
        self._emit(
            events.PROJECT_CREATED,
            kind="empty",
            name=data["name"],
        )
        self._status("status.new_project_created", name=data["name"])

    def _new_demo_project(self):
        if not self._confirm_discard_unsaved_changes():
            return

        raised_limit = self._ensure_demo_multi_solution_prefs()
        self._load_demo_project()
        self.services.layout.clear_solutions()
        self._show_workspace()
        self._emit(events.PROJECT_CREATED, kind="demo")
        if raised_limit:
            self._status(
                "status.demo_created_max_solutions_raised",
                n=self.services.preferences.current.max_solutions,
            )
        else:
            self._status("status.demo_created")

    def _ensure_demo_multi_solution_prefs(self) -> bool:
        """Ensure demo can show the comparator (≥2 candidatas).

        UAT often stalls with ``max_solutions=1``: Calcular layout keeps only
        one candidate and PgUp/Comparador look broken. Demo raises the floor
        back to the default when the preference is too low.
        """
        from studio.preferences import DEFAULT_MAX_SOLUTIONS

        prefs = self.services.preferences.current
        if prefs.max_solutions >= 2:
            return False
        try:
            self.services.preferences.update(
                dataclass_replace(prefs, max_solutions=DEFAULT_MAX_SOLUTIONS)
            )
        except OSError:
            return False
        return True

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
            manager=manager,
            language=self._ui_language(),
            parent=self,
        )
        result = dialog.exec()
        self._sync_template_actions()
        if result != dialog.DialogCode.Accepted:
            return
        name = dialog.selected_name()
        if not name:
            return

        include_placements = False
        if dialog.selected_placement_count() > 0:
            answer = QMessageBox.question(
                self,
                self._tr("template.pick_title"),
                self._tr("template.load_placements"),
            )
            include_placements = answer == QMessageBox.StandardButton.Yes

        project = manager.instantiate(name, include_placements=include_placements)
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
        self._sync_template_actions()
        self._status("status.template_saved", name=name)

    def _show_whats_new(self) -> None:
        dialog = WhatsNewDialog(language=self._ui_language(), parent=self)
        dialog.exec()

    def _show_about(self) -> None:
        dialog = AboutDialog(language=self._ui_language(), parent=self)
        dialog.exec()

    def _show_shortcuts(self) -> None:
        dialog = ShortcutsDialog(language=self._ui_language(), parent=self)
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

        board = StudioBoard(
            board_id=data["board_id"],
            length_mm=data["length_mm"],
            width_mm=data["width_mm"],
            material=data["material"],
            thickness_mm=data["thickness_mm"],
            quantity=data["quantity"],
        )
        self.services.commands.execute(AddBoardCommand(self.services, board))

        self._mark_project_modified()
        self.workspace.reload_project()
        self._reload_explorer()
        self.update_window_title()
        self.update_undo_redo()

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
            header_map, missing = self._apply_import_template(
                kind="boards",
                fieldnames=loaded.fieldnames,
                header_map=header_map,
                required_fields=BOARD_REQUIRED_FIELDS,
            )
        if missing:
            mapped = self._prompt_column_mapping(
                kind="boards",
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
            header_map, missing = self._apply_import_template(
                kind="pieces",
                fieldnames=loaded.fieldnames,
                header_map=header_map,
                required_fields=PIECE_REQUIRED_FIELDS,
            )
        if missing:
            mapped = self._prompt_column_mapping(
                kind="pieces",
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
        piece_lookup = {piece.piece_id: piece for piece in project.pieces}
        piece_lookup.update({piece.piece_id: piece for piece in pieces})
        for piece in pieces:
            x_mm, y_mm = self._find_free_piece_position(
                piece.length_mm,
                piece.width_mm,
                extra_placements=placements,
                piece_lookup=piece_lookup,
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

    def _apply_import_template(
        self,
        *,
        kind: str,
        fieldnames: list[str] | tuple[str, ...],
        header_map: dict[str, str],
        required_fields: tuple[str, ...],
    ) -> tuple[dict[str, str], list[str]]:
        """Merge a saved mapping template when it covers required fields."""
        template = self.services.import_templates.find_applicable(
            kind,
            fieldnames,
            required_fields,
        )
        if template is None:
            missing = missing_required_fields(header_map, required_fields)
            return header_map, missing

        merged = {
            **header_map,
            **sanitize_header_map(template.header_map, fieldnames),
        }
        missing = missing_required_fields(merged, required_fields)
        if not missing:
            self._status(
                "status.import_template_applied",
                5000,
                name=template.name,
            )
        return merged, missing

    def _prompt_column_mapping(
        self,
        *,
        kind: str,
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
            templates_manager=self.services.import_templates,
            kind=kind,
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
        self._maybe_save_import_template(kind, mapped)
        return mapped

    def _maybe_save_import_template(
        self, kind: str, header_map: dict[str, str]
    ) -> None:
        """Offer to persist the confirmed mapping as a reusable template."""
        answer = QMessageBox.question(
            self,
            self._tr("import.mapping_save_title"),
            self._tr("import.mapping_save_prompt"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        name, ok = QInputDialog.getText(
            self,
            self._tr("import.mapping_save_title"),
            self._tr("import.mapping_save_name"),
        )
        if not ok or not name.strip():
            return
        try:
            template = self.services.import_templates.save_template(
                kind,
                name,
                header_map,
            )
        except ValueError as exc:
            QMessageBox.warning(
                self,
                self._tr("import.mapping_save_title"),
                str(exc),
            )
            return
        self._status("status.import_template_saved", 5000, name=template.name)

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

        pieces: list[StudioPiece] = []
        placements: list[StudioPlacement] = []
        piece_lookup = {piece.piece_id: piece for piece in project.pieces}
        for piece_id in piece_ids:
            piece = StudioPiece(
                piece_id=piece_id,
                length_mm=data["length_mm"],
                width_mm=data["width_mm"],
                material=data["material"],
                thickness_mm=data["thickness_mm"],
            )
            pieces.append(piece)
            piece_lookup[piece_id] = piece
            x_mm, y_mm = self._find_free_piece_position(
                data["length_mm"],
                data["width_mm"],
                extra_placements=placements,
                piece_lookup=piece_lookup,
            )
            placements.append(
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

        self.services.commands.execute(
            AddPieceCommand(self.services, pieces, placements)
        )

        self._mark_project_modified()
        self.workspace.reload_project()
        self._reload_explorer()
        self.update_window_title()
        self.update_undo_redo()

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

        try:
            piece = project.piece_by_id(piece_id)
        except KeyError:
            # Stale explorer/canvas selection after undo without a tree reload.
            self.clear_inspector()
            return

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
                f"{self._tr('inspector.thickness')}: "
                f"{self._format_length(piece.thickness_mm)}\n"
                f"{self._tr('inspector.material')}: {piece.material}\n"
                f"{self._tr('inspector.unplaced')}\n"
                f"{self._tr('inspector.place_hint')}"
            )
            return

        self.inspector.setText(
            f"{self._tr('inspector.title')}\n\n"
            f"{self._tr('inspector.piece')}: {piece.piece_id}\n"
            f"{self._tr('inspector.dimensions')}: "
            f"{self._format_size(piece.length_mm, piece.width_mm)}\n"
            f"{self._tr('inspector.thickness')}: "
            f"{self._format_length(piece.thickness_mm)}\n"
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
        else:
            self.setWindowTitle(f"{marker}BoardComposer Studio — {project.name}")
        self._update_project_path_status()
        self._sync_project_file_actions()
        self._sync_generate_actions()
        self._sync_view_actions()
        self._sync_edit_selection_actions()
        self._sync_template_actions()

    def _sync_project_file_actions(self) -> None:
        """Enable save/rename/template only when a project is open."""
        has_project = self.services.projects.current_project is not None
        need_project = self._tr("status.nothing_to_save")
        need_rename = self._tr("status.nothing_to_rename")
        need_template = self._tr("status.template_missing_project")

        pairs = (
            ("save", "tip.save", need_project),
            ("save_as", "tip.save_as", need_project),
            ("save_as_template", "tip.save_as_template", need_template),
            ("rename_project", "tip.rename_project", need_rename),
        )
        for key, tip_key, disabled_tip in pairs:
            action = self._actions.get(key)
            if action is None:
                continue
            action.setEnabled(has_project)
            tip = (
                with_native_shortcuts(self._tr(tip_key))
                if has_project
                else disabled_tip
            )
            action.setStatusTip(tip)

    def _sync_template_actions(self) -> None:
        """Enable «Nuevo desde plantilla» only when templates exist."""
        manager = self.services.project_templates
        manager.refresh()
        has_templates = bool(manager.list())
        action = self._actions.get("new_from_template")
        if action is not None:
            action.setEnabled(has_templates)
            action.setStatusTip(
                with_native_shortcuts(self._tr("tip.new_from_template"))
                if has_templates
                else self._tr("status.template_empty")
            )
        if hasattr(self, "welcome"):
            self.welcome.set_has_templates(has_templates)

    def _sync_generate_actions(self) -> None:
        """Enable layout calculation only when a project is open."""
        has_project = self.services.projects.current_project is not None
        solve = self._actions.get("solve_layout")
        if solve is None:
            return
        solve.setEnabled(has_project)
        solve.setStatusTip(
            with_native_shortcuts(self._tr("tip.solve_layout"))
            if has_project
            else self._tr("status.nothing_to_solve")
        )

    def _update_project_path_status(self) -> None:
        """Refresh the permanent project-path widget and reveal action."""
        label = getattr(self, "_project_path_label", None)
        filename = self.services.projects.filename
        if label is not None:
            if filename:
                from PySide6.QtGui import QFontMetrics

                metrics = QFontMetrics(label.font())
                elided = metrics.elidedText(filename, Qt.TextElideMode.ElideMiddle, 560)
                label.setText(elided)
                label.setToolTip(filename)
            else:
                label.setText(self._tr("status.project_unsaved"))
                label.setToolTip("")
        reveal = self._actions.get("reveal_project_folder")
        if reveal is not None:
            has_file = bool(filename)
            reveal.setEnabled(has_file)
            tip = (
                with_native_shortcuts(self._tr("tip.reveal_project_folder"))
                if has_file
                else self._tr("status.project_folder_unavailable")
            )
            reveal.setStatusTip(tip)

    def _update_zoom_status(self, zoom: float | None = None) -> None:
        """Refresh the permanent Workspace zoom widget."""
        label = getattr(self, "_zoom_label", None)
        if label is not None:
            factor = self.workspace.zoom if zoom is None else zoom
            percent = max(1, int(round(factor * 100)))
            label.setText(self._tr("status.zoom", n=percent))
            tip = self._tr("tip.zoom_status")
            label.setToolTip(tip if tip != "tip.zoom_status" else "")
        self._sync_zoom_actions()

    def _sync_zoom_actions(self) -> None:
        """Enable zoom actions only while the camera can still move."""
        zoom_in = self._actions.get("zoom_in")
        zoom_out = self._actions.get("zoom_out")
        if zoom_in is None or zoom_out is None:
            return
        can_in = self.workspace.can_zoom_in
        can_out = self.workspace.can_zoom_out
        zoom_in.setEnabled(can_in)
        zoom_out.setEnabled(can_out)
        zoom_in.setStatusTip(
            with_native_shortcuts(self._tr("tip.zoom_in"))
            if can_in
            else self._tr("status.zoom_at_maximum")
        )
        zoom_out.setStatusTip(
            with_native_shortcuts(self._tr("tip.zoom_out"))
            if can_out
            else self._tr("status.zoom_at_minimum")
        )

    def update_undo_redo(self):
        """Refresh enabled state and honest status tips for undo/redo."""
        can_undo = self.services.commands.can_undo()
        can_redo = self.services.commands.can_redo()
        undo = self._actions["undo"]
        redo = self._actions["redo"]
        undo.setEnabled(can_undo)
        redo.setEnabled(can_redo)
        undo.setStatusTip(
            with_native_shortcuts(self._tr("tip.undo"))
            if can_undo
            else self._tr("status.nothing_to_undo")
        )
        redo.setStatusTip(
            with_native_shortcuts(self._tr("tip.redo"))
            if can_redo
            else self._tr("status.nothing_to_redo")
        )
        apply_shortcuts(self._actions)

    def _undo(self):
        self.services.commands.undo()
        self.workspace.reload_project()
        self._reload_explorer()
        self.update_undo_redo()

    def _redo(self):
        self.services.commands.redo()
        self.workspace.reload_project()
        self._reload_explorer()
        self.update_undo_redo()

    def _rotate_selected_piece(self):
        piece_id = self.workspace.selection.current()
        if piece_id is None:
            self._status("status.select_piece_first")
            return

        item = self.workspace.piece_item_by_id(piece_id)
        if item is None:
            self._status("status.select_piece_first")
            return

        project = self.services.projects.current_project
        if project is None:
            self._status("status.select_piece_first")
            return

        placement = project.placement_by_piece_id(piece_id)
        if placement is None:
            self._status("status.select_piece_first")
            return

        old_rotation = placement.rotation
        new_rotation = 90 if old_rotation % 180 == 0 else 0

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
        self._status("status.piece_rotated")

    def _delete_selected_piece(self):
        """Delete the selected piece, or the focused/explorer board (Delete)."""
        piece_id = self.workspace.selection.current()
        if piece_id is not None:
            self._delete_piece_by_id(piece_id)
            return

        item = self.explorer.currentItem()
        if item is not None:
            parsed = parse_explorer_role(item.data(0, Qt.ItemDataRole.UserRole))
            if parsed is not None:
                kind, object_id = parsed
                if kind == "piece":
                    self._delete_piece_by_id(object_id)
                    return
                if kind == "board":
                    self._delete_board(object_id)
                    return

        focused = self.workspace.focused_board_id()
        if focused is not None:
            self._delete_board(focused)
            return

        self._status("status.nothing_to_delete")

    def _delete_piece_by_id(self, piece_id: str) -> None:
        project = self.services.projects.current_project
        if project is None:
            return

        placed = project.placement_by_piece_id(piece_id) is not None
        if placed:
            message = self._tr("dialog.delete_piece_confirm_placed", id=piece_id)
        else:
            message = self._tr("dialog.delete_piece_confirm", id=piece_id)
        answer = QMessageBox.question(
            self,
            self._tr("dialog.delete_piece_title"),
            message,
        )
        if answer != QMessageBox.StandardButton.Yes:
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
        self._status("status.piece_deleted", id=piece_id)

    def _duplicate_selected_piece(self) -> None:
        """Duplicate the selected piece, or the focused/explorer board (Ctrl+D)."""
        piece_id = self.workspace.selection.current()
        if piece_id is not None:
            self._duplicate_piece_by_id(piece_id)
            return

        item = self.explorer.currentItem()
        if item is not None:
            parsed = parse_explorer_role(item.data(0, Qt.ItemDataRole.UserRole))
            if parsed is not None:
                kind, object_id = parsed
                if kind == "piece":
                    self._duplicate_piece_by_id(object_id)
                    return
                if kind == "board":
                    self._duplicate_board(object_id)
                    return

        focused = self.workspace.focused_board_id()
        if focused is not None:
            self._duplicate_board(focused)
            return

        self._status("status.nothing_to_duplicate")

    def _duplicate_piece_by_id(self, piece_id: str) -> None:
        project = self.services.projects.current_project
        if project is None:
            return

        try:
            source = project.piece_by_id(piece_id)
        except KeyError:
            return

        existing_ids = {piece.piece_id.casefold() for piece in project.pieces}
        new_id = allocate_unique_piece_id(f"{source.piece_id}-copy", existing_ids)
        clone = StudioPiece(
            piece_id=new_id,
            length_mm=source.length_mm,
            width_mm=source.width_mm,
            material=source.material,
            thickness_mm=source.thickness_mm,
        )

        source_placement = project.placement_by_piece_id(piece_id)
        if source_placement is not None:
            placement = StudioPlacement(
                piece_id=new_id,
                x_mm=source_placement.x_mm + 20.0,
                y_mm=source_placement.y_mm + 20.0,
                rotated=source_placement.rotated,
                rotation=source_placement.rotation,
                board_id=source_placement.board_id,
                board_instance=source_placement.board_instance,
                stock_panel_index=source_placement.stock_panel_index,
            )
        else:
            x_mm, y_mm = self._find_free_piece_position(
                clone.length_mm,
                clone.width_mm,
            )
            placement = StudioPlacement(
                piece_id=new_id,
                x_mm=x_mm,
                y_mm=y_mm,
                rotated=False,
                rotation=0,
                board_id=project.boards[0].board_id if project.boards else None,
                board_instance=0,
                stock_panel_index=0 if project.boards else None,
            )

        command = DuplicatePieceCommand(self.services, clone, placement)
        self.services.commands.execute(command)

        self.workspace.reload_project()
        self._reload_explorer()
        self.workspace.select_piece(new_id)
        self.refresh_inspector_for_piece(new_id)
        self._mark_project_modified(reason="piece_duplicated")
        self.update_window_title()
        self.update_undo_redo()
        self._status("status.piece_duplicated", id=new_id)

    def _select_all_pieces(self) -> None:
        self.workspace.select_all_pieces()
        count = len(self.workspace.selection.selected())
        if count:
            self._status("status.pieces_selected", n=count)
        else:
            self._status("status.no_pieces_to_select")

    def _deselect_pieces(self) -> None:
        had_selection = bool(self.workspace.selection.selected())
        self.workspace.clear_piece_selection()
        if had_selection:
            self._status("status.selection_cleared")
        else:
            self._status("status.nothing_to_deselect")

    def _invert_selection(self) -> None:
        self.workspace.invert_piece_selection()
        count = len(self.workspace.selection.selected())
        if count:
            self._status("status.pieces_selected", n=count)
        else:
            self._status("status.selection_cleared")

    def _fit_board(self) -> None:
        if not self.workspace.fit_board():
            self._status("status.nothing_to_fit_board")

    def _fit_selection(self) -> None:
        if not self.workspace.fit_selection():
            self._status("status.nothing_to_fit_selection")

    def _zoom_in(self) -> None:
        if not self.workspace.can_zoom_in:
            self._status("status.zoom_at_maximum")
            return
        self.workspace.zoom_in()

    def _zoom_out(self) -> None:
        if not self.workspace.can_zoom_out:
            self._status("status.zoom_at_minimum")
            return
        self.workspace.zoom_out()

    def _toggle_grid(self, checked: bool) -> None:
        prefs = self.services.preferences.current
        if prefs.show_grid == checked:
            return
        self.services.preferences.update(dataclass_replace(prefs, show_grid=checked))
        self.workspace.reload_project(fit=False)
        self._sync_view_actions()
        self._status("status.grid_shown" if checked else "status.grid_hidden")

    def _sync_view_actions(self) -> None:
        action = self._actions.get("toggle_grid")
        fit_board = self._actions.get("fit_board")
        fit_selection = self._actions.get("fit_selection")
        rotate_piece = self._actions.get("rotate_piece")
        if (
            action is None
            or fit_board is None
            or fit_selection is None
            or rotate_piece is None
        ):
            return
        action.blockSignals(True)
        action.setChecked(self.services.preferences.current.show_grid)
        action.blockSignals(False)
        grid_on = self.services.preferences.current.show_grid
        action.setStatusTip(
            with_native_shortcuts(
                self._tr("tip.toggle_grid_hide" if grid_on else "tip.toggle_grid_show")
            )
        )

        project = self.services.projects.current_project
        has_boards = bool(project and project.boards)
        fit_board.setEnabled(has_boards)
        fit_board.setStatusTip(
            with_native_shortcuts(self._tr("tip.fit_board"))
            if has_boards
            else self._tr("status.nothing_to_fit_board")
        )
        can_fit_selection = bool(self.workspace.selection.selected()) or (
            self.workspace.focused_board_id() is not None
        )
        fit_selection.setEnabled(can_fit_selection)
        fit_selection.setStatusTip(
            with_native_shortcuts(self._tr("tip.fit_selection"))
            if can_fit_selection
            else self._tr("status.nothing_to_fit_selection")
        )
        piece_id = self.workspace.selection.current()
        can_rotate = bool(
            piece_id is not None
            and project is not None
            and project.placement_by_piece_id(piece_id) is not None
        )
        rotate_piece.setEnabled(can_rotate)
        rotate_piece.setStatusTip(
            with_native_shortcuts(self._tr("tip.rotate_piece"))
            if can_rotate
            else self._tr("status.select_piece_first")
        )

    def _explorer_selection_kind(self) -> str | None:
        item = self.explorer.currentItem()
        if item is None:
            return None
        parsed = parse_explorer_role(item.data(0, Qt.ItemDataRole.UserRole))
        if parsed is None:
            return None
        return parsed[0]

    def _sync_edit_selection_actions(self) -> None:
        """Enable Edit selection actions only when they have a usable target."""
        explorer_kind = self._explorer_selection_kind()
        has_piece = self.workspace.selection.current() is not None
        selected = self.workspace.selection.selected()
        single_piece = len(selected) == 1
        has_selection = bool(selected)
        has_focus_board = self.workspace.focused_board_id() is not None
        explorer_piece_or_board = explorer_kind in {"piece", "board"}
        project = self.services.projects.current_project
        has_canvas_pieces = bool(project and project.placements)

        can_delete_or_duplicate = (
            has_piece or explorer_piece_or_board or has_focus_board
        )
        can_edit = explorer_piece_or_board or single_piece or has_focus_board
        can_rename = explorer_kind in {"piece", "board", "project"} or single_piece
        can_copy = explorer_piece_or_board or single_piece or has_focus_board

        pairs = (
            (
                "delete_piece",
                can_delete_or_duplicate,
                "tip.delete_piece",
                "status.nothing_to_delete",
            ),
            (
                "duplicate_piece",
                can_delete_or_duplicate,
                "tip.duplicate_piece",
                "status.nothing_to_duplicate",
            ),
            (
                "edit_selection",
                can_edit,
                "tip.edit_selection",
                "status.nothing_to_edit_selection",
            ),
            (
                "rename_selection",
                can_rename,
                "tip.rename_selection",
                "status.nothing_to_rename_selection",
            ),
            (
                "copy_selection_id",
                can_copy,
                "tip.copy_selection_id",
                "status.nothing_to_copy_id",
            ),
            (
                "select_all_pieces",
                has_canvas_pieces,
                "tip.select_all_pieces",
                "status.no_pieces_to_select",
            ),
            (
                "deselect_pieces",
                has_selection,
                "tip.deselect_pieces",
                "status.nothing_to_deselect",
            ),
            (
                "invert_selection",
                has_canvas_pieces,
                "tip.invert_selection",
                "status.no_pieces_to_select",
            ),
        )
        for key, enabled, tip_key, disabled_tip in pairs:
            action = self._actions.get(key)
            if action is None:
                continue
            action.setEnabled(enabled)
            action.setStatusTip(
                with_native_shortcuts(self._tr(tip_key))
                if enabled
                else self._tr(disabled_tip)
            )

    def _sync_solution_actions(self) -> None:
        """Enable solution actions only when they can do useful work."""
        total = len(self.services.layout.solutions)
        has_any = total > 0
        has_multiple = total > 1
        self._actions["apply_layout"].setEnabled(has_any)
        self._actions["export_selected"].setEnabled(has_any)
        self._actions["previous_solution"].setEnabled(has_multiple)
        self._actions["next_solution"].setEnabled(has_multiple)

        pin = getattr(self, "pin_reference_button", None)
        if pin is not None:
            pin.setEnabled(has_multiple)

        sort = getattr(self, "comparator_sort", None)
        sort_label = getattr(self, "comparator_sort_label", None)
        complete_only = getattr(self, "comparator_complete_only", None)
        if sort is not None:
            sort.setEnabled(has_any)
        if sort_label is not None:
            sort_label.setEnabled(has_any)
        if complete_only is not None:
            complete_only.setEnabled(has_any)

        need_layout = with_native_shortcuts(self._tr("status.calculate_layout_first"))
        only_one = with_native_shortcuts(self._tr("status.only_one_visible_solution"))
        apply = self._actions["apply_layout"]
        export = self._actions["export_selected"]
        previous = self._actions["previous_solution"]
        next_action = self._actions["next_solution"]
        apply.setStatusTip(
            with_native_shortcuts(self._tr("tip.apply_layout"))
            if has_any
            else need_layout
        )
        export.setStatusTip(
            with_native_shortcuts(self._tr("tip.export_selected"))
            if has_any
            else need_layout
        )
        previous.setStatusTip(
            with_native_shortcuts(self._tr("tip.previous_solution"))
            if has_multiple
            else (only_one if has_any else need_layout)
        )
        next_action.setStatusTip(
            with_native_shortcuts(self._tr("tip.next_solution"))
            if has_multiple
            else (only_one if has_any else need_layout)
        )
        if pin is not None:
            pin_tip = (
                self._tr("tip.pin_reference")
                if has_multiple
                else (only_one if has_any else need_layout)
            )
            pin.setToolTip(pin_tip)
            pin.setStatusTip(pin_tip)
        if sort is not None:
            sort_tip = self._tr("tip.comparator_sort") if has_any else need_layout
            sort.setToolTip(sort_tip)
            sort.setStatusTip(sort_tip)
        if complete_only is not None:
            filter_tip = (
                self._tr("tip.comparator_complete_only") if has_any else need_layout
            )
            complete_only.setToolTip(filter_tip)
            complete_only.setStatusTip(filter_tip)

    def _sync_timeline_actions(self) -> None:
        """Enable Timeline export only when there are events to export."""
        action = self._actions.get("export_timeline")
        if action is None:
            return
        entries = self.services.timeline.filtered(
            self.console.current_filter_event(),
            algorithm=self.console.current_filter_algorithm(),
            since=self.console.current_filter_since(),
        )
        has_events = bool(entries)
        action.setEnabled(has_events)
        tip_key = (
            "tip.export_timeline" if has_events else "status.timeline_export_empty"
        )
        tip = self._tr(tip_key)
        action.setStatusTip(with_native_shortcuts(tip) if tip != tip_key else tip)

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
            tip_key = f"tip.{key}"
            tip = self._tr(tip_key)
            action.setStatusTip(with_native_shortcuts(tip) if tip != tip_key else "")
        self._recent_menu.setTitle(self._tr("menu.recent"))
        if hasattr(self, "_toolbar"):
            self._toolbar.setWindowTitle(self._tr("toolbar.main"))
        if hasattr(self, "_toolbar_toggle"):
            self._toolbar_toggle.setText(self._tr("action.toggle_toolbar"))
            tip = self._tr("tip.toggle_toolbar")
            self._toolbar_toggle.setStatusTip(
                with_native_shortcuts(tip) if tip != "tip.toggle_toolbar" else ""
            )
        if hasattr(self, "_dock_toggles"):
            for key, action in self._dock_toggles.items():
                action.setText(self._tr(f"dock.{key}"))
            self._sync_dock_toggle_tips()

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
        self.pin_reference_button.setToolTip(self._tr("tip.pin_reference"))
        self.pin_reference_button.setStatusTip(self._tr("tip.pin_reference"))
        self.comparator_diff_label.setText(self._tr("comparator.diff_title"))
        self._refresh_solutions_outdated_banner()
        self.solution_differences.setPlaceholderText(
            self._tr("comparator.diff_placeholder")
        )

        self._reload_recent_files_menu()
        self._update_project_path_status()
        self._update_zoom_status()
        self.workspace.retranslate(self._ui_language())
        self.update_undo_redo()
        self._sync_project_file_actions()
        self._sync_generate_actions()
        self._sync_solution_actions()
        self._sync_timeline_actions()
        self._sync_edit_selection_actions()
        self._sync_zoom_actions()
        self._sync_template_actions()
        self._sync_welcome_action()
        self._sync_view_actions()
        self._sync_dock_toggle_tips()

    def _apply_preferences(self) -> None:
        from PySide6.QtWidgets import QApplication

        from studio.theme import apply_theme

        app = QApplication.instance()
        if isinstance(app, QApplication):
            apply_theme(app, self.services.preferences.current.theme)
        self._retranslate_ui()
        self._sync_view_actions()
        self._sync_edit_selection_actions()
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
        self._comparator_reference_pinned = False
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
        self._reveal_comparator_after_solve()

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
            self._maybe_warn_solution_truncated_by_limit(solution_count)
            return

        self._announce_layout_ok(solution_count)

    def _reveal_comparator_after_solve(self) -> None:
        """Bring Comparador forward so multi-candidate UAT is not buried under Timeline."""
        dock = getattr(self, "solutions_dock", None)
        if dock is None:
            return
        dock.show()
        self._raise_dock(dock)

    def _announce_layout_ok(self, shown: int) -> None:
        """Status after a complete solve: count + why there aren't more."""
        if shown <= 1 and int(self.services.layout.stats.accepted) <= 1:
            stats = self.services.layout.stats
            self._status(
                "status.layout_ok_single",
                8000,
                generated=int(stats.generated),
                unique=int(stats.unique),
            )
            return
        self._status("status.layout_ok", 8000, n=shown)
        self._maybe_warn_solution_truncated_by_limit(shown)

    def _maybe_warn_solution_truncated_by_limit(self, shown: int) -> None:
        """Hint when more accepted candidates exist than currently shown."""
        accepted = int(self.services.layout.stats.accepted)
        if accepted <= shown:
            return
        limit = int(self.services.preferences.current.max_solutions)
        self._status(
            "status.layout_truncated_by_limit",
            7000,
            shown=shown,
            accepted=accepted,
            limit=limit,
        )

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

        self._decorate_comparator_reference()
        self._reload_solution_differences()
        self._sync_solution_actions()

    def _reference_row_brush(self) -> QBrush:
        from studio.theme_tokens import tokens_for

        theme = self.services.preferences.current.theme
        name = "light" if theme == "system" else theme
        tokens = tokens_for(name)
        color = QColor(tokens.alternate if tokens is not None else "#ebe1d4")
        return QBrush(color)

    def _decorate_comparator_reference(self) -> None:
        """Mark the pinned reference row/thumbnail (SCR-003)."""
        ref = self._comparator_reference_index
        pinned = self._comparator_reference_pinned and ref is not None
        brush = self._reference_row_brush() if pinned else QBrush()
        clear = QBrush()
        highlights = self.services.layout.solution_highlights

        for row, solution_index in enumerate(self._solution_display_indexes):
            is_ref = pinned and solution_index == ref
            number = str(solution_index + 1)
            label = (
                self._tr("comparator.reference_mark", n=number) if is_ref else number
            )
            row_highlights = highlights.get(solution_index, [])
            highlight_tip = (
                self._tr(
                    "comparator.best_in",
                    items=", ".join(self._tr(key) for key in row_highlights),
                )
                if row_highlights
                else ""
            )
            for column in range(self.solutions_table.columnCount()):
                item = self.solutions_table.item(row, column)
                if item is None:
                    continue
                if column == 0:
                    item.setText(label)
                item.setBackground(brush if is_ref else clear)
                if is_ref:
                    tip = self._tr("comparator.reference_tooltip", n=number)
                    item.setToolTip(f"{tip}\n{highlight_tip}" if highlight_tip else tip)
                else:
                    item.setToolTip(highlight_tip)

            thumb = self.solution_thumbnails.item(row)
            if thumb is not None:
                thumb.setText(
                    self._tr("comparator.reference_thumb", n=solution_index + 1)
                    if is_ref
                    else f"#{solution_index + 1}"
                )
                thumb.setToolTip(
                    (
                        self._tr("comparator.reference_tooltip", n=number)
                        + (f"\n{highlight_tip}" if highlight_tip else "")
                    )
                    if is_ref
                    else highlight_tip
                )

    def _pin_selected_as_reference(self) -> None:
        solutions = self.services.layout.solutions
        selected = self.services.layout.selected_solution_index
        if not solutions or selected < 0 or selected >= len(solutions):
            self._status("status.select_solution_first")
            return
        self._comparator_reference_index = selected
        self._comparator_reference_pinned = True
        self._decorate_comparator_reference()
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
        self._raise_dock(self.solutions_dock)

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
        self._step_layout_solution(-1)

    def _next_layout_solution(self):
        self._step_layout_solution(1)

    def _ensure_solution_display_indexes(self) -> list[int]:
        """Refresh visible comparator order when the cache is empty."""
        if self._solution_display_indexes:
            return self._solution_display_indexes
        self._solution_display_indexes = ordered_solution_indexes(
            self.services.layout.solutions,
            sort_by=self._comparator_sort_by,
            complete_only=self._comparator_complete_only,
            board_waste=self.services.layout.board_waste_ratio,
        )
        return self._solution_display_indexes

    def _step_layout_solution(self, delta: int) -> None:
        """Move selection along the comparator display order (SCR-003)."""
        display = self._ensure_solution_display_indexes()
        if not display:
            if self.services.layout.solutions:
                self._status("status.no_solutions_match_filter")
            else:
                self._status("status.no_solutions")
            return

        if len(display) == 1:
            only = display[0]
            if self.services.layout.selected_solution_index != only:
                solution = self.services.layout.select_solution(only)
                if solution is not None:
                    self.workspace.preview_solution(solution)
                    self._show_layout_solution(solution)
                    self._refresh_explorer_solution_markers()
                    self._reload_solution_table()
            accepted = int(self.services.layout.stats.accepted)
            cached = len(self.services.layout.solutions)
            if accepted > cached:
                limit = int(self.services.preferences.current.max_solutions)
                self._status(
                    "status.only_one_visible_truncated",
                    5000,
                    accepted=accepted,
                    limit=limit,
                )
            else:
                self._status("status.only_one_visible_solution", 5000)
            return

        next_index = step_display_index(
            display,
            self.services.layout.selected_solution_index,
            delta=delta,
        )
        if next_index is None:
            self._status("status.no_solutions")
            return

        solution = self.services.layout.select_solution(next_index)
        if solution is None:
            self._status("status.no_solutions")
            return

        self.workspace.preview_solution(solution)
        self._show_layout_solution(solution)
        self._refresh_explorer_solution_markers()
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
            self._suggested_export_path("boardcomposer-timeline.json"),
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

        self._remember_export_directory(path)
        self._status("status.timeline_exported", 5000, path=path)
        self._offer_open_exported_path(path)

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
            # pyright: ignore[reportArgumentType]
            self,
            self._tr("dialog.export_selected"),
            self._suggested_export_path(default_filename),
            options.file_filter,
        )
        if not path:
            return

        self._emit(
            events.EXPORT_STARTED,
            format=options.label,
            path=path,
        )
        try:
            payload = render_export(
                solution,
                self.services.layout.solved_project,
                options,
                strategy_name=self.services.layout.strategy_name,
                solution_index=self.services.layout.selected_solution_index,
            )
            if options.format in {"png", "jpeg"}:
                assert isinstance(payload, str)
                image_format = "PNG" if options.format == "png" else "JPEG"
                Path(path).write_bytes(
                    svg_to_raster_bytes(payload, image_format=image_format)
                )
            elif isinstance(payload, bytes):
                Path(path).write_bytes(payload)
            else:
                Path(path).write_text(payload, encoding="utf-8")
        except OSError as exc:
            self._emit(
                events.EXPORT_FAILED,
                format=options.label,
                path=path,
                error=str(exc),
            )
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
            last_export_directory=str(Path(path).expanduser().resolve().parent),
        )
        self.services.preferences.update(updated)

        self._emit(
            events.EXPORT_COMPLETED,
            format=options.label,
            path=path,
        )
        self._status("status.exported", 5000, format=options.label, path=path)
        self._offer_open_exported_path(path)

    def _suggested_export_path(self, default_filename: str) -> str:
        """Prefer last successful export folder when it still exists."""
        directory = self.services.preferences.current.last_export_directory
        if directory:
            folder = Path(directory).expanduser()
            if folder.is_dir():
                return str(folder / default_filename)
        return default_filename

    def _remember_export_directory(self, path: str | Path) -> None:
        """Persist the folder of a successful export for the next dialog."""
        folder = str(Path(path).expanduser().resolve().parent)
        prefs = self.services.preferences.current
        if prefs.last_export_directory == folder:
            return
        self.services.preferences.update(
            dataclass_replace(prefs, last_export_directory=folder)
        )

    def _offer_open_exported_path(self, path: str | Path) -> None:
        """After a successful export, offer to open the file or its folder."""
        from studio.file_reveal import open_local_path, reveal_in_file_manager

        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Information)
        box.setWindowTitle(self._tr("export.done_title"))
        box.setText(self._tr("export.done_message", path=str(path)))
        open_button = box.addButton(
            self._tr("export.open_file"),
            QMessageBox.ButtonRole.AcceptRole,
        )
        reveal_button = box.addButton(
            self._tr("export.reveal_folder"),
            QMessageBox.ButtonRole.ActionRole,
        )
        box.addButton(QMessageBox.StandardButton.Close)
        box.exec()

        clicked = box.clickedButton()
        if clicked is open_button:
            if not open_local_path(path):
                self._status("status.export_open_failed", 5000, path=path)
            return
        if clicked is reveal_button:
            if not reveal_in_file_manager(path):
                self._status("status.export_reveal_failed", 5000, path=path)

    def _save_project(self) -> None:
        project = self.services.projects.current_project

        if project is None:
            self._status("status.nothing_to_save")
            return

        self._try_save_project()

    def _save_project_as(self) -> None:
        project = self.services.projects.current_project

        if project is None:
            self._status("status.nothing_to_save")
            return

        self._try_save_project_as()

    def _try_save_project(self) -> bool:
        """Save the current project. Return True only on success."""
        project = self.services.projects.current_project
        if project is None:
            return False

        filename = self.services.projects.filename
        if filename is None:
            return self._try_save_project_as()

        try:
            save_project(project, filename)
        except OSError as exc:
            self._report_save_failure(exc)
            return False

        self._after_successful_save(filename)
        return True

    def _try_save_project_as(self) -> bool:
        """Prompt for a path and save. Return True only on success."""
        project = self.services.projects.current_project
        if project is None:
            return False

        path, _selected_filter = QFileDialog.getSaveFileName(
            self,
            self._tr("dialog.save_project"),
            "boardcomposer-project.bcproj",
            self._tr("dialog.filter_bcproj"),
        )

        if not path:
            return False

        try:
            save_project(project, path)
        except OSError as exc:
            self._report_save_failure(exc)
            return False

        self._after_successful_save(path)
        return True

    def _after_successful_save(self, path: str | Path) -> None:
        saved = str(path)
        self.services.projects.mark_saved(saved)
        self._reload_recent_files_menu()
        self.services.recent_files.add(saved)
        self.update_window_title()
        self._emit(events.PROJECT_SAVED, path=saved)
        self._status("status.project_saved", 5000, path=saved)

    def _report_save_failure(self, error: OSError) -> None:
        message = self._tr("status.save_failed", error=error)
        QMessageBox.warning(
            self,
            self._tr("dialog.save_failed_title"),
            message,
        )
        self._status("status.save_failed", 5000, error=error)

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
        self.services.recent_files.prune_missing()
        recent_paths = self.services.recent_files.files
        clear_recent = self._actions.get("clear_recent")
        if clear_recent is not None:
            has_recent = bool(recent_paths)
            clear_recent.setEnabled(has_recent)
            clear_recent.setStatusTip(
                with_native_shortcuts(self._tr("tip.clear_recent"))
                if has_recent
                else self._tr("status.no_recent_to_clear")
            )

        self._recent_menu.clear()
        if hasattr(self, "welcome"):
            self.welcome.set_recent_files(recent_paths)

        if not recent_paths:
            empty_action = QAction(self._tr("action.no_recent"), self)
            empty_action.setEnabled(False)
            self._recent_menu.addAction(empty_action)
            return

        for filename in recent_paths:
            action = QAction(filename, self)
            action.triggered.connect(
                lambda checked=False, path=filename: self._open_recent_project(path)
            )
            self._recent_menu.addAction(action)

        self._recent_menu.addSeparator()
        self._recent_menu.addAction(self._actions["clear_recent"])

    def _clear_recent_files(self) -> None:
        if not self.services.recent_files.files:
            self._status("status.no_recent_to_clear")
            return
        answer = QMessageBox.question(
            self,
            self._tr("dialog.clear_recent_title"),
            self._tr("dialog.clear_recent_body"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        self.services.recent_files.clear()
        self._reload_recent_files_menu()
        self._status("status.recent_cleared")

    def _open_recent_project(self, path: str):
        if not self._confirm_discard_unsaved_changes():
            return

        try:
            project = load_project(path)
        except (UnsupportedProjectVersionError, OSError) as error:
            self.services.recent_files.remove(path)
            self._reload_recent_files_menu()
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

        from studio.unsaved_changes import unsaved_changes_message

        project = self.services.projects.current_project
        project_name = project.name if project is not None else ""
        body = unsaved_changes_message(
            project_name,
            self.services.projects.filename,
            language=self._ui_language(),
        )

        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Warning)
        box.setWindowTitle(self._tr("dialog.unsaved_title"))
        box.setText(body)
        save_button = box.addButton(
            self._tr("dialog.unsaved_save"),
            QMessageBox.ButtonRole.AcceptRole,
        )
        discard_button = box.addButton(
            self._tr("dialog.unsaved_discard"),
            QMessageBox.ButtonRole.DestructiveRole,
        )
        cancel_button = box.addButton(
            self._tr("dialog.unsaved_cancel"),
            QMessageBox.ButtonRole.RejectRole,
        )
        box.setDefaultButton(save_button)
        box.exec()

        clicked = box.clickedButton()
        if clicked is cancel_button:
            return False
        if clicked is discard_button:
            return True
        return self._try_save_project()

    def _restore_window_layout(self) -> None:
        """Restore geometry and dock/toolbar state from preferences."""
        prefs = self.services.preferences.current
        if prefs.window_geometry:
            geometry = QByteArray.fromBase64(
                prefs.window_geometry.encode("ascii", errors="ignore")
            )
            if not geometry.isEmpty():
                self.restoreGeometry(geometry)
        if prefs.window_state:
            state = QByteArray.fromBase64(
                prefs.window_state.encode("ascii", errors="ignore")
            )
            if not state.isEmpty():
                self.restoreState(state)
        self._ensure_bottom_docks_tabified()

    def _ensure_bottom_docks_tabified(self) -> None:
        """Re-tabify Timeline/Comparator if restoreState left them ungrouped."""
        console = getattr(self, "console_dock", None)
        solutions = getattr(self, "solutions_dock", None)
        if console is None or solutions is None:
            return
        if not _qt_is_valid(console) or not _qt_is_valid(solutions):
            return
        if solutions in self.tabifiedDockWidgets(console):
            return
        if console.isFloating() or solutions.isFloating():
            return
        self.tabifyDockWidget(console, solutions)

    def _reset_window_layout(self) -> None:
        """Restore factory dock/toolbar layout and persist it."""
        factory_geometry = getattr(self, "_factory_window_geometry", None)
        factory_state = getattr(self, "_factory_window_state", None)
        if factory_geometry:
            self.restoreGeometry(QByteArray(factory_geometry))
        if factory_state:
            self.restoreState(QByteArray(factory_state))

        self._toolbar.setVisible(True)
        for dock in (
            self.explorer_dock,
            self.inspector_dock,
            self.console_dock,
            self.solutions_dock,
        ):
            dock.setVisible(True)
        self._raise_dock(self.console_dock)

        self._persist_window_layout()
        self._status("status.window_layout_reset")

    def _raise_dock(self, dock: QDockWidget) -> None:
        """Raise a dock tab/window safely (deferred; avoids macOS SIGSEGV).

        Calling ``QWidget.raise_()`` synchronously from a QAction slot while
        QDockWidget is mid-layout update can crash Qt 6.11 on macOS
        (``QDockWidget::event`` / pointer auth failure). Defer to next tick
        and skip destroyed or hidden docks.
        """
        if dock is None:
            return
        QTimer.singleShot(0, lambda d=dock: self._raise_dock_now(d))

    def _raise_dock_now(self, dock: QDockWidget) -> None:
        if not _qt_is_valid(dock) or not dock.isVisible():
            return
        dock.raise_()

    def _persist_window_layout(self) -> None:
        """Save geometry and dock/toolbar state into preferences."""
        prefs = self.services.preferences.current
        geometry = _qbytearray_to_bytes(self.saveGeometry().toBase64()).decode("ascii")
        state = _qbytearray_to_bytes(self.saveState().toBase64()).decode("ascii")
        try:
            self.services.preferences.update(
                dataclass_replace(
                    prefs,
                    window_geometry=geometry,
                    window_state=state,
                )
            )
        except OSError:
            # Prefer closing over failing if preferences.json is unreachable.
            pass

    def _close_event(self, event):
        try:
            if not self._confirm_discard_unsaved_changes():
                event.ignore()
                return
            self._persist_window_layout()
            event.accept()
        except KeyboardInterrupt:
            # Ctrl+C while a modal dialog/persist runs — still quit cleanly.
            try:
                self._persist_window_layout()
            except OSError:
                pass
            event.accept()

    def closeEvent(  # pylint: disable=invalid-name
        self,
        event: QCloseEvent,
    ) -> None:
        """Handle the Qt window close event."""
        self._close_event(event)

    def _on_explorer_context_menu(self, position: QPoint) -> None:
        item = self.explorer.itemAt(position)
        if item is None:
            return
        role = item.data(0, Qt.ItemDataRole.UserRole)
        actions = explorer_context_actions(role)
        if not actions:
            return

        self.explorer.setCurrentItem(item)
        menu = QMenu(self)
        triggered: dict[QAction, str] = {}
        project = self.services.projects.current_project
        for key in actions:
            action = menu.addAction(self._tr(f"explorer.context.{key}"))
            if key == "reveal_folder" and not self.services.projects.filename:
                action.setEnabled(False)
            if key == "place_on_board":
                parsed = parse_explorer_role(role)
                can_place = False
                if (
                    parsed is not None
                    and parsed[0] == "piece"
                    and project is not None
                    and self.workspace.placement_target_board_id() is not None
                ):
                    can_place = project.placement_by_piece_id(parsed[1]) is None
                action.setEnabled(can_place)
            triggered[action] = key
        chosen = menu.exec(self.explorer.viewport().mapToGlobal(position))
        if chosen is None:
            return
        action_key = triggered.get(chosen)
        if action_key is None:
            return
        self._run_explorer_context_action(action_key, role)

    def _run_explorer_context_action(self, action_key: str, role: object) -> None:
        parsed = parse_explorer_role(role)
        if parsed is None:
            return
        kind, object_id = parsed

        if kind == "project" and action_key == "rename":
            self._rename_project()
            return
        if kind == "project" and action_key == "reveal_folder":
            self._reveal_project_folder()
            return
        if action_key == "add_board":
            self._add_board()
            return
        if action_key == "add_piece":
            self._add_piece()
            return
        if action_key == "preview_solution" and kind == "solution":
            try:
                index = int(object_id)
            except ValueError:
                return
            self._select_layout_solution(index)
            return
        if action_key == "copy_id" and kind in {"piece", "board"}:
            self._copy_text_to_clipboard(object_id)
            self._status("status.id_copied", id=object_id)
            return
        if kind == "piece":
            if action_key == "place_on_board":
                # Do not select_piece first: it clears the red highlight even
                # though sticky target remains; place, then select.
                self._place_piece_on_focused_board(object_id)
                return
            self.workspace.select_piece(object_id)
            self.services.selection.select_one(object_id)
            if action_key == "edit":
                self._edit_piece(object_id)
            elif action_key == "rename":
                self._rename_piece(object_id)
            elif action_key == "duplicate":
                self._duplicate_selected_piece()
            elif action_key == "delete":
                self._delete_selected_piece()
            return
        if kind == "board":
            if action_key == "edit":
                self._edit_board(object_id)
            elif action_key == "rename":
                self._rename_board(object_id)
            elif action_key == "duplicate":
                self._duplicate_board(object_id)
            elif action_key == "delete":
                self._delete_board(object_id)

    def _copy_text_to_clipboard(self, text: str) -> None:
        from PySide6.QtWidgets import QApplication

        clipboard = QApplication.clipboard()
        if clipboard is not None:
            clipboard.setText(text)

    def _duplicate_board(self, board_id: str) -> None:
        project = self.services.projects.current_project
        if project is None:
            return
        source = next(
            (board for board in project.boards if board.board_id == board_id),
            None,
        )
        if source is None:
            return

        existing_ids = {board.board_id.casefold() for board in project.boards}
        new_id = allocate_unique_board_id(f"{source.board_id}-copy", existing_ids)
        clone = StudioBoard(
            board_id=new_id,
            length_mm=source.length_mm,
            width_mm=source.width_mm,
            material=source.material,
            thickness_mm=source.thickness_mm,
            quantity=source.quantity,
        )
        command = DuplicateBoardCommand(self.services, clone)
        self.services.commands.execute(command)

        self.workspace.reload_project()
        self._reload_explorer()
        self.select_explorer_board(new_id)
        self._mark_project_modified(reason="board_duplicated")
        self.update_window_title()
        self.update_undo_redo()
        self._status("status.board_duplicated", id=new_id)

    def _reveal_project_folder(self) -> None:
        from studio.file_reveal import reveal_in_file_manager

        filename = self.services.projects.filename
        if not filename:
            self._status("status.project_folder_unavailable")
            return
        if not reveal_in_file_manager(filename):
            self._status("status.project_folder_failed")
            return
        self._status("status.project_folder_opened")

    def _diff_bcproj(self) -> None:
        """Open structural .bcproj diff dialog (FLW-006 / Core ``diff_bcproj``)."""
        project = self.services.projects.current_project
        current = project_to_dict(project) if project is not None else None
        filename = self.services.projects.filename
        start_dir = str(Path(filename).parent) if filename else str(Path.home())
        label = filename or (
            self._tr("diff_bcproj.current_project") if current is not None else None
        )
        dialog = BcprojDiffDialog(
            self,
            language=self._ui_language(),
            current_project=current,
            current_label=label,
            project_path=filename,
            start_dir=start_dir,
        )
        dialog.exec()

    def _rename_selection(self) -> None:
        """Rename the Explorador selection (piece, board, or project) via F2."""
        item = self.explorer.currentItem()
        if item is not None:
            parsed = parse_explorer_role(item.data(0, Qt.ItemDataRole.UserRole))
            if parsed is not None:
                kind, object_id = parsed
                if kind == "project":
                    self._rename_project()
                    return
                if kind == "piece":
                    self._rename_piece(object_id)
                    return
                if kind == "board":
                    self._rename_board(object_id)
                    return

        selected = self.workspace.selection.selected()
        if len(selected) == 1:
            self._rename_piece(selected[0])
            return

        self._status("status.nothing_to_rename_selection")

    def _edit_selection(self) -> None:
        """Edit the selected piece or board (Return / Editar…)."""
        item = self.explorer.currentItem()
        if item is not None:
            parsed = parse_explorer_role(item.data(0, Qt.ItemDataRole.UserRole))
            if parsed is not None:
                kind, object_id = parsed
                if kind == "piece":
                    self._edit_piece(object_id)
                    return
                if kind == "board":
                    self._edit_board(object_id)
                    return

        selected = self.workspace.selection.selected()
        if len(selected) == 1:
            self._edit_piece(selected[0])
            return

        focused = self.workspace.focused_board_id()
        if focused is not None:
            self._edit_board(focused)
            return

        self._status("status.nothing_to_edit_selection")

    def _copy_selection_id(self) -> None:
        """Copy the selected piece or board id to the clipboard."""
        item = self.explorer.currentItem()
        if item is not None:
            parsed = parse_explorer_role(item.data(0, Qt.ItemDataRole.UserRole))
            if parsed is not None:
                kind, object_id = parsed
                if kind in {"piece", "board"}:
                    self._copy_text_to_clipboard(object_id)
                    self._status("status.id_copied", id=object_id)
                    return

        selected = self.workspace.selection.selected()
        if len(selected) == 1:
            self._copy_text_to_clipboard(selected[0])
            self._status("status.id_copied", id=selected[0])
            return

        focused = self.workspace.focused_board_id()
        if focused is not None:
            self._copy_text_to_clipboard(focused)
            self._status("status.id_copied", id=focused)
            return

        self._status("status.nothing_to_copy_id")

    def _rename_project(self) -> None:
        project = self.services.projects.current_project
        if project is None:
            self._status("status.nothing_to_rename")
            return

        name, ok = QInputDialog.getText(
            self,
            self._tr("dialog.rename_project_title"),
            self._tr("form.project_name"),
            text=project.name,
        )
        if not ok:
            return
        cleaned = name.strip()
        if not cleaned:
            QMessageBox.warning(
                self,
                self._tr("dialog.rename_project_title"),
                self._tr("dialog.project_name_required"),
            )
            return
        if cleaned == project.name:
            return

        command = RenameProjectCommand(self.services, project.name, cleaned)
        self.services.commands.execute(command)
        self._mark_project_modified(affects_layout=False, reason="project_renamed")
        self._reload_explorer()
        self.update_window_title()
        self.update_undo_redo()
        self._status("status.project_renamed", name=cleaned)

    def _rename_piece(self, piece_id: str) -> None:
        project = self.services.projects.current_project
        if project is None:
            return
        try:
            piece = project.piece_by_id(piece_id)
        except KeyError:
            return

        name, ok = QInputDialog.getText(
            self,
            self._tr("dialog.rename_piece_title"),
            self._tr("form.id"),
            text=piece.piece_id,
        )
        if not ok:
            return
        new_piece_id = name.strip()
        if not new_piece_id:
            self._status("status.piece_id_empty")
            return
        if new_piece_id == piece_id:
            return
        if any(
            existing.piece_id != piece_id
            and existing.piece_id.strip().casefold() == new_piece_id.casefold()
            for existing in project.pieces
        ):
            self._status("status.piece_id_exists", id=new_piece_id)
            return

        updated = StudioPiece(
            piece_id=new_piece_id,
            length_mm=piece.length_mm,
            width_mm=piece.width_mm,
            material=piece.material,
            thickness_mm=piece.thickness_mm,
        )
        command = EditPieceCommand(self.services, piece, updated)
        self.services.commands.execute(command)

        self._mark_project_modified(reason="piece_renamed")
        self.workspace.reload_project()
        self._reload_explorer()
        self._reload_solution_table()
        self.services.selection.select_one(new_piece_id)
        self.workspace.select_piece(new_piece_id)
        self.refresh_inspector_for_piece(new_piece_id)
        self.update_window_title()
        self.update_undo_redo()
        self._status("status.piece_renamed", id=new_piece_id)

    def _rename_board(self, board_id: str) -> None:
        project = self.services.projects.current_project
        if project is None:
            return
        board = next(
            (
                candidate
                for candidate in project.boards
                if candidate.board_id == board_id
            ),
            None,
        )
        if board is None:
            return

        name, ok = QInputDialog.getText(
            self,
            self._tr("dialog.rename_board_title"),
            self._tr("form.id"),
            text=board.board_id,
        )
        if not ok:
            return
        new_board_id = name.strip()
        if not new_board_id:
            self._status("status.board_id_empty")
            return
        if new_board_id == board_id:
            return
        if any(
            existing.board_id != board_id
            and existing.board_id.strip().casefold() == new_board_id.casefold()
            for existing in project.boards
        ):
            self._status("status.board_id_exists", id=new_board_id)
            return

        updated = StudioBoard(
            board_id=new_board_id,
            length_mm=board.length_mm,
            width_mm=board.width_mm,
            material=board.material,
            thickness_mm=board.thickness_mm,
            quantity=board.quantity,
        )
        command = EditBoardCommand(self.services, board, updated)
        self.services.commands.execute(command)

        self._mark_project_modified(reason="board_renamed")
        self.workspace.reload_project()
        self._reload_explorer()
        self._reload_solution_table()
        self.select_explorer_board(new_board_id)
        self.update_window_title()
        self.update_undo_redo()
        self._status("status.board_renamed", id=new_board_id)

    def _delete_board(self, board_id: str) -> None:
        project = self.services.projects.current_project
        if project is None:
            return
        if not any(board.board_id == board_id for board in project.boards):
            return

        placed = sum(
            1 for placement in project.placements if placement.board_id == board_id
        )
        if placed:
            answer = QMessageBox.question(
                self,
                self._tr("dialog.delete_board_title"),
                self._tr(
                    "dialog.delete_board_confirm_placements",
                    id=board_id,
                    n=placed,
                ),
            )
        else:
            answer = QMessageBox.question(
                self,
                self._tr("dialog.delete_board_title"),
                self._tr("dialog.delete_board_confirm", id=board_id),
            )
        if answer != QMessageBox.StandardButton.Yes:
            return

        command = DeleteBoardCommand(self.services, board_id)
        self.services.commands.execute(command)

        self.services.layout.clear_solutions()
        self.workspace.reload_project()
        self._reload_explorer()
        self._reload_solution_table()
        self.clear_inspector()
        self._mark_project_modified(reason="board_deleted")
        self._refresh_solutions_outdated_banner()
        self.update_window_title()
        self.update_undo_redo()
        self._status("status.board_deleted", id=board_id)

    def _on_explorer_item_activated(self, item, _column):
        """Double-click or Enter/Return on an Explorador row."""
        data = item.data(0, Qt.ItemDataRole.UserRole)
        parsed = parse_explorer_role(data)
        if parsed is None:
            return
        kind, object_id = parsed

        if kind == "board":
            self._edit_board(object_id)
            return

        if kind == "piece":
            project = self.services.projects.current_project
            if (
                project is not None
                and project.placement_by_piece_id(object_id) is None
                and self.workspace.placement_target_board_id() is not None
            ):
                self._place_piece_on_focused_board(object_id)
                return
            self._edit_piece(object_id)
            return

        if kind == "solution":
            try:
                index = int(object_id)
            except ValueError:
                return
            self._select_layout_solution(index)

    def _place_piece_on_focused_board(self, piece_id: str) -> None:
        """Place an unplaced piece on the Explorador-focused board panel."""
        project = self.services.projects.current_project
        if project is None:
            return

        if project.placement_by_piece_id(piece_id) is not None:
            self._status("status.piece_already_placed", id=piece_id)
            return

        board_id = self.workspace.placement_target_board_id()
        if board_id is None:
            self._status("status.place_needs_board_focus")
            return

        try:
            piece = project.piece_by_id(piece_id)
        except KeyError:
            return

        board = next((b for b in project.boards if b.board_id == board_id), None)
        if board is None:
            return

        reason = incompatibility_reason(piece, board)
        if reason is not None:
            self._status(
                f"status.place_incompatible_{reason}",
                piece=piece_id,
                board=board_id,
                piece_thickness=self._format_length(piece.thickness_mm),
                board_thickness=self._format_length(board.thickness_mm),
                piece_material=piece.material,
                board_material=board.material,
            )
            return

        stock_panel_index = next(
            (
                index
                for index, candidate in enumerate(project.boards)
                if candidate.board_id == board_id
            ),
            None,
        )
        if stock_panel_index is None:
            return

        x_mm, y_mm, fits = self._find_free_piece_position_on_panel(
            board,
            piece.length_mm,
            piece.width_mm,
            board_id=board_id,
            board_instance=0,
            stock_panel_index=stock_panel_index,
        )
        if not fits:
            self._status(
                "status.place_no_space",
                piece=piece_id,
                board=board_id,
            )
            return

        placement = StudioPlacement(
            piece_id=piece_id,
            x_mm=x_mm,
            y_mm=y_mm,
            rotated=False,
            rotation=0,
            board_id=board_id,
            board_instance=0,
            stock_panel_index=stock_panel_index,
        )
        self.services.commands.execute(PlacePieceCommand(self.services, placement))
        self.workspace.reload_project()
        self._reload_explorer()
        self.workspace.focus_board(board_id)
        self.workspace.select_piece(piece_id)
        self.refresh_inspector_for_piece(piece_id)
        self._mark_project_modified(reason="piece_placed")
        self.update_window_title()
        self.update_undo_redo()
        self._status("status.piece_placed", piece=piece_id, board=board_id)

    def _find_free_piece_position_on_panel(
        self,
        board: StudioBoard,
        length_mm: float,
        width_mm: float,
        *,
        board_id: str,
        board_instance: int,
        stock_panel_index: int,
        extra_placements: list[StudioPlacement] | None = None,
        piece_lookup: dict[str, StudioPiece] | None = None,
    ) -> tuple[float, float, bool]:
        """Return ``(x, y, fits)`` for a free slot on one physical panel."""
        project = self.services.projects.current_project
        if project is None:
            return 0.0, 0.0, False

        margin = 20.0
        if (
            length_mm + 2 * margin > board.length_mm
            or width_mm + 2 * margin > board.width_mm
        ):
            # Try without margins if piece is large but still fits the panel.
            if length_mm > board.length_mm or width_mm > board.width_mm:
                return 0.0, 0.0, False
            margin = 0.0

        known_pieces = piece_lookup or {}

        def _piece_for(piece_id: str) -> StudioPiece | None:
            piece = known_pieces.get(piece_id)
            if piece is not None:
                return piece
            try:
                return project.piece_by_id(piece_id)
            except KeyError:
                return None

        occupied: list[tuple[float, float, float, float]] = []
        for placement in (*project.placements, *(extra_placements or ())):
            same_panel = (
                placement.board_id == board_id
                and placement.board_instance == board_instance
                and placement.stock_panel_index == stock_panel_index
            )
            if not same_panel:
                continue
            other = _piece_for(placement.piece_id)
            if other is None:
                continue
            placed_w = (
                other.width_mm if placement.rotation in (90, 270) else other.length_mm
            )
            placed_h = (
                other.length_mm if placement.rotation in (90, 270) else other.width_mm
            )
            occupied.append((placement.x_mm, placement.y_mm, placed_w, placed_h))

        def _overlaps(x: float, y: float) -> bool:
            for ox, oy, ow, oh in occupied:
                if not (
                    x + length_mm <= ox
                    or ox + ow <= x
                    or y + width_mm <= oy
                    or oy + oh <= y
                ):
                    return True
            return False

        step = max(10.0, margin)
        y = margin
        while y + width_mm <= board.width_mm - margin + 1e-6:
            x = margin
            while x + length_mm <= board.length_mm - margin + 1e-6:
                if not _overlaps(x, y):
                    return x, y, True
                x += step
            y += step

        # Last chance: origin if empty and fits.
        if not occupied and length_mm <= board.length_mm and width_mm <= board.width_mm:
            return 0.0, 0.0, True
        return 0.0, 0.0, False

    def _find_free_piece_position(
        self,
        length_mm: float,
        width_mm: float,
        *,
        extra_placements: list[StudioPlacement] | None = None,
        piece_lookup: dict[str, StudioPiece] | None = None,
    ) -> tuple[float, float]:
        project = self.services.projects.current_project

        if project is None or not project.boards:
            return 0.0, 0.0

        board = project.boards[0]
        x, y, _fits = self._find_free_piece_position_on_panel(
            board,
            length_mm,
            width_mm,
            board_id=board.board_id,
            board_instance=0,
            stock_panel_index=0,
            extra_placements=extra_placements,
            piece_lookup=piece_lookup,
        )
        return x, y

    def _refresh_explorer_solution_markers(self) -> None:
        """Update ✓ markers without rebuilding the tree.

        A full ``_reload_explorer`` mid double-click deletes the
        ``QTreeWidgetItem`` and drops ``itemDoubleClicked``/``itemActivated``.
        """
        selected = self.services.layout.selected_solution_index
        for index, solution in enumerate(self.services.layout.solutions):
            item = self._find_explorer_item_by_role(f"solution:{index}")
            if item is None:
                continue
            prefix = "✓ " if index == selected else ""
            item.setText(
                0,
                f"{prefix}"
                + self._tr(
                    "explorer.solution",
                    n=index + 1,
                    pieces=len(solution.placements),
                    waste=f"{solution.waste_ratio:.1%}",
                ),
            )
        selected_item = self._find_explorer_item_by_role(f"solution:{selected}")
        if selected_item is None:
            return
        blocked = self.explorer.blockSignals(True)
        try:
            self.explorer.setCurrentItem(selected_item)
            self.explorer.scrollToItem(selected_item)
        finally:
            self.explorer.blockSignals(blocked)

    def _select_layout_solution(self, index: int) -> None:
        solution = self.services.layout.select_solution(index)

        if solution is None:
            return

        self.workspace.preview_solution(solution)
        self._show_layout_solution(solution)
        self._refresh_explorer_solution_markers()
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

        updated_board = StudioBoard(
            board_id=new_board_id,
            length_mm=data["length_mm"],
            width_mm=data["width_mm"],
            material=data["material"],
            thickness_mm=data["thickness_mm"],
            quantity=data["quantity"],
        )
        if updated_board == board:
            return

        command = EditBoardCommand(self.services, board, updated_board)
        self.services.commands.execute(command)

        self._mark_project_modified(reason="board_edited")

        self.workspace.reload_project()
        self._reload_explorer()
        self._reload_solution_table()
        self.update_window_title()
        self.update_undo_redo()

        if not self.services.layout.solutions_outdated:
            self._status("status.board_updated")

    def _edit_piece(self, piece_id: str) -> None:
        project = self.services.projects.current_project
        if project is None:
            return

        piece = project.piece_by_id(piece_id)

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

        updated_piece = StudioPiece(
            piece_id=new_piece_id,
            length_mm=data["length_mm"],
            width_mm=data["width_mm"],
            material=data["material"],
            thickness_mm=data["thickness_mm"],
        )
        if updated_piece == piece:
            return

        command = EditPieceCommand(self.services, piece, updated_piece)
        self.services.commands.execute(command)

        self._mark_project_modified(reason="piece_edited")

        self.workspace.reload_project()
        self._reload_explorer()
        self._reload_solution_table()

        self.services.selection.select_one(new_piece_id)
        self.workspace.select_piece(new_piece_id)
        self.refresh_inspector_for_piece(new_piece_id)

        self.update_window_title()
        self.update_undo_redo()
        if not self.services.layout.solutions_outdated:
            self._status("status.piece_updated")
