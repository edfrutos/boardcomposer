from boardcomposer import PanelReference, Project, StockPanel


def test_project_can_add_stock_panel():
    project = Project()
    panel = StockPanel(3000, 1200, 19, "P1")

    project.add_stock_panel(panel)

    assert project.stock_panels == [panel]


def test_project_expands_stock_panel_quantity_into_physical_instances():
    project = Project()
    panel = StockPanel(3000, 1200, 19, "P1", quantity=2)
    project.add_stock_panel(panel)

    assert project.stock_panel_instances() == (
        (PanelReference(stock_panel_index=0, instance_index=0), panel),
        (PanelReference(stock_panel_index=0, instance_index=1), panel),
    )
