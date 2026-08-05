"""Welcome / home screen for BoardComposer Studio (SCR-001)."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from studio.dialogs.dialog_chrome import (
    polish_primary_button,
    polish_secondary_button,
)
from studio.i18n import DEFAULT_LANGUAGE, tr
from studio.keyboard_shortcuts import with_native_shortcuts
from studio.project_thumbnail import RECENT_THUMBNAIL_SIZE, project_file_thumbnail
from studio.version import STUDIO_VERSION


class WelcomeScreen(QWidget):
    """Landing page with primary actions and recent projects."""

    new_project_requested = Signal()
    open_project_requested = Signal()
    open_recent_requested = Signal(str)
    remove_recent_requested = Signal(str)
    pin_recent_requested = Signal(str)
    reveal_recent_requested = Signal(str)
    clear_recent_requested = Signal()
    import_pieces_requested = Signal()
    preferences_requested = Signal()
    demo_project_requested = Signal()
    from_template_requested = Signal()
    docs_requested = Signal()
    whats_new_requested = Signal()
    shortcuts_requested = Signal()
    about_requested = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("welcomeRoot")

        self._language = DEFAULT_LANGUAGE
        self._recent_paths: list[str] = []
        self._pinned_paths: set[str] = set()
        self._has_templates = False
        self._thumbnail_cache: dict[tuple[str, float], QIcon] = {}

        root = QHBoxLayout(self)
        root.setContentsMargins(56, 48, 56, 48)
        root.setSpacing(48)

        hero = QVBoxLayout()
        hero.setSpacing(12)
        hero.setAlignment(Qt.AlignmentFlag.AlignTop)

        brand = QLabel("BoardComposer")
        brand.setObjectName("welcomeBrand")
        brand.setWordWrap(True)
        hero.addWidget(brand)

        self.subtitle = QLabel(f"Studio {STUDIO_VERSION}")
        self.subtitle.setObjectName("welcomeSubtitle")
        hero.addWidget(self.subtitle)

        self.tagline = QLabel()
        self.tagline.setObjectName("welcomeTagline")
        self.tagline.setWordWrap(True)
        hero.addWidget(self.tagline)

        hero.addSpacing(16)

        actions = QHBoxLayout()
        actions.setSpacing(10)

        self.new_button = polish_primary_button(QPushButton())
        self.new_button.setMinimumWidth(140)
        self.new_button.clicked.connect(self.new_project_requested.emit)
        actions.addWidget(self.new_button)

        self.open_button = polish_secondary_button(QPushButton(), min_height=44)
        self.open_button.clicked.connect(self.open_project_requested.emit)
        actions.addWidget(self.open_button)

        self.import_button = polish_secondary_button(QPushButton(), min_height=44)
        self.import_button.clicked.connect(self.import_pieces_requested.emit)
        actions.addWidget(self.import_button)

        actions.addStretch(1)
        hero.addLayout(actions)

        hero.addSpacing(20)

        secondary = QHBoxLayout()
        secondary.setSpacing(10)
        self.demo_button = polish_secondary_button(QPushButton())
        self.demo_button.clicked.connect(self.demo_project_requested.emit)
        secondary.addWidget(self.demo_button)

        self.template_button = polish_secondary_button(QPushButton())
        self.template_button.clicked.connect(self.from_template_requested.emit)
        secondary.addWidget(self.template_button)

        self.docs_button = polish_secondary_button(QPushButton())
        self.docs_button.clicked.connect(self.docs_requested.emit)
        secondary.addWidget(self.docs_button)

        self.whats_new_button = polish_secondary_button(QPushButton())
        self.whats_new_button.clicked.connect(self.whats_new_requested.emit)
        secondary.addWidget(self.whats_new_button)

        self.preferences_button = polish_secondary_button(QPushButton())
        self.preferences_button.clicked.connect(self.preferences_requested.emit)
        secondary.addWidget(self.preferences_button)
        secondary.addStretch(1)
        hero.addLayout(secondary)

        hero.addSpacing(12)

        help_row = QHBoxLayout()
        help_row.setSpacing(10)
        self.shortcuts_button = polish_secondary_button(QPushButton())
        self.shortcuts_button.clicked.connect(self.shortcuts_requested.emit)
        help_row.addWidget(self.shortcuts_button)

        self.about_button = polish_secondary_button(QPushButton())
        self.about_button.clicked.connect(self.about_requested.emit)
        help_row.addWidget(self.about_button)
        help_row.addStretch(1)
        hero.addLayout(help_row)

        hero.addStretch(1)

        hero_wrap = QWidget()
        hero_wrap.setLayout(hero)
        hero_wrap.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        root.addWidget(hero_wrap, stretch=3)

        recent_col = QVBoxLayout()
        recent_col.setSpacing(10)
        recent_col.setAlignment(Qt.AlignmentFlag.AlignTop)

        recent_header = QHBoxLayout()
        recent_header.setSpacing(8)
        self.recent_label = QLabel()
        self.recent_label.setObjectName("welcomeRecentLabel")
        recent_header.addWidget(self.recent_label, stretch=1)
        self.clear_recent_button = polish_secondary_button(QPushButton(), min_height=32)
        self.clear_recent_button.setObjectName("welcomeClearRecent")
        self.clear_recent_button.setFlat(True)
        self.clear_recent_button.clicked.connect(self.clear_recent_requested.emit)
        recent_header.addWidget(self.clear_recent_button)
        recent_col.addLayout(recent_header)

        self.recent_list = QListWidget()
        self.recent_list.setObjectName("welcomeRecentList")
        self.recent_list.setMinimumWidth(280)
        self.recent_list.setMinimumHeight(280)
        self.recent_list.setIconSize(RECENT_THUMBNAIL_SIZE)
        self.recent_list.setSpacing(6)
        self.recent_list.itemActivated.connect(self._on_recent_activated)
        self.recent_list.itemPressed.connect(self._on_recent_item_pressed)
        self.recent_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.recent_list.customContextMenuRequested.connect(
            self._on_recent_context_menu
        )
        for sequence in (QKeySequence.StandardKey.Delete, QKeySequence("Backspace")):
            shortcut = QShortcut(sequence, self.recent_list)
            shortcut.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
            shortcut.activated.connect(self._remove_selected_recent)
        recent_col.addWidget(self.recent_list, stretch=1)

        recent_wrap = QWidget()
        recent_wrap.setLayout(recent_col)
        recent_wrap.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )
        root.addWidget(recent_wrap, stretch=2)

        self.apply_language(DEFAULT_LANGUAGE)

    def apply_language(self, language: str) -> None:
        """Refresh visible strings for the selected language."""
        self._language = language
        self.tagline.setText(tr("welcome.tagline", language))
        self.new_button.setText(tr("welcome.new", language))
        self.open_button.setText(tr("welcome.open", language))
        self.import_button.setText(tr("welcome.import", language))
        self.recent_label.setText(tr("welcome.recent", language))
        self.clear_recent_button.setText(tr("welcome.clear_recent", language))
        self.demo_button.setText(tr("welcome.demo", language))
        self.template_button.setText(tr("welcome.from_template", language))
        self.docs_button.setText(tr("welcome.docs", language))
        self.whats_new_button.setText(tr("welcome.whats_new", language))
        self.preferences_button.setText(tr("welcome.preferences", language))
        self.shortcuts_button.setText(tr("welcome.shortcuts", language))
        self.about_button.setText(tr("welcome.about", language))
        tip_pairs = (
            (self.new_button, "tip.new_project"),
            (self.open_button, "tip.open"),
            (self.import_button, "tip.import_pieces_csv"),
            (self.demo_button, "tip.new_demo_project"),
            (self.docs_button, "tip.open_docs"),
            (self.whats_new_button, "tip.whats_new"),
            (self.preferences_button, "tip.preferences"),
            (self.shortcuts_button, "tip.shortcuts"),
            (self.about_button, "tip.about"),
        )
        for button, tip_key in tip_pairs:
            tip = with_native_shortcuts(tr(tip_key, language))
            button.setToolTip(tip)
            button.setStatusTip(tip)
        self.set_recent_files(self._recent_paths, pinned=sorted(self._pinned_paths))
        self.set_has_templates(self._has_templates)

    def set_has_templates(self, has_templates: bool) -> None:
        """Enable or disable the from-template button with an honest tip."""
        self._has_templates = has_templates
        self.template_button.setEnabled(has_templates)
        tip = (
            with_native_shortcuts(tr("tip.new_from_template", self._language))
            if has_templates
            else tr("status.template_empty", self._language)
        )
        self.template_button.setToolTip(tip)
        self.template_button.setStatusTip(tip)

    def set_recent_files(
        self, paths: list[str], *, pinned: list[str] | None = None
    ) -> None:
        """Populate the recent-projects list with name, date and thumbnail."""
        self._recent_paths = list(paths)
        self._pinned_paths = set(pinned or ())
        has_recent = bool(paths)
        self.clear_recent_button.setEnabled(has_recent)
        clear_tip = (
            with_native_shortcuts(tr("tip.clear_recent", self._language))
            if has_recent
            else tr("welcome.empty_recent", self._language)
        )
        self.clear_recent_button.setToolTip(clear_tip)
        self.clear_recent_button.setStatusTip(clear_tip)
        self.recent_list.clear()
        if not paths:
            empty = QListWidgetItem(tr("welcome.empty_recent", self._language))
            empty.setFlags(Qt.ItemFlag.NoItemFlags)
            self.recent_list.addItem(empty)
            return

        keep_keys = set()
        for path in paths:
            path_obj = Path(path)
            mtime = 0.0
            date_str = ""
            try:
                mtime = path_obj.stat().st_mtime
                date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
            except OSError:
                pass

            name = path_obj.name
            if path in self._pinned_paths:
                name = f"★ {name}"
            lines = [name]
            if date_str:
                lines.append(date_str)
            lines.append(path)
            item = QListWidgetItem("\n".join(lines))
            item.setData(Qt.ItemDataRole.UserRole, path)
            tip = (
                tr("tip.unpin_recent", self._language)
                if path in self._pinned_paths
                else tr("tip.pin_recent", self._language)
            )
            item.setToolTip(with_native_shortcuts(tip))

            cache_key = (path, mtime)
            keep_keys.add(cache_key)
            icon = self._thumbnail_cache.get(cache_key)
            if icon is None:
                pixmap = project_file_thumbnail(path)
                if pixmap is not None and not pixmap.isNull():
                    icon = QIcon(pixmap)
                    self._thumbnail_cache[cache_key] = icon
            if icon is not None:
                item.setIcon(icon)

            self.recent_list.addItem(item)

        stale = [key for key in self._thumbnail_cache if key not in keep_keys]
        for key in stale:
            del self._thumbnail_cache[key]

    def _on_recent_item_pressed(self, item: QListWidgetItem | None) -> None:
        """Open on left press only (right-click is for the context menu)."""
        if QApplication.mouseButtons() != Qt.MouseButton.LeftButton:
            return
        self._on_recent_activated(item)

    def _on_recent_activated(self, item: QListWidgetItem | None) -> None:
        if item is None:
            return
        path = item.data(Qt.ItemDataRole.UserRole)
        if path:
            self.open_recent_requested.emit(str(path))

    def _selected_recent_path(self) -> str | None:
        item = self.recent_list.currentItem()
        if item is None:
            return None
        path = item.data(Qt.ItemDataRole.UserRole)
        return str(path) if path else None

    def _remove_selected_recent(self) -> None:
        path = self._selected_recent_path()
        if path:
            self.remove_recent_requested.emit(path)

    def _on_recent_context_menu(self, position) -> None:
        item = self.recent_list.itemAt(position)
        if item is None:
            return
        path = item.data(Qt.ItemDataRole.UserRole)
        if not path:
            return
        self.recent_list.setCurrentItem(item)
        menu = QMenu(self)
        pin_key = (
            "welcome.unpin_recent"
            if str(path) in self._pinned_paths
            else "welcome.pin_recent"
        )
        tip_key = (
            "tip.unpin_recent" if str(path) in self._pinned_paths else "tip.pin_recent"
        )
        pin_action = menu.addAction(tr(pin_key, self._language))
        pin_tip = with_native_shortcuts(tr(tip_key, self._language))
        pin_action.setToolTip(pin_tip)
        pin_action.setStatusTip(pin_tip)
        reveal_action = menu.addAction(tr("welcome.reveal_folder", self._language))
        reveal_tip = tr("tip.reveal_recent", self._language)
        reveal_action.setToolTip(reveal_tip)
        reveal_action.setStatusTip(reveal_tip)
        menu.addSeparator()
        remove_action = menu.addAction(tr("welcome.remove_recent", self._language))
        remove_tip = with_native_shortcuts(tr("tip.remove_recent", self._language))
        remove_action.setToolTip(remove_tip)
        remove_action.setStatusTip(remove_tip)
        chosen = menu.exec(self.recent_list.mapToGlobal(position))
        if chosen is pin_action:
            self.pin_recent_requested.emit(str(path))
        elif chosen is reveal_action:
            self.reveal_recent_requested.emit(str(path))
        elif chosen is remove_action:
            self.remove_recent_requested.emit(str(path))
