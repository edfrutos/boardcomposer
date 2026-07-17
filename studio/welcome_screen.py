"""Welcome / home screen for BoardComposer Studio (SCR-001)."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

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

        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 40, 48, 40)
        layout.setSpacing(20)

        brand = QLabel("BoardComposer")
        brand.setObjectName("welcomeBrand")
        brand.setStyleSheet(
            "QLabel#welcomeBrand { font-size: 36px; font-weight: 700; }"
        )
        layout.addWidget(brand)

        subtitle = QLabel(f"Studio {STUDIO_VERSION}")
        subtitle.setStyleSheet("font-size: 14px; opacity: 0.7;")
        layout.addWidget(subtitle)

        tagline = QLabel(
            "Optimiza el corte de tableros. Crea un proyecto, abre uno reciente "
            "o importa piezas para empezar."
        )
        tagline.setWordWrap(True)
        tagline.setStyleSheet("font-size: 15px; margin-top: 8px;")
        layout.addWidget(tagline)

        actions = QHBoxLayout()
        actions.setSpacing(12)

        self.new_button = QPushButton("Nuevo proyecto")
        self.new_button.setMinimumHeight(40)
        self.new_button.clicked.connect(self.new_project_requested.emit)
        actions.addWidget(self.new_button)

        self.open_button = QPushButton("Abrir proyecto…")
        self.open_button.setMinimumHeight(40)
        self.open_button.clicked.connect(self.open_project_requested.emit)
        actions.addWidget(self.open_button)

        self.import_button = QPushButton("Importar piezas (CSV/Excel)…")
        self.import_button.setMinimumHeight(40)
        self.import_button.clicked.connect(self.import_pieces_requested.emit)
        actions.addWidget(self.import_button)

        actions.addStretch(1)
        layout.addLayout(actions)

        layout.addWidget(QLabel("Proyectos recientes"))
        self.recent_list = QListWidget()
        self.recent_list.setMinimumHeight(180)
        self.recent_list.itemActivated.connect(self._on_recent_activated)
        self.recent_list.itemDoubleClicked.connect(self._on_recent_activated)
        layout.addWidget(self.recent_list)

        secondary = QHBoxLayout()
        self.demo_button = QPushButton("Proyecto de ejemplo")
        self.demo_button.clicked.connect(self.demo_project_requested.emit)
        secondary.addWidget(self.demo_button)

        self.preferences_button = QPushButton("Preferencias…")
        self.preferences_button.clicked.connect(self.preferences_requested.emit)
        secondary.addWidget(self.preferences_button)
        secondary.addStretch(1)
        layout.addLayout(secondary)

        layout.addStretch(1)

    def set_recent_files(self, paths: list[str]) -> None:
        """Populate the recent-projects list."""
        self.recent_list.clear()
        if not paths:
            empty = QListWidgetItem("Sin proyectos recientes")
            empty.setFlags(Qt.ItemFlag.NoItemFlags)
            self.recent_list.addItem(empty)
            return

        for path in paths:
            path_obj = Path(path)
            item = QListWidgetItem(f"{path_obj.name}\n{path}")
            item.setData(Qt.ItemDataRole.UserRole, path)
            self.recent_list.addItem(item)

    def _on_recent_activated(self, item: QListWidgetItem) -> None:
        path = item.data(Qt.ItemDataRole.UserRole)
        if path:
            self.open_recent_requested.emit(str(path))
