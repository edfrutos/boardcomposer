"""Servicio de layout que conecta BoardComposer Studio con el motor de cálculo.

Convierte el proyecto de Studio en un proyecto del núcleo, ejecuta el
solver geométrico y gestiona la selección y aplicación de soluciones.
"""

from __future__ import annotations

from boardcomposer import Board, Project, ProjectConstraints
from boardcomposer.domain import AssemblySolution
from boardcomposer.solver.geometry_solver import GeometrySolver
from boardcomposer.solver.strategies import material_first_strategy

from studio.models import StudioPlacement
from boardcomposer.layout.validation import has_overlaps


class LayoutService:
    """Bridge between BoardComposer Studio and the core layout engine."""

    def __init__(self, services):
        self.services = services
        self.solutions: list[AssemblySolution] = []
        self.selected_solution_index = 0
        self.strategy_name: str | None = None

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

        candidate_solutions = GeometrySolver(
            project,
            strategy=strategy,
        ).solve()

        solutions = [
            solution
            for solution in candidate_solutions
            if self._is_valid_solution(solution)
        ]

        if not solutions:
            self.clear_solutions()
            return None

        self.solutions = solutions

    def apply_last_solution_to_current_project(self) -> bool:
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

    def _is_valid_solution(
        self,
        solution: AssemblySolution,
    ) -> bool:
        studio_project = self.services.projects.current_project

        if studio_project is None or not studio_project.boards:
            return False

        expected_ids = {piece.piece_id for piece in studio_project.pieces}
        placed_ids = [placement.board_id for placement in solution.placements]

        if len(placed_ids) != len(expected_ids):
            return False

        if len(set(placed_ids)) != len(placed_ids):
            return False

        if set(placed_ids) != expected_ids:
            return False

        if has_overlaps(solution.placements):
            return False

        board = studio_project.boards[0]

        for placement in solution.placements:
            placed_length = (
                placement.width_mm if placement.rotated else placement.length_mm
            )
            placed_width = (
                placement.length_mm if placement.rotated else placement.width_mm
            )

            if placement.x_mm < 0 or placement.y_mm < 0:
                return False

            if placement.x_mm + placed_length > board.length_mm:
                return False

            if placement.y_mm + placed_width > board.width_mm:
                return False

        return True

    def clear_solutions(self) -> None:
        """Clear cached layout solutions and reset selection state."""
        self.solutions = []
        self.selected_solution_index = 0
        self.strategy_name = None

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
