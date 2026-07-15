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


BOARD_ORDERINGS = (
    ("original", original_order),
    ("largest_area", largest_area_first),
    ("longest_edge", longest_edge_first),
)


def smallest_area_first(boards: list[Board]) -> list[Board]:
    return sorted(
        boards,
        key=lambda board: (
            board.length_mm * board.width_mm,
            board.length_mm,
            board.width_mm,
        ),
    )


def shortest_edge_first(boards: list[Board]) -> list[Board]:
    return sorted(
        boards,
        key=lambda board: (
            max(board.length_mm, board.width_mm),
            board.length_mm * board.width_mm,
        ),
    )


def longest_first(boards: list[Board]) -> list[Board]:
    return sorted(
        boards,
        key=lambda board: (
            board.length_mm,
            board.width_mm,
            board.area_mm2,
        ),
        reverse=True,
    )


def widest_first(boards: list[Board]) -> list[Board]:
    return sorted(
        boards,
        key=lambda board: (
            board.width_mm,
            board.length_mm,
            board.area_mm2,
        ),
        reverse=True,
    )
