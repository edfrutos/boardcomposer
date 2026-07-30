"""Tests for Timeline payload formatting helpers."""

from studio.timeline.panel import _format_payload


def test_format_payload_piece_moved_same_panel():
    payload = {
        "piece": "A",
        "kind": "moved",
        "from_x": 10.0,
        "from_y": 20.0,
        "to_x": 30.0,
        "to_y": 40.0,
        "from_board": "P1",
        "to_board": "P1",
        "from_board_instance": 0,
        "to_board_instance": 0,
        "from_stock_panel_index": 0,
        "to_stock_panel_index": 0,
    }
    assert _format_payload(payload, "es") == "A: (10,20)→(30,40)"


def test_format_payload_piece_moved_reassigned_panel():
    payload = {
        "piece": "A",
        "kind": "reassigned",
        "from_x": 10.0,
        "from_y": 20.0,
        "to_x": 30.0,
        "to_y": 40.0,
        "from_board": "P1",
        "to_board": "P2",
        "from_board_instance": 0,
        "to_board_instance": 1,
        "from_stock_panel_index": 0,
        "to_stock_panel_index": 1,
    }
    assert _format_payload(payload, "es") == "A: P1#0→P2#1, (10,20)→(30,40)"


def test_format_payload_piece_moved_keeps_other_details():
    payload = {
        "piece": "A",
        "kind": "moved",
        "from_x": 1.0,
        "from_y": 2.0,
        "to_x": 3.0,
        "to_y": 4.0,
        "count": 2,
        "algorithm": "maxrects",
    }
    text = _format_payload(payload, "en")
    assert "A: (1,2)→(3,4)" in text
    assert "2 item(s)" in text
    assert "maxrects" in text
