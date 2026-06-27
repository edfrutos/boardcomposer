from boardcomposer import Board, Project
from boardcomposer.solver import SequentialSolver


def main() -> None:
    project = Project()
    project.add_board(Board(length_mm=2000, width_mm=300, thickness_mm=20, id="A"))
    project.add_board(Board(length_mm=1000, width_mm=300, thickness_mm=20, id="B"))

    solution = SequentialSolver(project).solve()[0]

    print("BoardComposer")
    print(f"Soluciones: 1")
    print(f"Tablas colocadas: {len(solution.placements)}")
    print(f"Largo total: {solution.total_length_mm} mm")
    print(f"Ancho total: {solution.total_width_mm} mm")
    print(f"Puntuación: {solution.score.total}")
