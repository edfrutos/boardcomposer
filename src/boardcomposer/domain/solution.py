from dataclasses import dataclass, field

from boardcomposer.layout.bounds import bounding_rectangle

from .explanation import SolutionExplanation
from .offcut import Offcut
from .panel_reference import PanelReference
from .placement import BoardPlacement
from .project import Project
from .score import SolutionScore


@dataclass(frozen=True)
class AssemblySolution:
    placements: list[BoardPlacement]
    score: SolutionScore = field(default_factory=SolutionScore)
    explanation: SolutionExplanation = field(default_factory=SolutionExplanation)
    omitted_piece_ids: tuple[str, ...] = ()
    offcuts: tuple[Offcut, ...] = ()

    @property
    def is_complete(self) -> bool:
        """Return whether every requested piece was placed."""
        return not self.omitted_piece_ids

    @property
    def total_offcut_area_mm2(self) -> float:
        """Return the total area of every reported offcut."""
        return sum(offcut.area_mm2 for offcut in self.offcuts)

    @property
    def used_area_mm2(self) -> float:
        return sum(p.area_mm2 for p in self.placements)

    @property
    def total_length_mm(self) -> float:
        return bounding_rectangle(self.placements).length_mm

    @property
    def total_width_mm(self) -> float:
        return bounding_rectangle(self.placements).width_mm

    @property
    def bounding_area_mm2(self) -> float:
        if self.panel_references:
            return sum(
                bounding_rectangle(
                    [
                        placement
                        for placement in self.placements
                        if placement.panel_reference == reference
                    ]
                ).area_mm2
                for reference in self.panel_references
            )
        return bounding_rectangle(self.placements).area_mm2

    @property
    def waste_area_mm2(self) -> float:
        return self.bounding_area_mm2 - self.used_area_mm2

    @property
    def waste_ratio(self) -> float:
        if self.bounding_area_mm2 == 0:
            return 0
        return self.waste_area_mm2 / self.bounding_area_mm2

    @property
    def panel_references(self) -> tuple[PanelReference, ...]:
        """Return the physical panels consumed by this solution."""
        return tuple(
            sorted(
                {
                    placement.panel_reference
                    for placement in self.placements
                    if placement.panel_reference is not None
                }
            )
        )

    def panel_used_area_mm2(self, reference: PanelReference) -> float:
        """Return the piece area assigned to one physical panel."""
        return sum(
            placement.area_mm2
            for placement in self.placements
            if placement.panel_reference == reference
        )

    def panel_waste_area_mm2(
        self,
        project: Project,
        reference: PanelReference,
    ) -> float:
        """Return unused area on one consumed physical panel."""
        panel = project.stock_panel_for(reference)
        if panel is None:
            raise ValueError("La referencia de panel no existe en el proyecto")
        return panel.area_mm2 - self.panel_used_area_mm2(reference)

    def total_panel_area_mm2(self, project: Project) -> float:
        """Return the area of all physical panels consumed by the solution."""
        total = 0.0
        for reference in self.panel_references:
            panel = project.stock_panel_for(reference)
            if panel is None:
                raise ValueError("La referencia de panel no existe en el proyecto")
            total += panel.area_mm2
        return total

    def total_panel_waste_area_mm2(self, project: Project) -> float:
        """Return total unused area across consumed physical panels."""
        return sum(
            self.panel_waste_area_mm2(project, reference)
            for reference in self.panel_references
        )

    def panel_waste_ratio(self, project: Project) -> float:
        """Return total waste relative to consumed physical-panel area."""
        total_area = self.total_panel_area_mm2(project)
        if total_area == 0:
            return 0.0
        return self.total_panel_waste_area_mm2(project) / total_area
