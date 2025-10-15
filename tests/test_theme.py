import os
from pathlib import Path
import tempfile

import toml

from chalkbox.core.theme import Theme, get_theme, set_theme


class TestThemeCore:
    """Tests for Theme class."""

    def test_theme_initialization(self):
        """Test theme initializes with defaults."""
        theme = Theme()

        # Check default colors
        assert "primary" in theme.colors
        assert "success" in theme.colors
        assert "error" in theme.colors

        # Check default spacing
        assert "default" in theme.spacing
        assert isinstance(theme.spacing["default"], int)

        # Check default glyphs
        assert "success" in theme.glyphs
        assert "error" in theme.glyphs

    def test_theme_get_nested_values(self):
        """Test getting nested theme values."""
        theme = Theme()

        # Test valid paths
        assert theme.get("colors.primary") == "cyan"
        assert theme.get("spacing.default") == 1
        assert theme.get("glyphs.success") == "✓"

        # Test invalid paths with defaults
        assert theme.get("invalid.path") is None
        assert theme.get("invalid.path", "default") == "default"

    def test_theme_update_values(self):
        """Test updating theme values."""
        theme = Theme()

        updates = {
            "colors.primary": "magenta",
            "colors.secondary": "purple",
            "spacing.xl": 5,
            "glyphs.custom": "★",
        }

        theme.update(updates)

        assert theme.colors["primary"] == "magenta"
        assert theme.colors["secondary"] == "purple"
        assert theme.spacing["xl"] == 5
        assert theme.glyphs["custom"] == "★"

    def test_theme_from_file(self):
        """Test loading theme from TOML file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            config = {
                "colors": {
                    "primary": "blue",
                    "success": "bright_green",
                },
                "spacing": {
                    "default": 2,
                    "large": 4,
                },
                "glyphs": {
                    "success": "✓ ",
                    "error": "❌",
                },
            }
            toml.dump(config, f)
            temp_path = Path(f.name)

        try:
            theme = Theme.from_file(temp_path)

            assert theme.colors["primary"] == "blue"
            assert theme.colors["success"] == "bright_green"
            assert theme.spacing["default"] == 2
            assert theme.glyphs["success"] == "✓ "
        finally:
            temp_path.unlink()

    def test_theme_from_env(self):
        """Test creating theme from environment variables."""
        # Set environment variables
        os.environ["CHALKBOX_THEME_COLORS_PRIMARY"] = "red"
        os.environ["CHALKBOX_THEME_SPACING_DEFAULT"] = "3"
        os.environ["CHALKBOX_THEME_GLYPHS_SUCCESS"] = "✔"

        try:
            theme = Theme.from_env()

            # Only the env-specified values should be updated
            assert "red" in str(theme.colors)
            assert "3" in str(theme.spacing)
            assert "✔" in str(theme.glyphs)
        finally:
            # Clean up
            del os.environ["CHALKBOX_THEME_COLORS_PRIMARY"]
            del os.environ["CHALKBOX_THEME_SPACING_DEFAULT"]
            del os.environ["CHALKBOX_THEME_GLYPHS_SUCCESS"]

    def test_theme_get_style(self):
        """Test getting style strings for severity levels."""
        theme = Theme()

        # Test default severity styles
        assert theme.get_style("info") == theme.colors["info"]
        assert theme.get_style("success") == theme.colors["success"]
        assert theme.get_style("warning") == theme.colors["warning"]
        assert theme.get_style("error") == theme.colors["error"]

        # Test fallback
        assert theme.get_style("unknown") == theme.colors["text"]


class TestThemeGlobal:
    """Tests for global theme functions."""

    def test_get_theme_singleton(self):
        """Test get_theme returns singleton."""
        # Get theme instances
        theme1 = get_theme()
        theme2 = get_theme()

        # Should be the same instance
        assert theme1 is theme2

    def test_set_theme(self):
        """Test setting global theme."""

        # Set with instance
        custom_theme = Theme()
        custom_theme.colors["primary"] = "yellow"
        set_theme(custom_theme)

        current = get_theme()
        assert current.colors["primary"] == "yellow"

        # Set with kwargs
        set_theme(None, **{"colors.primary": "green"})
        current = get_theme()
        assert current.colors["primary"] == "green"


class TestThemeIntegration:
    """Integration tests for theme system."""

    def test_theme_with_components(self):
        """Test theme integration with components."""
        from chalkbox import Alert, set_theme

        # Set custom theme
        set_theme(
            None,
            **{
                "colors.success": "bright_green",
                "glyphs.success": "✓ ",
            },
        )

        # Create component
        alert = Alert.success("Test message")

        # Component should use theme
        assert alert.theme.colors["success"] == "bright_green"
        assert alert.theme.glyphs["success"] == "✓ "

    def test_theme_precedence(self):
        """Test configuration precedence."""
        # This would test: call-time > env > file > defaults
        # But requires more complex setup with actual file system
        pass
