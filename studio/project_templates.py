"""Named project templates for BoardComposer Studio (SCR-001 / SCR-005)."""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field
from pathlib import Path

from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.project_serializer import load_project, save_project


def default_project_templates_dir() -> Path:
    return Path.home() / ".boardcomposer" / "project_templates"


def slugify_template_name(name: str) -> str:
    """Build a filesystem-safe stem from a display name."""
    cleaned = re.sub(r"[^\w\-]+", "-", name.strip(), flags=re.UNICODE)
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-._")
    return cleaned.casefold() or "plantilla"


@dataclass(frozen=True)
class ProjectTemplateInfo:
    """Metadata for a stored project template."""

    name: str
    path: Path

    @property
    def board_count(self) -> int:
        try:
            project = load_project(self.path)
        except Exception:
            return 0
        return len(project.boards)

    @property
    def piece_count(self) -> int:
        try:
            project = load_project(self.path)
        except Exception:
            return 0
        return len(project.pieces)


@dataclass
class ProjectTemplatesManager:
    """Persist and instantiate project templates as `.bcproj` files."""

    directory: Path | None = None
    autoload: bool = True
    _templates: list[ProjectTemplateInfo] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        if self.directory is None:
            self.directory = default_project_templates_dir()
        if self.autoload:
            self.refresh()

    def refresh(self) -> list[ProjectTemplateInfo]:
        assert self.directory is not None
        self.directory.mkdir(parents=True, exist_ok=True)
        templates: list[ProjectTemplateInfo] = []
        for path in sorted(self.directory.glob("*.bcproj")):
            try:
                project = load_project(path)
            except Exception:
                continue
            templates.append(ProjectTemplateInfo(name=project.name, path=path))
        templates.sort(key=lambda item: item.name.casefold())
        self._templates = templates
        return list(self._templates)

    def list(self) -> list[ProjectTemplateInfo]:
        return list(self._templates)

    def get(self, name: str) -> ProjectTemplateInfo | None:
        wanted = name.strip().casefold()
        for template in self._templates:
            if template.name.casefold() == wanted:
                return template
        return None

    def save_from_project(
        self,
        name: str,
        project: StudioProject,
        *,
        include_placements: bool = False,
    ) -> ProjectTemplateInfo:
        """Save boards/pieces (and optional placements) as a named template."""
        cleaned = name.strip()
        if not cleaned:
            raise ValueError("El nombre de la plantilla no puede estar vacío")

        assert self.directory is not None
        self.directory.mkdir(parents=True, exist_ok=True)

        existing = self.get(cleaned)
        if existing is not None:
            path = existing.path
        else:
            stem = slugify_template_name(cleaned)
            path = self.directory / f"{stem}.bcproj"
            counter = 2
            while path.exists():
                path = self.directory / f"{stem}-{counter}.bcproj"
                counter += 1

        template_project = StudioProject(
            project_id=f"TPL-{slugify_template_name(cleaned)[:24]}",
            name=cleaned,
            boards=[
                StudioBoard(
                    board.board_id,
                    board.length_mm,
                    board.width_mm,
                    board.material,
                    board.thickness_mm,
                    board.quantity,
                )
                for board in project.boards
            ],
            pieces=[
                StudioPiece(
                    piece.piece_id,
                    piece.length_mm,
                    piece.width_mm,
                    piece.material,
                    piece.thickness_mm,
                )
                for piece in project.pieces
            ],
            placements=(
                [
                    StudioPlacement(
                        placement.piece_id,
                        placement.x_mm,
                        placement.y_mm,
                        placement.rotated,
                        placement.rotation,
                        placement.board_id,
                        placement.board_instance,
                        placement.stock_panel_index,
                    )
                    for placement in project.placements
                ]
                if include_placements
                else []
            ),
        )
        save_project(template_project, path)
        self.refresh()
        saved = self.get(cleaned)
        if saved is None:
            raise RuntimeError("La plantilla no se pudo registrar tras guardarla")
        return saved

    def delete(self, name: str) -> bool:
        template = self.get(name)
        if template is None:
            return False
        try:
            template.path.unlink(missing_ok=True)
        except OSError:
            return False
        self.refresh()
        return True

    def instantiate(
        self,
        name: str,
        *,
        include_placements: bool = False,
    ) -> StudioProject:
        """Load a template as a new untitled project (new id, no file path)."""
        template = self.get(name)
        if template is None:
            raise KeyError(name)
        source = load_project(template.path)
        return StudioProject(
            project_id=f"PRJ-{uuid.uuid4().hex[:8].upper()}",
            name=source.name,
            boards=list(source.boards),
            pieces=list(source.pieces),
            placements=list(source.placements) if include_placements else [],
        )
