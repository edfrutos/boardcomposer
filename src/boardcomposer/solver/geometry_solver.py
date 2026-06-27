from boardcomposer.domain import Project

from .base_solver import BaseSolver
from .sequential_solver import SequentialSolver


class GeometrySolver(BaseSolver):
    def __init__(self, project: Project) -> None:
        self.project = project

    def solve(self):
        # Temporalmente delega en el solver secuencial.
        # Aquí construiremos el motor geométrico.
        return SequentialSolver(self.project).solve()
