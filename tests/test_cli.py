from boardcomposer.cli import build_demo_project


def test_build_demo_project():
    project = build_demo_project()

    assert len(project.boards) == 2
    assert project.total_area_mm2 == 900000


def test_cli_project_constraints_from_cli_options():
    from boardcomposer import ProjectConstraints

    constraints = ProjectConstraints(
        max_length_mm=2500,
        max_width_mm=600,
        **{"allow_rotation": True},
    )

    assert constraints.max_length_mm == 2500
    assert constraints.max_width_mm == 600
    assert constraints.allow_rotation is True
