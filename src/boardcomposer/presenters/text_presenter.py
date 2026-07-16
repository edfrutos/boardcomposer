from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.solver.strategies import OptimizationStrategy

from .base import Presenter


class TextPresenter(Presenter):
    def render(
        self,
        project: Project,
        strategy: OptimizationStrategy | None,
        solutions: list[AssemblySolution],
        top: int,
    ) -> str:
        best = solutions[0]

        lines = [
            "BoardComposer",
            f"Tablas entrada: {len(project.boards)}",
            f"Soluciones válidas: {len(solutions)}",
            f"Tablas colocadas: {len(best.placements)}",
            f"Largo total: {best.total_length_mm} mm",
            f"Ancho total: {best.total_width_mm} mm",
            f"Puntuación: {best.score.total}",
            f"Layout: {', '.join(best.explanation.notes)}",
        ]

        if best.omitted_piece_ids:
            lines.append(f"Piezas sin colocar: {', '.join(best.omitted_piece_ids)}")

        if best.offcuts:
            lines.append(
                f"Retales aprovechables: {len(best.offcuts)} "
                f"(área total {best.total_offcut_area_mm2:.0f} mm²)"
            )

        return "\n".join(lines)


def solution_to_text(
    project: Project,
    solutions: list[AssemblySolution],
) -> str:
    return TextPresenter().render(
        project=project,
        strategy=None,
        solutions=solutions,
        top=1,
    )
