from statistics import mean

from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.layout.bounds import bounding_rectangle


def material_utilization(
    solution: AssemblySolution,
    project: Project | None = None,
) -> float:
    if project is not None and project.stock_panels:
        panel_area = solution.total_panel_area_mm2(project)
        if panel_area == 0:
            return 0.0
        return solution.used_area_mm2 / panel_area

    if solution.bounding_area_mm2 == 0:
        return 0.0
    return solution.used_area_mm2 / solution.bounding_area_mm2


def _compactness_ratio(length_mm: float, width_mm: float) -> float | None:
    if length_mm == 0 or width_mm == 0:
        return None

    long_side = max(length_mm, width_mm)
    short_side = min(length_mm, width_mm)

    return short_side / long_side


def compactness(solution: AssemblySolution) -> float:
    if solution.panel_references:
        ratios = []
        for reference in solution.panel_references:
            panel_placements = [
                placement
                for placement in solution.placements
                if placement.panel_reference == reference
            ]
            rect = bounding_rectangle(panel_placements)
            ratio = _compactness_ratio(rect.length_mm, rect.width_mm)
            if ratio is not None:
                ratios.append(ratio)

        return mean(ratios) if ratios else 0.0

    ratio = _compactness_ratio(solution.total_length_mm, solution.total_width_mm)
    return ratio if ratio is not None else 0.0


def rotation_ratio(solution: AssemblySolution) -> float:
    if not solution.placements:
        return 0.0

    rotated = sum(1 for placement in solution.placements if placement.rotated)
    return rotated / len(solution.placements)


def placed_board_ratio(solution: AssemblySolution, total_boards: int) -> float:
    if total_boards == 0:
        return 0.0

    return len(solution.placements) / total_boards
