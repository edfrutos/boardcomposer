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
    pinned: list[str] = field(default_factory=list)
    max_items: int = 10
    path: Path | None = None

    def __post_init__(self) -> None:
        if self.path is None:
            self.path = default_recent_files_path()
        if not self.files:
            self.load()

    def is_pinned(self, filename: str) -> bool:
        return filename in self.pinned

    def ordered_files(self) -> list[str]:
        """Pinned (stable order) first, then unpinned in MRU order."""
        pinned_set = set(self.pinned)
        pinned_order = [path for path in self.pinned if path in self.files]
        unpinned = [path for path in self.files if path not in pinned_set]
        return pinned_order + unpinned

    def existing_ordered_files(self) -> list[str]:
        """Ordered recent paths that still exist on disk."""
        existing = set(self.existing_files())
        return [path for path in self.ordered_files() if path in existing]

    def add(self, filename: str) -> None:
        if filename in self.files:
            self.files.remove(filename)

        self.files.insert(0, filename)
        self._trim()
        self.save()

    def clear(self) -> None:
        self.files.clear()
        self.pinned.clear()
        self.save()

    def remove(self, filename: str) -> bool:
        """Remove one path from the list. Returns True if it was present."""
        if filename not in self.files:
            return False
        self.files.remove(filename)
        if filename in self.pinned:
            self.pinned.remove(filename)
        self.save()
        return True

    def toggle_pin(self, filename: str) -> bool:
        """Toggle pin. Returns True if pinned after the call."""
        if filename not in self.files:
            return False
        if filename in self.pinned:
            self.pinned.remove(filename)
            self.save()
            return False
        self.pinned.append(filename)
        self.save()
        return True

    def existing_files(self) -> list[str]:
        """Return recent paths that still exist on disk."""
        return [path for path in self.files if Path(path).is_file()]

    def prune_missing(self) -> int:
        """Drop paths that no longer exist on disk. Returns how many were removed."""
        kept = self.existing_files()
        removed = len(self.files) - len(kept)
        if removed:
            kept_set = set(kept)
            self.files = kept
            self.pinned = [path for path in self.pinned if path in kept_set]
            self.save()
        return removed

    def _trim(self) -> None:
        while len(self.files) > self.max_items:
            dropped = False
            for index in range(len(self.files) - 1, -1, -1):
                if self.files[index] not in self.pinned:
                    self.files.pop(index)
                    dropped = True
                    break
            if dropped:
                continue
            # Only pinned remain over the cap: drop oldest MRU entry.
            path = self.files.pop()
            if path in self.pinned:
                self.pinned.remove(path)

    def load(self) -> None:
        if self.path is None or not self.path.is_file():
            return
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return
        if isinstance(payload, list):
            self.files = [str(item) for item in payload if isinstance(item, str)][
                : self.max_items
            ]
            self.pinned = []
            return
        if not isinstance(payload, dict):
            return
        files = payload.get("files")
        if not isinstance(files, list):
            return
        self.files = [str(item) for item in files if isinstance(item, str)][
            : self.max_items
        ]
        pinned_raw = payload.get("pinned", [])
        if not isinstance(pinned_raw, list):
            pinned_raw = []
        files_set = set(self.files)
        self.pinned = [
            str(item)
            for item in pinned_raw
            if isinstance(item, str) and item in files_set
        ]

    def save(self) -> None:
        if self.path is None:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"files": self.files, "pinned": self.pinned}
        self.path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
