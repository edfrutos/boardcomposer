"""Recent project files manager."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RecentFilesManager:
    files: list[str] = field(default_factory=list)
    max_items: int = 10

    def add(self, filename: str) -> None:
        if filename in self.files:
            self.files.remove(filename)

        self.files.insert(0, filename)
        self.files = self.files[: self.max_items]

    def clear(self) -> None:
        self.files.clear()
