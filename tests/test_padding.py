from rich.panel import Panel

from chalkbox import Alert, Padding


class TestPadding:
    """Tests for Padding component."""

    def test_padding_creation(self):
        """Test basic padding creation."""
        alert = Alert.info("Test")
        padding = Padding(alert, pad=2)
        assert padding is not None
        assert padding.pad == 2

    def test_padding_render(self):
        """Test padding renders without error."""
        alert = Alert.success("Test")
        padding = Padding(alert, pad=1)
        renderable = padding.__rich__()
        assert renderable is not None

    def test_padding_none(self):
        """Test none (zero) padding factory."""
        alert = Alert.info("Test")
        padding = Padding.none(alert)
        assert padding.pad == 0

    def test_padding_xs(self):
        """Test extra-small padding factory."""
        alert = Alert.info("Test")
        padding = Padding.xs(alert)
        assert padding.pad == 0  # Theme default for xs

    def test_padding_small(self):
        """Test small padding factory."""
        alert = Alert.info("Test")
        padding = Padding.small(alert)
        assert padding.pad == 1  # Theme default for sm

    def test_padding_medium(self):
        """Test medium padding factory."""
        alert = Alert.info("Test")
        padding = Padding.medium(alert)
        assert padding.pad == 2  # Theme default for md

    def test_padding_large(self):
        """Test large padding factory."""
        alert = Alert.info("Test")
        padding = Padding.large(alert)
        assert padding.pad == 3  # Theme default for lg

    def test_padding_xl(self):
        """Test extra-large padding factory."""
        alert = Alert.info("Test")
        padding = Padding.xl(alert)
        assert padding.pad == 4  # Theme default for xl

    def test_padding_symmetric(self):
        """Test symmetric padding."""
        alert = Alert.info("Test")
        padding = Padding.symmetric(alert, vertical=2, horizontal=4)
        assert padding.pad == (2, 4)

    def test_padding_vertical(self):
        """Test vertical-only padding."""
        alert = Alert.info("Test")
        padding = Padding.vertical(alert, amount=3)
        assert padding.pad == (3, 0)

    def test_padding_horizontal(self):
        """Test horizontal-only padding."""
        alert = Alert.info("Test")
        padding = Padding.horizontal(alert, amount=5)
        assert padding.pad == (0, 5)

    def test_padding_custom(self):
        """Test custom padding on all sides."""
        alert = Alert.info("Test")
        padding = Padding.custom(alert, top=1, right=2, bottom=3, left=4)
        assert padding.pad == (1, 2, 3, 4)

    def test_padding_tuple_two_elements(self):
        """Test padding with 2-element tuple (vertical, horizontal)."""
        alert = Alert.info("Test")
        padding = Padding(alert, pad=(1, 2))
        assert padding.pad == (1, 2)

    def test_padding_tuple_four_elements(self):
        """Test padding with 4-element tuple (top, right, bottom, left)."""
        alert = Alert.info("Test")
        padding = Padding(alert, pad=(1, 2, 3, 4))
        assert padding.pad == (1, 2, 3, 4)

    def test_padding_negative_int_failsafe(self):
        """Test fail-safe for negative integer padding."""
        alert = Alert.info("Test")
        padding = Padding(alert, pad=-5)
        assert padding.pad == 0  # Falls back to 0

    def test_padding_negative_tuple_failsafe(self):
        """Test fail-safe for negative values in tuple."""
        alert = Alert.info("Test")
        padding = Padding(alert, pad=(-1, -2))
        assert padding.pad == (0, 0)  # Falls back to 0

    def test_padding_negative_four_tuple_failsafe(self):
        """Test fail-safe for negative values in 4-element tuple."""
        alert = Alert.info("Test")
        padding = Padding(alert, pad=(-1, -2, -3, -4))
        assert padding.pad == (0, 0, 0, 0)  # Falls back to 0

    def test_padding_invalid_tuple_length_failsafe(self):
        """Test fail-safe for invalid tuple length."""
        alert = Alert.info("Test")
        padding = Padding(alert, pad=(1, 2, 3))  # Invalid: 3 elements
        assert padding.pad == 1  # Falls back to default

    def test_padding_style_parameter(self):
        """Test style parameter."""
        alert = Alert.info("Test")
        padding = Padding(alert, pad=2, style="cyan")
        assert padding.style == "cyan"

    def test_padding_expand_parameter(self):
        """Test expand parameter."""
        alert = Alert.info("Test")
        padding = Padding(alert, pad=2, expand=False)
        assert padding.expand is False

    def test_padding_with_panel(self):
        """Test padding Rich Panel."""
        panel = Panel("Content", title="Test")
        padding = Padding(panel, pad=2)
        renderable = padding.__rich__()
        assert renderable is not None

    def test_padding_with_various_renderables(self):
        """Test padding works with various renderables."""
        # With Alert
        alert = Alert.success("Test")
        padding1 = Padding.medium(alert)
        assert padding1.__rich__() is not None

        # With string
        padding2 = Padding.small("Simple text")
        assert padding2.__rich__() is not None

        # With Panel
        panel = Panel("Content")
        padding3 = Padding.large(panel)
        assert padding3.__rich__() is not None

    def test_padding_renders_correctly(self):
        """Test padding renders correctly without errors."""
        alert = Alert.info("Test")
        padding = Padding.medium(alert)
        # Should not raise when rendering
        renderable = padding.__rich__()
        assert renderable is not None

    def test_padding_composability(self):
        """Test padding is composable with other components."""
        alert = Alert.warning("Test warning")
        padding = Padding.large(alert)
        # Should render without error
        renderable = padding.__rich__()
        assert renderable is not None

    def test_padding_default_expand(self):
        """Test default expand parameter."""
        alert = Alert.info("Test")
        padding = Padding(alert)
        assert padding.expand is True

    def test_padding_theme_integration(self):
        """Test padding uses theme spacing tokens."""
        alert = Alert.info("Test")

        # These should use theme spacing values
        pad_xs = Padding.xs(alert)
        pad_sm = Padding.small(alert)
        pad_md = Padding.medium(alert)
        pad_lg = Padding.large(alert)
        pad_xl = Padding.xl(alert)

        # All should have valid pad values from theme
        assert pad_xs.pad is not None
        assert pad_sm.pad is not None
        assert pad_md.pad is not None
        assert pad_lg.pad is not None
        assert pad_xl.pad is not None
