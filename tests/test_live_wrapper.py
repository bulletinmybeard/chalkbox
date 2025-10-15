from rich.text import Text

from chalkbox.live.wrapper import LiveComponent, LiveLayout, LiveTable


class TestLiveComponent:
    """Tests for LiveComponent wrapper."""

    def test_live_component_creation(self):
        """Test live component creation."""
        component = Text("Test")
        live = LiveComponent(component)
        assert live.component == component
        assert live.refresh_per_second == 2
        assert live.screen is False
        assert live.transient is False

    def test_live_component_custom_settings(self):
        """Test live component with custom settings."""
        component = Text("Test")
        live = LiveComponent(component, refresh_per_second=4, screen=True, transient=True)
        assert live.refresh_per_second == 4
        assert live.screen is True
        assert live.transient is True

    def test_live_component_with_update_fn(self):
        """Test live component with update function."""

        def update_fn():
            return Text("Updated")

        component = Text("Original")
        live = LiveComponent(component, update_fn=update_fn)
        assert live.update_fn is update_fn

    def test_live_component_get_renderable(self):
        """Test getting renderable from component."""
        component = Text("Test")
        live = LiveComponent(component)
        renderable = live._get_renderable()
        assert renderable is not None

    def test_live_component_wrap_factory(self):
        """Test wrap factory method."""
        component = Text("Test")
        live = LiveComponent.wrap(component, refresh_per_second=3)
        assert isinstance(live, LiveComponent)
        assert live.refresh_per_second == 3


class TestLiveTable:
    """Tests for LiveTable wrapper."""

    def test_live_table_creation(self):
        """Test live table creation."""
        live_table = LiveTable()
        assert live_table is not None
        assert live_table._wrapper is not None

    def test_live_table_with_update_fn(self):
        """Test live table with update function."""

        def update_fn():
            from chalkbox import Table

            return Table(headers=["Name"])

        live_table = LiveTable(update_fn=update_fn)
        assert live_table.update_fn is update_fn

    def test_live_table_custom_refresh_rate(self):
        """Test live table with custom refresh rate."""
        live_table = LiveTable(refresh_per_second=4)
        assert live_table._wrapper.refresh_per_second == 4

    def test_live_table_screen_mode(self):
        """Test live table with screen mode."""
        live_table = LiveTable(screen=True)
        assert live_table._wrapper.screen is True


class TestLiveLayout:
    """Tests for LiveLayout wrapper."""

    def test_live_layout_creation(self):
        """Test live layout creation."""
        live_layout = LiveLayout()
        assert live_layout is not None
        assert live_layout._wrapper is not None

    def test_live_layout_default_screen_mode(self):
        """Test live layout defaults to screen mode."""
        live_layout = LiveLayout()
        assert live_layout._wrapper.screen is True

    def test_live_layout_with_update_fn(self):
        """Test live layout with update function."""

        def update_fn():
            from rich.layout import Layout

            return Layout()

        live_layout = LiveLayout(update_fn=update_fn)
        assert live_layout.update_fn is update_fn

    def test_live_layout_custom_refresh_rate(self):
        """Test live layout with custom refresh rate."""
        live_layout = LiveLayout(refresh_per_second=5)
        assert live_layout._wrapper.refresh_per_second == 5

    def test_live_layout_disable_screen_mode(self):
        """Test disabling screen mode."""
        live_layout = LiveLayout(screen=False)
        assert live_layout._wrapper.screen is False
