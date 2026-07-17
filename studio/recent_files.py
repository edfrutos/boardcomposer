"""Recent project files manager with optional disk persistence."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


def default_recent_files_path() -> Path:
    return Path.home() / ".boardcomposer" / "recent_files.json"


@dataclass
class RecentFilesManager:
    files: list[str] = field(default_factory=list)
    max_items: int = 10
    path: Path | None = None

    def __post_init__(self) -> None:
        if self.path is None:
            self.path = default_recent_files_path()
        if not self.files:
            self.load()

    def add(self, filename: str) -> None:
        if filename in self.files:
            self.files.remove(filename)

        self.files.insert(0, filename)
        self.files = self.files[: self.max_items]
        self.save()

    def clear(self) -> None:
        self.files.clear()
        self.save()

    def existing_files(self) -> list[str]:
        """Return recent paths that still exist on disk."""
        return [path for path in self.files if Path(path).is_file()]

    def load(self) -> None:
        if self.path is None or not self.path.is_file():
            return
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return
        if not isinstance(payload, list):
            return
        self.files = [str(item) for item in payload if isinstance(item, str)][
            : self.max_items
        ]

    def save(self) -> None:
        if self.path is None:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(self.files, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
