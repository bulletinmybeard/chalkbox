from chalkbox.components.status import Status, status


class TestStatus:
    """Tests for Status component."""

    def test_status_creation(self):
        """Test basic status creation."""
        st = Status("Working...")
        assert st.message == "Working..."
        assert st.spinner_name == "dots"
        assert st.custom_spinner_style is None
        assert st.speed == 1.0
        assert st.refresh_per_second == 12.5

    def test_status_custom_spinner(self):
        """Test status with custom spinner."""
        st = Status("Processing...", spinner="arc")
        assert st.message == "Processing..."
        assert st.spinner_name == "arc"

    def test_status_custom_style(self):
        """Test status with custom spinner style."""
        st = Status("Loading...", spinner_style="bold green")
        assert st.custom_spinner_style == "bold green"

    def test_status_custom_speed(self):
        """Test status with custom speed."""
        st = Status("Fast loading...", speed=2.0)
        assert st.speed == 2.0

    def test_status_show_factory(self):
        """Test show factory method."""
        st = Status.show("Quick status", spinner="line")
        assert st.message == "Quick status"
        assert st.spinner_name == "line"

    def test_status_convenience_function(self):
        """Test status convenience function."""
        st = status("Test message", spinner="dots")
        assert isinstance(st, Status)
        assert st.message == "Test message"
        assert st.spinner_name == "dots"
