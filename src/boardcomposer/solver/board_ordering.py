from boardcomposer.domain import Board


def original_order(boards: list[Board]) -> list[Board]:
    return list(boards)


def largest_area_first(boards: list[Board]) -> list[Board]:
    return sorted(
        boards,
        key=lambda board: (
            board.length_mm * board.width_mm,
            board.length_mm,
            board.width_mm,
        ),
        reverse=True,
    )


def longest_edge_first(boards: list[Board]) -> list[Board]:
    return sorted(
        boards,
        key=lambda board: (
            max(board.length_mm, board.width_mm),
            board.length_mm * board.width_mm,
        ),
        reverse=True,
    )
