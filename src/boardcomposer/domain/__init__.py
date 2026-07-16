"""
🔹Entidades de dominio para la aplicación BoardComposer.
"""

from .board import Board
from .constraints import ProjectConstraints
from .explanation import SolutionExplanation
from .offcut import Offcut
from .panel_reference import PanelReference
from .placement import BoardPlacement
from .project import Project
from .score import SolutionScore
from .solution import AssemblySolution
from .stock_panel import StockPanel

__all__ = [
    "AssemblySolution",
    "Board",
    "BoardPlacement",
    "Offcut",
    "PanelReference",
    "Project",
    "ProjectConstraints",
    "SolutionExplanation",
    "SolutionScore",
    "StockPanel",
]
