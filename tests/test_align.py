from rich.panel import Panel

from chalkbox import Alert, Align


class TestAlign:
    """Tests for Align component."""

    def test_align_creation(self):
        """Test basic align creation."""
        alert = Alert.info("Test")
        align = Align(alert, align="center")
        assert align is not None
        assert align.align == "center"

    def test_align_render(self):
        """Test align renders without error."""
        alert = Alert.success("Test")
        align = Align(alert, align="center")
        renderable = align.__rich__()
        assert renderable is not None

    def test_align_left(self):
        """Test left alignment factory."""
        alert = Alert.info("Test")
        align = Align.left(alert)
        assert align.align == "left"
        assert align.vertical is None

    def test_align_center(self):
        """Test center alignment factory."""
        alert = Alert.info("Test")
        align = Align.center(alert)
        assert align.align == "center"
        assert align.vertical is None

    def test_align_right(self):
        """Test right alignment factory."""
        alert = Alert.info("Test")
        align = Align.right(alert)
        assert align.align == "right"
        assert align.vertical is None

    def test_align_middle(self):
        """Test vertical middle alignment."""
        alert = Alert.info("Test")
        align = Align.middle(alert)
        assert align.vertical == "middle"
        assert align.align == "center"  # Default horizontal

    def test_align_top(self):
        """Test vertical top alignment."""
        alert = Alert.info("Test")
        align = Align.top(alert)
        assert align.vertical == "top"
        assert align.align == "center"  # Default horizontal

    def test_align_bottom(self):
        """Test vertical bottom alignment."""
        alert = Alert.info("Test")
        align = Align.bottom(alert)
        assert align.vertical == "bottom"
        assert align.align == "center"  # Default horizontal

    def test_align_with_vertical(self):
        """Test combining horizontal and vertical alignment."""
        alert = Alert.info("Test")
        align = Align.left(alert, vertical="middle")
        assert align.align == "left"
        assert align.vertical == "middle"

    def test_align_width_and_height(self):
        """Test width and height parameters."""
        alert = Alert.info("Test")
        align = Align(alert, align="center", width=80, height=10)
        assert align.width == 80
        assert align.height == 10

    def test_align_style_parameter(self):
        """Test style parameter."""
        alert = Alert.info("Test")
        align = Align(alert, style="cyan")
        assert align.style == "cyan"

    def test_align_pad_parameter(self):
        """Test pad parameter."""
        alert = Alert.info("Test")
        align = Align(alert, pad=False)
        assert align.pad is False

    def test_align_invalid_horizontal_failsafe(self):
        """Test fail-safe for invalid horizontal alignment."""
        alert = Alert.info("Test")
        align = Align(alert, align="invalid")  # type: ignore[arg-type]
        assert align.align == "left"  # Falls back to default

    def test_align_invalid_vertical_failsafe(self):
        """Test fail-safe for invalid vertical alignment."""
        alert = Alert.info("Test")
        align = Align(alert, vertical="invalid")  # type: ignore[arg-type]
        assert align.vertical is None  # Falls back to None

    def test_align_with_panel(self):
        """Test aligning Rich Panel."""
        panel = Panel("Content", title="Test")
        align = Align.center(panel)
        renderable = align.__rich__()
        assert renderable is not None

    def test_align_with_various_renderables(self):
        """Test align works with various renderables."""
        # With Alert
        alert = Alert.success("Test")
        align1 = Align.center(alert)
        assert align1.__rich__() is not None

        # With string
        align2 = Align.center("Simple text")
        assert align2.__rich__() is not None

        # With Panel
        panel = Panel("Content")
        align3 = Align.right(panel)
        assert align3.__rich__() is not None

    def test_align_print_method(self):
        """Test print method doesn't raise."""
        alert = Alert.info("Test")
        align = Align.center(alert)
        # Should not raise
        align.print()

    def test_align_middle_with_custom_horizontal(self):
        """Test middle alignment with custom horizontal."""
        alert = Alert.info("Test")

        align_left = Align.middle(alert, align="left")
        assert align_left.vertical == "middle"
        assert align_left.align == "left"

        align_right = Align.middle(alert, align="right")
        assert align_right.vertical == "middle"
        assert align_right.align == "right"

    def test_align_composability(self):
        """Test align is composable with other components."""
        alert = Alert.warning("Test warning")
        align = Align.center(alert)
        # Should render without error
        renderable = align.__rich__()
        assert renderable is not None
