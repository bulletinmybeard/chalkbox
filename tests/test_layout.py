from rich.text import Text

from chalkbox.components.layout import MultiPanel


class TestMultiPanel:
    """Tests for MultiPanel component."""

    def test_layout_creation(self):
        """Test basic layout creation."""
        layout = MultiPanel("test")
        assert layout.name == "test"

    def test_layout_default_name(self):
        """Test layout with default name."""
        layout = MultiPanel()
        assert layout.name == "root"

    def test_layout_update(self):
        """Test updating layout content."""
        layout = MultiPanel()
        content = Text("Test content")
        layout.update(content)
        # Should not raise error

    def test_layout_split_row(self):
        """Test horizontal split."""
        root = MultiPanel()
        left = MultiPanel("left")
        right = MultiPanel("right")
        root.split_row(left, right)
        # Should not raise error

    def test_layout_split_column(self):
        """Test vertical split."""
        root = MultiPanel()
        top = MultiPanel("top")
        bottom = MultiPanel("bottom")
        root.split_column(top, bottom)
        # Should not raise error

    def test_layout_create_sidebar_left(self):
        """Test sidebar layout with left position."""
        sidebar_content = Text("Sidebar")
        main_content = Text("Main")
        layout = MultiPanel.create_sidebar(sidebar_content, main_content, sidebar_position="left")
        assert layout is not None

    def test_layout_create_sidebar_right(self):
        """Test sidebar layout with right position."""
        sidebar_content = Text("Sidebar")
        main_content = Text("Main")
        layout = MultiPanel.create_sidebar(sidebar_content, main_content, sidebar_position="right")
        assert layout is not None

    def test_layout_create_header_footer(self):
        """Test header/footer layout."""
        header = Text("Header")
        main = Text("Main")
        footer = Text("Footer")
        layout = MultiPanel.create_header_footer(header, main, footer)
        assert layout is not None

    def test_layout_create_grid(self):
        """Test grid layout."""
        panels = {
            "panel1": Text("Panel 1"),
            "panel2": Text("Panel 2"),
            "panel3": Text("Panel 3"),
            "panel4": Text("Panel 4"),
        }
        layout = MultiPanel.create_grid(panels, rows=2, cols=2)
        assert layout is not None

    def test_layout_create_dashboard_with_footer(self):
        """Test dashboard layout with footer."""
        header = Text("Header")
        sidebar = Text("Sidebar")
        main = Text("Main")
        footer = Text("Footer")
        layout = MultiPanel.create_dashboard(header, sidebar, main, footer)
        assert layout is not None

    def test_layout_create_dashboard_without_footer(self):
        """Test dashboard layout without footer."""
        header = Text("Header")
        sidebar = Text("Sidebar")
        main = Text("Main")
        layout = MultiPanel.create_dashboard(header, sidebar, main)
        assert layout is not None

    def test_layout_update_panel(self):
        """Test updating named panel."""
        header = Text("Header")
        sidebar = Text("Sidebar")
        main = Text("Main")
        layout = MultiPanel.create_dashboard(header, sidebar, main)

        new_main = Text("Updated Main")
        layout.update_panel("main", new_main)
        # Should not raise error

    def test_layout_render(self):
        """Test layout renders without error."""
        layout = MultiPanel()
        layout.update(Text("Content"))
        rendered = layout.__rich__()
        assert rendered is not None
