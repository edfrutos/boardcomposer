"""Welcome / home screen for BoardComposer Studio (SCR-001)."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from studio.i18n import DEFAULT_LANGUAGE, tr
from studio.project_thumbnail import RECENT_THUMBNAIL_SIZE, project_file_thumbnail

STUDIO_VERSION = "0.4.0.dev0"


class WelcomeScreen(QWidget):
    """Landing page with primary actions and recent projects."""

    new_project_requested = Signal()
    open_project_requested = Signal()
    open_recent_requested = Signal(str)
    import_pieces_requested = Signal()
    preferences_requested = Signal()
    demo_project_requested = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("welcomeRoot")

        self._language = DEFAULT_LANGUAGE
        self._recent_paths: list[str] = []
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

        self.new_button = QPushButton()
        self.new_button.setObjectName("primaryButton")
        self.new_button.setMinimumHeight(44)
        self.new_button.setMinimumWidth(140)
        self.new_button.clicked.connect(self.new_project_requested.emit)
        actions.addWidget(self.new_button)

        self.open_button = QPushButton()
        self.open_button.setMinimumHeight(44)
        self.open_button.clicked.connect(self.open_project_requested.emit)
        actions.addWidget(self.open_button)

        self.import_button = QPushButton()
        self.import_button.setMinimumHeight(44)
        self.import_button.clicked.connect(self.import_pieces_requested.emit)
        actions.addWidget(self.import_button)

        actions.addStretch(1)
        hero.addLayout(actions)

        hero.addSpacing(20)

        secondary = QHBoxLayout()
        secondary.setSpacing(10)
        self.demo_button = QPushButton()
        self.demo_button.clicked.connect(self.demo_project_requested.emit)
        secondary.addWidget(self.demo_button)

        self.preferences_button = QPushButton()
        self.preferences_button.clicked.connect(self.preferences_requested.emit)
        secondary.addWidget(self.preferences_button)
        secondary.addStretch(1)
        hero.addLayout(secondary)

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

        self.recent_label = QLabel()
        self.recent_label.setObjectName("welcomeRecentLabel")
        recent_col.addWidget(self.recent_label)

        self.recent_list = QListWidget()
        self.recent_list.setObjectName("welcomeRecentList")
        self.recent_list.setMinimumWidth(280)
        self.recent_list.setMinimumHeight(280)
        self.recent_list.setIconSize(RECENT_THUMBNAIL_SIZE)
        self.recent_list.setSpacing(6)
        self.recent_list.itemActivated.connect(self._on_recent_activated)
        self.recent_list.itemDoubleClicked.connect(self._on_recent_activated)
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
        self.demo_button.setText(tr("welcome.demo", language))
        self.preferences_button.setText(tr("welcome.preferences", language))
        self.set_recent_files(self._recent_paths)

    def set_recent_files(self, paths: list[str]) -> None:
        """Populate the recent-projects list with name, date and thumbnail."""
        self._recent_paths = list(paths)
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

            lines = [path_obj.name]
            if date_str:
                lines.append(date_str)
            lines.append(path)
            item = QListWidgetItem("\n".join(lines))
            item.setData(Qt.ItemDataRole.UserRole, path)

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

    def _on_recent_activated(self, item: QListWidgetItem) -> None:
        path = item.data(Qt.ItemDataRole.UserRole)
        if path:
            self.open_recent_requested.emit(str(path))
