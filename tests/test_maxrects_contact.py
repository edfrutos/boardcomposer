from boardcomposer.solver.maxrects.contact import contact_score
from boardcomposer.solver.maxrects.placement import MaxRectsPlacement


def test_contact_score_without_contact():
    placement = MaxRectsPlacement(1000, 1000, 500, 500)

    assert contact_score(placement, [], 3000, 3000) == 0


def test_contact_score_with_left_edge():
    placement = MaxRectsPlacement(0, 1000, 500, 300)

    assert contact_score(placement, [], 3000, 3000) == 300


def test_contact_score_with_vertical_piece_contact():
    placement = MaxRectsPlacement(500, 0, 500, 300)
    placed = [
        MaxRectsPlacement(0, 0, 500, 300),
    ]

    assert contact_score(placement, placed, 3000, 3000) == 800


def test_contact_score_with_horizontal_piece_contact():
    placement = MaxRectsPlacement(0, 300, 500, 300)
    placed = [
        MaxRectsPlacement(0, 0, 500, 300),
    ]

    assert contact_score(placement, placed, 3000, 3000) == 800
