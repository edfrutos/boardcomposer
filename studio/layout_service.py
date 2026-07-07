from __future__ import annotations

from boardcomposer import Board, Project, ProjectConstraints
from boardcomposer.solver.geometry_solver import GeometrySolver
from boardcomposer.solver.strategies import material_first_strategy

from studio.models import StudioPlacement


class LayoutService:
    """Bridge between BoardComposer Studio and the core layout engine."""

    def __init__(self, services):
        self.services = services
        self.solutions = []
        self.selected_solution_index = 0
        self.strategy_name = None

    def select_next_solution(self):
        if not self.solutions:
            return None

        self.selected_solution_index = (
            self.selected_solution_index + 1
        ) % len(self.solutions)

        return self.selected_solution

    def select_previous_solution(self):
        if not self.solutions:
            return None

        self.selected_solution_index = (
            self.selected_solution_index - 1
        ) % len(self.solutions)

        return self.selected_solution

    @property
    def selected_solution(self):
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

    def solve_current_project(self):
        project = self.to_core_project()
        if project is None:
            return None

        strategy = material_first_strategy()
        self.strategy_name = strategy.name

        solutions = GeometrySolver(
            project,
            strategy=strategy,
        ).solve()

        if not solutions:
            return None

        self.solutions = solutions
        self.selected_solution_index = 0
        return self.selected_solution

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


@property
def selected_solution(self):
    if not self.solutions:
        return None

    return self.solutions[self.selected_solution_index]
