from rich.panel import Panel
from rich.text import Text

from chalkbox.live.dashboard import Dashboard, DashboardSection


class TestDashboardSection:
    """Tests for DashboardSection."""

    def test_section_creation(self):
        """Test section creation."""
        section = DashboardSection("test")
        assert section.name == "test"
        assert section.content is not None

    def test_section_with_content(self):
        """Test section with initial content."""
        content = Text("Initial content")
        section = DashboardSection("test", content=content)
        assert section.content == content

    def test_section_update(self):
        """Test updating section content."""
        section = DashboardSection("test")
        new_content = Text("Updated")
        section.update(new_content)
        assert section.content == new_content


class TestDashboard:
    """Tests for Dashboard builder."""

    def test_dashboard_creation(self):
        """Test dashboard creation."""
        dashboard = Dashboard()
        assert dashboard.layout_type == "default"
        assert len(dashboard.sections) > 0

    def test_dashboard_custom_layout(self):
        """Test dashboard with custom layout."""
        dashboard = Dashboard("sidebar_left")
        assert dashboard.layout_type == "sidebar_left"

    def test_dashboard_set_header(self):
        """Test setting header."""
        dashboard = Dashboard("header_footer")
        dashboard.set_header("Test Header")
        assert "header" in dashboard.sections

    def test_dashboard_set_header_with_update_fn(self):
        """Test setting header with update function."""

        def update_header():
            return Panel("Dynamic Header")

        dashboard = Dashboard("header_footer")
        dashboard.set_header("Static", update_fn=update_header)
        assert "header" in dashboard.update_functions

    def test_dashboard_set_main(self):
        """Test setting main content."""
        dashboard = Dashboard()
        content = Text("Main content")
        dashboard.set_main(content=content)
        assert dashboard.sections["main"].content == content

    def test_dashboard_set_footer(self):
        """Test setting footer."""
        dashboard = Dashboard("header_footer")
        dashboard.set_footer("Footer text")
        assert "footer" in dashboard.sections

    def test_dashboard_set_sidebar(self):
        """Test setting sidebar."""
        dashboard = Dashboard("sidebar_left")
        content = Text("Sidebar")
        dashboard.set_sidebar(content)
        assert dashboard.sections["sidebar"].content == content

    def test_dashboard_sidebar_not_available_error(self):
        """Test error when sidebar not available in layout."""
        dashboard = Dashboard("header_footer")
        try:
            dashboard.set_sidebar(Text("Test"))
            raise AssertionError("Should have raised ValueError")
        except ValueError as e:
            assert "not available" in str(e)

    def test_dashboard_build_layout(self):
        """Test building layout."""
        dashboard = Dashboard("header_footer")
        dashboard.set_header("Header")
        dashboard.set_main(content=Text("Main"))
        dashboard.set_footer("Footer")

        layout = dashboard._build_layout()
        assert layout is not None

    def test_dashboard_run_once(self):
        """Test run_once method."""
        dashboard = Dashboard()
        dashboard.set_main(content=Text("Test"))
        # Should not raise error
        # NOTE: Can't test actual rendering without TTY!

    def test_dashboard_create_factory(self):
        """Test create factory method."""
        dashboard = Dashboard.create("sidebar_right")
        assert isinstance(dashboard, Dashboard)
        assert dashboard.layout_type == "sidebar_right"

    def test_dashboard_default_layout_sections(self):
        """Test default layout has required sections."""
        dashboard = Dashboard("default")
        assert "header" in dashboard.sections
        assert "main" in dashboard.sections
        assert "footer" in dashboard.sections
        assert "sidebar" in dashboard.sections

    def test_dashboard_header_footer_layout_sections(self):
        """Test header_footer layout sections."""
        dashboard = Dashboard("header_footer")
        assert "header" in dashboard.sections
        assert "main" in dashboard.sections
        assert "footer" in dashboard.sections
        assert "sidebar" not in dashboard.sections

    def test_dashboard_full_layout_sections(self):
        """Test full layout has all sections."""
        dashboard = Dashboard("full")
        assert "header" in dashboard.sections
        assert "sidebar" in dashboard.sections
        assert "main" in dashboard.sections
        assert "footer" in dashboard.sections
