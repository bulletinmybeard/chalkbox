from chalkbox import Bar


class TestBar:
    """Tests for Bar component."""

    def test_bar_creation(self):
        """Test basic bar creation."""
        bar = Bar(50, 100)
        assert bar is not None
        assert bar.completed == 50
        assert bar.total == 100

    def test_bar_render(self):
        """Test bar renders without error."""
        bar = Bar(75, 100, width=40)
        renderable = bar.__rich__()
        assert renderable is not None

    def test_bar_percentage(self):
        """Test percentage factory method."""
        bar = Bar.percentage(75)
        assert bar.completed == 75
        assert bar.total == 100

    def test_bar_percentage_clamping(self):
        """Test percentage clamping to 0-100."""
        bar_low = Bar.percentage(-10)
        assert bar_low.completed == 0

        bar_high = Bar.percentage(150)
        assert bar_high.completed == 100

    def test_bar_fraction(self):
        """Test fraction factory method."""
        bar = Bar.fraction(512, 1024)
        assert bar.completed == 512
        assert bar.total == 1024

    def test_bar_from_ratio(self):
        """Test ratio factory method."""
        bar = Bar.from_ratio(0.75)
        assert bar.completed == 75
        assert bar.total == 100

    def test_bar_ratio_clamping(self):
        """Test ratio clamping to 0.0-1.0."""
        bar_low = Bar.from_ratio(-0.5)
        assert bar_low.completed == 0

        bar_high = Bar.from_ratio(1.5)
        assert bar_high.completed == 100

    def test_bar_indeterminate(self):
        """Test indeterminate bar creation."""
        bar = Bar.indeterminate()
        assert bar.total is None
        assert bar.pulse is True

    def test_bar_severity_styling(self):
        """Test severity-based styling."""
        bar_success = Bar.percentage(50, severity="success")
        assert bar_success is not None

        bar_warning = Bar.percentage(75, severity="warning")
        assert bar_warning is not None

        bar_error = Bar.percentage(95, severity="error")
        assert bar_error is not None

    def test_bar_width(self):
        """Test custom width."""
        bar = Bar(50, 100, width=20)
        assert bar.width == 20

    def test_bar_negative_completed_failsafe(self):
        """Test fail-safe for negative completed value."""
        bar = Bar(-10, 100)
        assert bar.completed == 0

    def test_bar_zero_total_failsafe(self):
        """Test fail-safe for zero/negative total."""
        bar = Bar(50, 0)
        assert bar.total is None  # Treated as indeterminate

        bar2 = Bar(50, -10)
        assert bar2.total is None  # Treated as indeterminate

    def test_bar_negative_width_failsafe(self):
        """Test fail-safe for negative width."""
        bar = Bar(50, 100, width=-5)
        assert bar.width == 40  # Falls back to default

    def test_bar_custom_styles(self):
        """Test custom style parameters."""
        bar = Bar(50, 100, style="dim white", complete_style="cyan", finished_style="bright_green")
        assert bar.style == "dim white"
        assert bar.complete_style == "cyan"
        assert bar.finished_style == "bright_green"

    def test_bar_complete_detection(self):
        """Test completion detection."""
        bar_incomplete = Bar(50, 100)
        renderable = bar_incomplete.__rich__()
        assert renderable is not None

        bar_complete = Bar(100, 100)
        renderable2 = bar_complete.__rich__()
        assert renderable2 is not None

    def test_bar_print_method(self):
        """Test print method doesn't raise."""
        bar = Bar.percentage(60)
        # Should not raise
        bar.print()

    def test_bar_style_default(self):
        """Test default bar style is 'line'."""
        bar = Bar(50, 100)
        assert bar.bar_style == "line"

    def test_bar_style_block(self):
        """Test block bar style."""
        bar = Bar(50, 100, bar_style="block")
        assert bar.bar_style == "block"
        renderable = bar.__rich__()
        assert renderable is not None

    def test_bar_style_line(self):
        """Test explicit line bar style."""
        bar = Bar(50, 100, bar_style="line")
        assert bar.bar_style == "line"
        renderable = bar.__rich__()
        assert renderable is not None

    def test_bar_percentage_with_block_style(self):
        """Test percentage factory with block style."""
        bar = Bar.percentage(75, bar_style="block")
        assert bar.bar_style == "block"
        assert bar.completed == 75

    def test_bar_fraction_with_block_style(self):
        """Test fraction factory with block style."""
        bar = Bar.fraction(512, 1024, bar_style="block")
        assert bar.bar_style == "block"

    def test_bar_from_ratio_with_block_style(self):
        """Test ratio factory with block style."""
        bar = Bar.from_ratio(0.75, bar_style="block")
        assert bar.bar_style == "block"

    def test_bar_severity_with_block_style(self):
        """Test severity styling with block style."""
        bar = Bar.percentage(75, severity="warning", bar_style="block")
        assert bar.bar_style == "block"
        renderable = bar.__rich__()
        assert renderable is not None
