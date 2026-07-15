"""MaxRects state implementation."""

from copy import deepcopy
from dataclasses import dataclass

from boardcomposer.domain import Board, BoardPlacement
from boardcomposer.solver.maxrects.maxrects import MaxRects
from boardcomposer.solver.maxrects.contact import contact_score
from boardcomposer.solver.maxrects.placement import MaxRectsPlacement


@dataclass
class MaxRectsState:
    packer: MaxRects
    placements: list[BoardPlacement]
    next_board: int

    def clone(self) -> "MaxRectsState":
        return MaxRectsState(
            packer=deepcopy(self.packer),
            placements=self.placements.copy(),
            next_board=self.next_board,
        )

    def expand(
        self,
        boards: list[Board],
        allow_rotation: bool,
        candidate_width: int | None = None,
    ) -> list["MaxRectsState"]:

        if self.next_board >= len(boards):
            return []

        board = boards[self.next_board]
        candidates = self.packer.find_candidates(
            board.length_mm,
            board.width_mm,
            allow_rotation=allow_rotation,
        )

        candidates = sorted(
            candidates,
            key=self._candidate_key,
            reverse=True,
        )

        if candidate_width is not None:
            if candidate_width <= 0:
                raise ValueError("candidate_width debe ser mayor que 0")

            candidates = candidates[:candidate_width]
        states = []

        for candidate in candidates:
            state = self.clone()
            placement = state.packer.place_candidate(candidate)
            state.placements.append(
                BoardPlacement(
                    board_id=board.id or f"board-{self.next_board + 1}",
                    x_mm=placement.x_mm,
                    y_mm=placement.y_mm,
                    length_mm=placement.length_mm,
                    width_mm=placement.width_mm,
                    rotated=placement.rotated,
                )
            )
            state.next_board += 1
            states.append(state)

        return states

    def _candidate_key(
        self,
        candidate: MaxRectsPlacement,
    ) -> tuple[float, float, float, float, float]:
        placed = [
            MaxRectsPlacement(
                x_mm=placement.x_mm,
                y_mm=placement.y_mm,
                length_mm=placement.length_mm,
                width_mm=placement.width_mm,
                rotated=placement.rotated,
            )
            for placement in self.placements
        ]

        contact = contact_score(
            candidate,
            placed,
            board_length_mm=self.packer.length_mm,
            board_width_mm=self.packer.width_mm,
        )

        waste = self.packer._waste_area(candidate)

        occupied_length = max(
            [placement.x_mm + placement.length_mm for placement in self.placements]
            + [candidate.x_mm + candidate.length_mm]
        )
        occupied_width = max(
            [placement.y_mm + placement.width_mm for placement in self.placements]
            + [candidate.y_mm + candidate.width_mm]
        )

        occupied_area = occupied_length * occupied_width

        return (
            -waste,
            contact,
            -occupied_area,
            -candidate.y_mm,
            -candidate.x_mm,
        )
