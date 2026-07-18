from studio.explorer_actions import explorer_context_actions, parse_explorer_role


def test_parse_explorer_role():
    assert parse_explorer_role("piece:A") == ("piece", "A")
    assert parse_explorer_role("category:boards") == ("category", "boards")
    assert parse_explorer_role(None) is None
    assert parse_explorer_role("invalid") is None


def test_explorer_context_actions_for_piece():
    assert explorer_context_actions("piece:A") == ("edit", "duplicate", "delete")


def test_explorer_context_actions_for_board_and_categories():
    assert explorer_context_actions("board:B1") == ("edit", "delete")
    assert explorer_context_actions("category:boards") == ("add_board",)
    assert explorer_context_actions("category:pieces") == ("add_piece",)
    assert explorer_context_actions("category:solutions") == ()
    assert explorer_context_actions("solution:2") == ("preview_solution",)
