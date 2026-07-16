from studio.models import StudioBoard
from studio.workspace.panel_layout import PanelSlot, arrange_panel_slots, slot_at_point


def test_arrange_panel_slots_lays_out_every_physical_instance_left_to_right():
    boards = [StudioBoard("P1", 1000, 500, "Demo", 19, 2)]

    slots = arrange_panel_slots(boards, gap_mm=100)

    assert [slot.key for slot in slots] == [(0, 0), (0, 1)]
    assert slots[0].x_mm == 0
    assert slots[1].x_mm == 1100


def test_arrange_panel_slots_advances_across_multiple_board_types():
    boards = [
        StudioBoard("P1", 1000, 500, "Demo", 19, 1),
        StudioBoard("P2", 800, 400, "Demo", 19, 1),
    ]

    slots = arrange_panel_slots(boards, gap_mm=100)

    assert [slot.board_id for slot in slots] == ["P1", "P2"]
    assert slots[1].x_mm == 1100


def test_slot_at_point_finds_the_slot_containing_the_coordinate():
    slots = [
        PanelSlot(0, "P1", 0, 0, 0, 1000, 500),
        PanelSlot(0, "P1", 1, 1200, 0, 1000, 500),
    ]

    assert slot_at_point(slots, 500, 250) == slots[0]
    assert slot_at_point(slots, 1500, 250) == slots[1]


def test_slot_at_point_returns_none_outside_every_slot():
    slots = [PanelSlot(0, "P1", 0, 0, 0, 1000, 500)]

    assert slot_at_point(slots, 1100, 250) is None


def test_slot_at_point_returns_none_in_the_gap_between_slots():
    slots = [
        PanelSlot(0, "P1", 0, 0, 0, 1000, 500),
        PanelSlot(0, "P1", 1, 1200, 0, 1000, 500),
    ]

    assert slot_at_point(slots, 1100, 250) is None
