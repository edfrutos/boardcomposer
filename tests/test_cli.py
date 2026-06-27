from boardcomposer.cli import build_demo_project


def test_build_demo_project():
    project = build_demo_project()

    assert len(project.boards) == 2
    assert project.total_area_mm2 == 900000
