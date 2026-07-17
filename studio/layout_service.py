"""Servicio de layout que conecta BoardComposer Studio con el motor de cálculo.

Convierte el proyecto de Studio en un proyecto del núcleo, ejecuta el
solver geométrico y gestiona la selección y aplicación de soluciones.
"""

from __future__ import annotations

from boardcomposer import Board, Project, ProjectConstraints, StockPanel
from boardcomposer.domain import AssemblySolution
from boardcomposer.solver.cancel import CancellationToken
from boardcomposer.solver.geometry_solver import GeometrySolver
from boardcomposer.solver.pipeline_stats import PipelineStats
from boardcomposer.solver.strategies import material_first_strategy

from studio.models import StudioPlacement
from studio.solution_highlights import solution_highlights


class LayoutService:
    """Bridge between BoardComposer Studio and the core layout engine."""

    def __init__(self, services):
        self.services = services
        self.solutions: list[AssemblySolution] = []
        self.selected_solution_index = 0
        self.strategy_name: str | None = None
        self.stats = PipelineStats()
        self._solved_project: Project | None = None

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

    @property
    def solved_project(self) -> Project | None:
        """Return the Core project used for the current solution set."""
        return self._solved_project

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

        for board in studio_project.boards:
            core_project.add_stock_panel(
                StockPanel(
                    id=board.board_id,
                    length_mm=board.length_mm,
                    width_mm=board.width_mm,
                    thickness_mm=board.thickness_mm,
                    quantity=board.quantity,
                    material=board.material,
                )
            )

        for piece in studio_project.pieces:
            core_project.add_board(
                Board(
                    id=piece.piece_id,
                    length_mm=piece.length_mm,
                    width_mm=piece.width_mm,
                    thickness_mm=piece.thickness_mm,
                    material=piece.material,
                )
            )

        return core_project

    def _resolve_strategy(self):
        preferences = getattr(self.services, "preferences", None)
        if preferences is None:
            return material_first_strategy()
        return preferences.current.resolved_strategy()

    def solve_current_project(
        self,
        cancel: CancellationToken | None = None,
    ) -> AssemblySolution | None:
        project = self.to_core_project()
        if project is None:
            return None
        self._solved_project = project

        strategy = self._resolve_strategy()
        self.strategy_name = strategy.name

        solver = GeometrySolver(
            project,
            strategy=strategy,
            cancel=cancel,
        )

        solutions = solver.solve()
        self.stats = solver.stats

        if not solutions:
            self.solutions = []
            self.selected_solution_index = 0

            return None

        preferences = getattr(self.services, "preferences", None)
        limit = (
            preferences.current.max_solutions
            if preferences is not None
            else len(solutions)
        )
        self.solutions = solutions[: max(1, limit)]
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
            panel_reference = placement.panel_reference
            board_id = None
            board_instance = 0

            if panel_reference is not None and panel_reference.stock_panel_index < len(
                studio_project.boards
            ):
                board_id = studio_project.boards[
                    panel_reference.stock_panel_index
                ].board_id
                board_instance = panel_reference.instance_index

            studio_project.placements.append(
                StudioPlacement(
                    piece_id=placement.board_id,
                    x_mm=placement.x_mm,
                    y_mm=placement.y_mm,
                    rotated=placement.rotated,
                    rotation=90 if placement.rotated else 0,
                    board_id=board_id,
                    board_instance=board_instance,
                    stock_panel_index=(
                        panel_reference.stock_panel_index
                        if panel_reference is not None
                        else None
                    ),
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
        self._solved_project = None

    def board_waste_ratio(self, solution: AssemblySolution) -> float:
        """Return unused board area relative to the source board."""
        if self._solved_project is not None and solution.panel_references:
            return solution.panel_waste_ratio(self._solved_project)

        studio_project = self.services.projects.current_project

        if studio_project is None or not studio_project.boards:
            return 0.0

        board = studio_project.boards[0]
        board_area = board.length_mm * board.width_mm

        if board_area <= 0:
            return 0.0

        return max(0.0, 1.0 - solution.used_area_mm2 / board_area)

    @property
    def solution_highlights(self) -> dict[int, list[str]]:
        """Return, per solution index, which metrics it wins at (SCR-003)."""
        return solution_highlights(self.solutions)

    def stats_summary_lines(self, language: str = "es") -> list[str]:
        """Return human-readable solver statistics."""
        from studio.i18n import tr

        lines = [
            tr("diag.title", language),
            tr("diag.generated", language, n=self.stats.generated),
            tr("diag.unique", language, n=self.stats.unique),
            tr("diag.accepted", language, n=self.stats.accepted),
            tr("diag.rejected", language, n=self.stats.rejected),
        ]
        if self.stats.cancelled:
            lines.insert(1, tr("diag.cancelled", language))

        reason_keys = {
            "missing_board": "diag.missing_board",
            "duplicate_board": "diag.duplicate_board",
            "unknown_board": "diag.unknown_board",
            "overlap": "diag.overlap",
            "exceeds_constraints": "diag.exceeds_constraints",
            "unassigned_stock_panel": "diag.unassigned_stock_panel",
            "unknown_stock_panel": "diag.unknown_stock_panel",
            "exceeds_stock_panel": "diag.exceeds_stock_panel",
            "panel_thickness_mismatch": "diag.panel_thickness_mismatch",
            "panel_material_mismatch": "diag.panel_material_mismatch",
        }

        if self.stats.rejection_reasons:
            lines.append("")
            lines.append(tr("diag.reasons", language))

            for reason, count in self.stats.rejection_reasons.items():
                key = reason_keys.get(reason.value)
                label = tr(key, language) if key else reason.value
                lines.append(f"  {label}: {count}")

        return lines
