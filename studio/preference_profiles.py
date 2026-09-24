"""Named local shop-preference profiles (IDE-0054). No cloud sync."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from studio.preferences import (
    StudioPreferences,
    _LOCAL_PREF_KEYS,
    portable_preferences_payload,
    preferences_from_payload,
    preferences_payload,
)


def default_preference_profiles_path() -> Path:
    return Path.home() / ".boardcomposer" / "preference_profiles.json"


def preferences_from_profile(
    current: StudioPreferences,
    portable: dict,
) -> StudioPreferences:
    """Replace shop settings; keep local folders and window geometry."""
    base = preferences_payload(StudioPreferences())
    base.update(portable)
    current_payload = preferences_payload(current)
    for key in _LOCAL_PREF_KEYS:
        base[key] = current_payload.get(key)
    return preferences_from_payload(base)


@dataclass
class PreferenceProfile:
    name: str
    preferences: dict

    @property
    def key(self) -> str:
        return self.name.casefold()


@dataclass
class PreferenceProfilesManager:
    """Load and save named preference profiles from a local JSON file."""

    profiles: list[PreferenceProfile] = field(default_factory=list)
    path: Path | None = None
    autoload: bool = True

    def __post_init__(self) -> None:
        if self.path is None and self.autoload:
            self.path = default_preference_profiles_path()
        if self.autoload and not self.profiles:
            self.load()

    def names(self) -> list[str]:
        return [profile.name for profile in self.profiles]

    def get(self, name: str) -> PreferenceProfile | None:
        wanted = name.strip().casefold()
        for profile in self.profiles:
            if profile.key == wanted:
                return profile
        return None

    def save_profile(
        self,
        name: str,
        preferences: StudioPreferences,
    ) -> PreferenceProfile:
        """Insert or replace a profile by name and persist."""
        cleaned = name.strip()
        if not cleaned:
            raise ValueError("El nombre del perfil no puede estar vacío")
        profile = PreferenceProfile(
            name=cleaned,
            preferences=portable_preferences_payload(preferences),
        )
        self.profiles = [
            existing for existing in self.profiles if existing.key != profile.key
        ]
        self.profiles.append(profile)
        self.profiles.sort(key=lambda item: item.name.casefold())
        self.save()
        return profile

    def delete(self, name: str) -> bool:
        wanted = name.strip().casefold()
        before = len(self.profiles)
        self.profiles = [profile for profile in self.profiles if profile.key != wanted]
        if len(self.profiles) == before:
            return False
        self.save()
        return True

    def load(self) -> None:
        if self.path is None or not self.path.is_file():
            return
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return
        entries = raw.get("profiles") if isinstance(raw, dict) else None
        if not isinstance(entries, list):
            return
        loaded: list[PreferenceProfile] = []
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            name = str(entry.get("name", "")).strip()
            prefs = entry.get("preferences")
            if not name or not isinstance(prefs, dict):
                continue
            loaded.append(PreferenceProfile(name=name, preferences=prefs))
        loaded.sort(key=lambda item: item.name.casefold())
        self.profiles = loaded

    def save(self) -> None:
        if self.path is None:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "profiles": [
                {"name": profile.name, "preferences": profile.preferences}
                for profile in self.profiles
            ]
        }
        self.path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
