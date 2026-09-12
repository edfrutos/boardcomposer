from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectConstraints:
    max_length_mm: float | None = None
    max_width_mm: float | None = None
    allow_rotation: bool = False
    allow_cutting: bool = False
    kerf_mm: float = 0.0

    def __post_init__(self) -> None:
        if self.max_length_mm is not None and self.max_length_mm <= 0:
            raise ValueError("max_length_mm debe ser mayor que 0")
        if self.max_width_mm is not None and self.max_width_mm <= 0:
            raise ValueError("max_width_mm debe ser mayor que 0")
        if self.kerf_mm < 0:
            raise ValueError("kerf_mm no puede ser negativo")
