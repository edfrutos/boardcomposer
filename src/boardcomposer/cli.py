import argparse
import json

from boardcomposer import Board, Project, ProjectConstraints
from boardcomposer.io import load_project_from_csv
from boardcomposer.solver import GeometrySolver


def build_demo_project() -> Project:
    project = Project()
    project.add_board(Board(length_mm=2000, width_mm=300, thickness_mm=20, id="A"))
    project.add_board(Board(length_mm=1000, width_mm=300, thickness_mm=20, id="B"))
    return project


def main() -> None:
    parser = argparse.ArgumentParser(description="BoardComposer CLI")
    parser.add_argument("--csv", help="Ruta a un CSV con tablas")
    parser.add_argument("--max-length", type=float, help="Largo máximo en mm")
    parser.add_argument("--max-width", type=float, help="Ancho máximo en mm")
    parser.add_argument("--allow-rotation", action="store_true", help="Permitir rotar tablas")
    parser.add_argument("--json", action="store_true", help="Mostrar salida JSON")
    args = parser.parse_args()

    project load_project_from_csv(args.csv) if args.csv else build_demo_project()
    project.constraints = ProjectConstraints(
        max_length_mm=args.max_length,
        max_width_mm=args.max_width,
        allow_rotation=args.allow_rotation,
    )

    solutions = GeometrySolver(project).solve()

    if not solutions:
        print("No hay soluciones válidas.")
        return

    if args.json:
        print(
            json.dumps(
                {
                    "input_boards": len(project.boards),
                    "solutions": [
                        {
                            "placed_boards": len(solution.placements),
                            "total_length_mm": solution.total_length_mm,
                            "total_width_mm": solution.total_width_mm,
                            "score": solution.score.total,
                            "layout": solution.explanation.notes,
                            "placements": [
                                {
                                   "board_id": placement.board_id,
                                    "x_mm": placement.x_mm,
                                    "y_mm": placement.y_mm,
                                    "length_mm": placement.length_mm,
                                    "width_mm": placement.width_mm,
                                    "rotated": placement.rotated,
                                }
                                for placement in solution.placements
                            ],
                        }
                        for solution in solutions
                    ],
                },
                indent=2,
            )
        )
        return

    best = solutions[0]

    print("BoardComposer")
    print(f"Tablas entrada: {len(project.boards)}")
    print(f"Soluciones válidas: {len(solutions)}")
    print(f"Tablas colocadas: {len(best.placements)}")
    print(f"Largo total: {best.total_length_mm} mm")
    print(f"Ancho total: {best.total_width_mm} mm")
    print(f"Puntuación: {best.sre.total}")
    print(f"Layout: {', '.join(best.explanation.notes)}")
