"""User-level Studio preferences (SCR-006), stored outside project files."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path

from boardcomposer.solver.scoring_weights import ScoringWeights
from boardcomposer.solver.strategies import OptimizationStrategy, strategy_by_name
from studio.theme import DEFAULT_THEME, VALID_THEMES

DEFAULT_STRATEGY = "material"
VALID_STRATEGIES = ("balanced", "material", "compact", "exact")
DEFAULT_GRID_SIZE_MM = 100
MIN_GRID_SIZE_MM = 10
MAX_GRID_SIZE_MM = 500


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


def _clamp_grid_size(value: int | float) -> int:
    size = int(value)
    return max(MIN_GRID_SIZE_MM, min(MAX_GRID_SIZE_MM, size))


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

        return StudioPreferences(
            strategy_name=strategy_name,
            use_custom_weights=bool(payload.get("use_custom_weights", False)),
            weights=weights,
            theme=theme,
            show_grid=bool(payload.get("show_grid", True)),
            grid_size_mm=grid_size_mm,
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
        }
        self.path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def update(self, preferences: StudioPreferences) -> None:
        self.save(preferences)
