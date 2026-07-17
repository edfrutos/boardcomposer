"""Application services for BoardComposer Studio."""

from dataclasses import dataclass, field
from studio.recent_files import RecentFilesManager

from studio.commands import CommandManager
from studio.events import EventBus
from studio.export_templates import ExportTemplatesManager
from studio.project import ProjectManager
from studio.project_templates import ProjectTemplatesManager
from studio.selection import SelectionManager
from studio.layout_service import LayoutService
from studio.preferences import PreferencesManager


@dataclass
class StudioServices:
    """Container for shared Studio services."""

    events: EventBus = field(default_factory=EventBus)
    projects: ProjectManager = field(default_factory=ProjectManager)
    selection: SelectionManager = field(default_factory=SelectionManager)
    commands: CommandManager = field(default_factory=CommandManager)
    recent_files: RecentFilesManager = field(default_factory=RecentFilesManager)
    preferences: PreferencesManager = field(default_factory=PreferencesManager)
    export_templates: ExportTemplatesManager = field(
        default_factory=ExportTemplatesManager
    )
    project_templates: ProjectTemplatesManager = field(
        default_factory=ProjectTemplatesManager
    )

    def __post_init__(self):
        self.layout = LayoutService(self)
