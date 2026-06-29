from boardcomposer.solver.skyline.skyline import Skyline


def test_skyline_can_be_created():
    skyline = Skyline()

    assert skyline is not None
