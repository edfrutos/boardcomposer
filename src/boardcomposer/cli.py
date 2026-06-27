import argparse

from boardcomposer import Board, Project
from boardcomposer.io import load_project_from_csv
from boardcomposer.solver import SequentialSolver


def build_demo_project() -> Project:
    project = Project()
    project.add_board(Board(length_mm=2000, width_mm=300, thickness_mm=20, id="A"))
    project.add_board(Board(length_mm=1000, width_mm=300, thickness_mm=20, id="B"))
    return project


def main() -> None:
    parser = argparse.ArgumentParser(description="BoardComposer CLI")
    parser.add_argument("--csv", help="Ruta a un CSV con tablas")
    args = parser.parse_args()

    project = load_project_from_csv(args.csv) if args.csv else build_demo_project()
    solution = SequentialSolver(project).solve()[0]

    print("BoardComposer")
    print(f"Tablas entrada: {len(project.boards)}")
    print(f"Tablas colocadas: {len(solution.placements)}")
    print(f"Largo total: {solution.total_length_mm} mm")
    print(f"Ancho total: {solution.total_width_mm} mm")
    print(f"Puntuación: {solution.score.total}")
