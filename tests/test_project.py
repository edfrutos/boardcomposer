from boardcomposer import Project, StockPanel


def test_project_can_add_stock_panel():
    project = Project()
    panel = StockPanel(3000, 1200, 19, "P1")

    project.add_stock_panel(panel)

    assert project.stock_panels == [panel]
