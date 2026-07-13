"""Servicio de layout que conecta BoardComposer Studio con el motor de cálculo.

Convierte el proyecto de Studio en un proyecto del núcleo, ejecuta el
solver geométrico y gestiona la selección y aplicación de soluciones.
"""

from __future__ import annotations

from boardcomposer import Board, Project, ProjectConstraints
from boardcomposer.domain import AssemblySolution
from boardcomposer.solver.geometry_solver import GeometrySolver
from boardcomposer.solver.pipeline_stats import PipelineStats
from boardcomposer.solver.strategies import material_first_strategy

from studio.models import StudioPlacement


class LayoutService:
    """Bridge between BoardComposer Studio and the core layout engine."""

    def __init__(self, services):
        self.services = services
        self.solutions: list[AssemblySolution] = []
        self.selected_solution_index = 0
        self.strategy_name: str | None = None
        self.stats = PipelineStats()

    def select_next_solution(self) -> AssemblySolution | None:
        """Select and return the next solution in the list, wrapping to the first."""
        if not self.solutions:
            return None

        self.selected_solution_index = (self.selected_solution_index + 1) % len(
            self.solutions
        )

        return self.selected_solution

    def select_previous_solution(self) -> AssemblySolution | None:
        """Select and return the previous solution in the list, wrapping to the last."""
        if not self.solutions:
            return None

        self.selected_solution_index = (self.selected_solution_index - 1) % len(
            self.solutions
        )

        return self.selected_solution

    def select_solution(self, index: int) -> AssemblySolution | None:
        """Select and return the solution at the given index."""
        if not self.solutions:
            return None

        if index < 0 or index >= len(self.solutions):
            return None

        self.selected_solution_index = index
        return self.selected_solution

    @property
    def selected_solution(self) -> AssemblySolution | None:
        if not self.solutions:
            return None

        return self.solutions[self.selected_solution_index]

    def to_core_project(self) -> Project | None:
        studio_project = self.services.projects.current_project
        if studio_project is None:
            return None

        core_project = Project(
            constraints=ProjectConstraints(
                allow_rotation=True,
                allow_cutting=False,
            )
        )

        source_board = studio_project.boards[0] if studio_project.boards else None

        if source_board is not None:
            core_project.constraints = ProjectConstraints(
                max_length_mm=source_board.length_mm,
                max_width_mm=source_board.width_mm,
                allow_rotation=True,
                allow_cutting=False,
            )

        for piece in studio_project.pieces:
            core_project.add_board(
                Board(
                    id=piece.piece_id,
                    length_mm=piece.length_mm,
                    width_mm=piece.width_mm,
                    thickness_mm=19,
                )
            )

        return core_project

    def solve_current_project(self) -> AssemblySolution | None:
        project = self.to_core_project()
        if project is None:
            return None

        strategy = material_first_strategy()
        self.strategy_name = strategy.name

        solver = GeometrySolver(
            project,
            strategy=strategy,
        )

        solutions = solver.solve()
        self.stats = solver.stats

        if not solutions:
            self.clear_solutions()

            return None

        self.solutions = solutions
        self.selected_solution_index = 0

        return self.selected_solution

    def apply_last_solution_to_current_project(self) -> bool:
        """Apply the last solution to the current project."""
        studio_project = self.services.projects.current_project
        solution = self.selected_solution

        if studio_project is None or solution is None:
            return False

        studio_project.placements.clear()

        for placement in solution.placements:
            studio_project.placements.append(
                StudioPlacement(
                    piece_id=placement.board_id,
                    x_mm=placement.x_mm,
                    y_mm=placement.y_mm,
                    rotated=placement.rotated,
                    rotation=90 if placement.rotated else 0,
                )
            )

        self.services.projects.mark_modified()
        return True

    def clear_solutions(self) -> None:
        """Clear cached layout solutions and reset selection state."""
        self.solutions = []
        self.selected_solution_index = 0
        self.strategy_name = None
        self.stats = PipelineStats()

    def board_waste_ratio(self, solution: AssemblySolution) -> float:
        """Return unused board area relative to the source board."""
        studio_project = self.services.projects.current_project

        if studio_project is None or not studio_project.boards:
            return 0.0

        board = studio_project.boards[0]
        board_area = board.length_mm * board.width_mm

        if board_area <= 0:
            return 0.0

        return max(0.0, 1.0 - solution.used_area_mm2 / board_area)

    def stats_summary_lines(self) -> list[str]:
        """Return human-readable solver statistics."""
        lines = [
            "Diagnóstico del cálculo",
            f"Candidatas generadas: {self.stats.generated}",
            f"Candidatas únicas: {self.stats.unique}",
            f"Aceptadas: {self.stats.accepted}",
            f"Rechazadas: {self.stats.rejected}",
        ]

        reason_labels = {
            "missing_board": "Piezas omitidas",
            "duplicate_board": "Piezas duplicadas",
            "unknown_board": "Piezas desconocidas",
            "overlap": "Solapes",
            "exceeds_constraints": "Fuera del tablero",
        }

        if self.stats.rejection_reasons:
            lines.append("")
            lines.append("Motivos de rechazo:")

            for reason, count in self.stats.rejection_reasons.items():
                label = reason_labels.get(reason.value, reason.value)
                lines.append(f"  {label}: {count}")

        return lines
