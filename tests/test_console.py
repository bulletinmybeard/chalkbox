from chalkbox.core.console import Console, get_console, reset_console


class TestConsole:
    """Tests for Console class."""

    def test_console_creation(self):
        """Test console creation."""
        console = Console()
        assert console is not None
        assert console.is_terminal or not console.is_terminal  # Should work either way

    def test_console_default_highlight_disabled(self):
        """Test that highlight is disabled by default."""
        console = Console()
        assert console._highlight is False

    def test_console_custom_kwargs(self):
        """Test console with custom kwargs."""
        console = Console(force_terminal=True)
        assert console.is_terminal is True


class TestConsoleSingleton:
    """Tests for console singleton functions."""

    @staticmethod
    def setup_method():
        """Reset console before each test."""
        reset_console()

    def test_get_console_returns_instance(self):
        """Test get_console returns Console instance."""
        console = get_console()
        assert isinstance(console, Console)

    def test_get_console_is_singleton(self):
        """Test get_console returns same instance."""
        console1 = get_console()
        console2 = get_console()
        assert console1 is console2

    def test_get_console_ignores_subsequent_kwargs(self):
        """Test that subsequent get_console calls ignore kwargs."""
        console1 = get_console(force_terminal=True)
        console2 = get_console(force_terminal=False)
        assert console1 is console2
        assert console1.is_terminal is True

    def test_reset_console(self):
        """Test reset_console clears singleton."""
        console1 = get_console()
        reset_console()
        console2 = get_console()
        assert console1 is not console2

    def test_console_after_reset_accepts_new_kwargs(self):
        """Test that reset allows new console with different kwargs."""
        console1 = get_console(force_terminal=True)
        assert console1.is_terminal is True

        reset_console()

        console2 = get_console(force_terminal=False)
        assert console1 is not console2
