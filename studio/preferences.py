"""User-level Studio preferences (SCR-006), stored outside project files."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path

from boardcomposer.solver.scoring_weights import ScoringWeights
from boardcomposer.solver.strategies import OptimizationStrategy, strategy_by_name
from studio.theme import DEFAULT_THEME, VALID_THEMES
from studio.export_options import (
    DEFAULT_EXPORT_FORMAT,
    VALID_EXPORT_FORMATS,
    ExportOptions,
)
from studio.i18n import DEFAULT_LANGUAGE, VALID_LANGUAGES
from studio.units import DEFAULT_UNITS, VALID_UNITS

DEFAULT_STRATEGY = "material"
VALID_STRATEGIES = ("balanced", "material", "compact", "exact")
DEFAULT_GRID_SIZE_MM = 100
MIN_GRID_SIZE_MM = 10
MAX_GRID_SIZE_MM = 500
DEFAULT_MAX_SOLUTIONS = 20
MIN_MAX_SOLUTIONS = 1
MAX_MAX_SOLUTIONS = 100


@dataclass(frozen=True)
class WeightPreferences:
    material_utilization: float = 60.0
    placed_boards: float = 25.0
    compactness: float = 10.0
    rotation_penalty: float = 5.0

    def to_scoring_weights(self) -> ScoringWeights:
        return ScoringWeights(
            material_utilization=self.material_utilization,
            placed_boards=self.placed_boards,
            compactness=self.compactness,
            rotation_penalty=self.rotation_penalty,
        )

    @classmethod
    def from_scoring_weights(cls, weights: ScoringWeights) -> WeightPreferences:
        return cls(
            material_utilization=weights.material_utilization,
            placed_boards=weights.placed_boards,
            compactness=weights.compactness,
            rotation_penalty=weights.rotation_penalty,
        )


@dataclass
class StudioPreferences:
    """Persisted user preferences for BoardComposer Studio."""

    strategy_name: str = DEFAULT_STRATEGY
    use_custom_weights: bool = False
    weights: WeightPreferences = field(
        default_factory=lambda: WeightPreferences.from_scoring_weights(
            strategy_by_name(DEFAULT_STRATEGY).weights
        )
    )
    theme: str = DEFAULT_THEME
    show_grid: bool = True
    grid_size_mm: int = DEFAULT_GRID_SIZE_MM
    language: str = DEFAULT_LANGUAGE
    units: str = DEFAULT_UNITS
    export_format: str = DEFAULT_EXPORT_FORMAT
    export_include_metrics: bool = True
    export_include_explanation: bool = True
    export_include_offcuts: bool = True
    last_export_directory: str | None = None
    max_solutions: int = DEFAULT_MAX_SOLUTIONS
    window_geometry: str | None = None
    window_state: str | None = None
    timeline_event_filter: str | None = None
    timeline_algorithm_filter: str | None = None
    timeline_period_seconds: int | None = None
    timeline_replay_mode: str = "placements"
    timeline_replay_interval_ms: int = 450

    def resolved_strategy(self) -> OptimizationStrategy:
        """Return the OptimizationStrategy implied by these preferences."""
        name = (
            self.strategy_name
            if self.strategy_name in VALID_STRATEGIES
            else DEFAULT_STRATEGY
        )
        base = strategy_by_name(name)
        if not self.use_custom_weights:
            return base
        return replace(base, weights=self.weights.to_scoring_weights())

    def export_options(self) -> ExportOptions:
        """Return the last-used / default export options."""
        return ExportOptions(
            format=self.export_format,
            include_metrics=self.export_include_metrics,
            include_explanation=self.export_include_explanation,
            include_offcuts=self.export_include_offcuts,
        ).normalized()


def _clamp_grid_size(value: int | float) -> int:
    size = int(value)
    return max(MIN_GRID_SIZE_MM, min(MAX_GRID_SIZE_MM, size))


def _clamp_max_solutions(value: int | float) -> int:
    size = int(value)
    return max(MIN_MAX_SOLUTIONS, min(MAX_MAX_SOLUTIONS, size))


def _optional_base64_string(value: object) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    return value.strip()


def _optional_directory(value: object) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    return value.strip()


def _optional_string(value: object) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    return value.strip()


def _optional_period_seconds(value: object) -> int | None:
    if value is None:
        return None
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed > 0 else None


_VALID_TIMELINE_REPLAY_MODES = frozenset({"placements", "phases"})
_DEFAULT_TIMELINE_REPLAY_MODE = "placements"
_VALID_TIMELINE_REPLAY_INTERVALS = frozenset({200, 450, 900})
_DEFAULT_TIMELINE_REPLAY_INTERVAL_MS = 450


def _timeline_replay_mode(value: object) -> str:
    if isinstance(value, str) and value in _VALID_TIMELINE_REPLAY_MODES:
        return value
    return _DEFAULT_TIMELINE_REPLAY_MODE


def _timeline_replay_interval_ms(value: object) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return _DEFAULT_TIMELINE_REPLAY_INTERVAL_MS
    if parsed in _VALID_TIMELINE_REPLAY_INTERVALS:
        return parsed
    return _DEFAULT_TIMELINE_REPLAY_INTERVAL_MS


def default_preferences_path() -> Path:
    return Path.home() / ".boardcomposer" / "preferences.json"


class PreferencesManager:
    """Load and save `StudioPreferences` from a JSON file."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path or default_preferences_path()
        self.current = self.load()

    def load(self) -> StudioPreferences:
        if not self.path.is_file():
            return StudioPreferences()

        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return StudioPreferences()

        strategy_name = payload.get("strategy_name", DEFAULT_STRATEGY)
        if strategy_name not in VALID_STRATEGIES:
            strategy_name = DEFAULT_STRATEGY

        theme = payload.get("theme", DEFAULT_THEME)
        if theme not in VALID_THEMES:
            theme = DEFAULT_THEME

        language = payload.get("language", DEFAULT_LANGUAGE)
        if language not in VALID_LANGUAGES:
            language = DEFAULT_LANGUAGE

        units = payload.get("units", DEFAULT_UNITS)
        if units not in VALID_UNITS:
            units = DEFAULT_UNITS

        weights_payload = payload.get("weights") or {}
        preset = WeightPreferences.from_scoring_weights(
            strategy_by_name(strategy_name).weights
        )
        weights = WeightPreferences(
            material_utilization=float(
                weights_payload.get("material_utilization", preset.material_utilization)
            ),
            placed_boards=float(
                weights_payload.get("placed_boards", preset.placed_boards)
            ),
            compactness=float(weights_payload.get("compactness", preset.compactness)),
            rotation_penalty=float(
                weights_payload.get("rotation_penalty", preset.rotation_penalty)
            ),
        )

        try:
            grid_size_mm = _clamp_grid_size(
                payload.get("grid_size_mm", DEFAULT_GRID_SIZE_MM)
            )
        except (TypeError, ValueError):
            grid_size_mm = DEFAULT_GRID_SIZE_MM

        try:
            max_solutions = _clamp_max_solutions(
                payload.get("max_solutions", DEFAULT_MAX_SOLUTIONS)
            )
        except (TypeError, ValueError):
            max_solutions = DEFAULT_MAX_SOLUTIONS

        export_format = payload.get("export_format", DEFAULT_EXPORT_FORMAT)
        if export_format not in VALID_EXPORT_FORMATS:
            export_format = DEFAULT_EXPORT_FORMAT

        return StudioPreferences(
            strategy_name=strategy_name,
            use_custom_weights=bool(payload.get("use_custom_weights", False)),
            weights=weights,
            theme=theme,
            show_grid=bool(payload.get("show_grid", True)),
            grid_size_mm=grid_size_mm,
            language=language,
            units=units,
            export_format=export_format,
            export_include_metrics=bool(payload.get("export_include_metrics", True)),
            export_include_explanation=bool(
                payload.get("export_include_explanation", True)
            ),
            export_include_offcuts=bool(payload.get("export_include_offcuts", True)),
            last_export_directory=_optional_directory(
                payload.get("last_export_directory")
            ),
            max_solutions=max_solutions,
            window_geometry=_optional_base64_string(payload.get("window_geometry")),
            window_state=_optional_base64_string(payload.get("window_state")),
            timeline_event_filter=_optional_string(
                payload.get("timeline_event_filter")
            ),
            timeline_algorithm_filter=_optional_string(
                payload.get("timeline_algorithm_filter")
            ),
            timeline_period_seconds=_optional_period_seconds(
                payload.get("timeline_period_seconds")
            ),
            timeline_replay_mode=_timeline_replay_mode(
                payload.get("timeline_replay_mode")
            ),
            timeline_replay_interval_ms=_timeline_replay_interval_ms(
                payload.get("timeline_replay_interval_ms")
            ),
        )

    def save(self, preferences: StudioPreferences | None = None) -> None:
        preferences = preferences or self.current
        self.current = preferences
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "strategy_name": preferences.strategy_name,
            "use_custom_weights": preferences.use_custom_weights,
            "weights": asdict(preferences.weights),
            "theme": preferences.theme,
            "show_grid": preferences.show_grid,
            "grid_size_mm": preferences.grid_size_mm,
            "language": preferences.language,
            "units": preferences.units,
            "export_format": preferences.export_format,
            "export_include_metrics": preferences.export_include_metrics,
            "export_include_explanation": preferences.export_include_explanation,
            "export_include_offcuts": preferences.export_include_offcuts,
            "last_export_directory": preferences.last_export_directory,
            "max_solutions": preferences.max_solutions,
            "window_geometry": preferences.window_geometry,
            "window_state": preferences.window_state,
            "timeline_event_filter": preferences.timeline_event_filter,
            "timeline_algorithm_filter": preferences.timeline_algorithm_filter,
            "timeline_period_seconds": preferences.timeline_period_seconds,
            "timeline_replay_mode": preferences.timeline_replay_mode,
            "timeline_replay_interval_ms": preferences.timeline_replay_interval_ms,
        }
        self.path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def update(self, preferences: StudioPreferences) -> None:
        self.save(preferences)
