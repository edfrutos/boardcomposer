from boardcomposer.solver.board_ordering import (
    largest_area_first,
    longest_edge_first,
    longest_first,
    original_order,
    shortest_edge_first,
    smallest_area_first,
    widest_first,
)

MAXRECTS_BOARD_ORDERINGS = (
    ("original", original_order),
    ("largest_area", largest_area_first),
    ("smallest_area", smallest_area_first),
    ("longest_edge", longest_edge_first),
    ("shortest_edge", shortest_edge_first),
    ("longest", longest_first),
    ("widest", widest_first),
)
