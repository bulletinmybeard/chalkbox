import os
from pathlib import Path
import tempfile

import toml

from chalkbox.core.theme import ColorsConfig, SpacingConfig, Theme, get_theme, set_theme


class TestThemeCore:
    """Tests for Theme class."""

    def test_theme_initialization(self):
        """Test theme initializes with defaults."""
        theme = Theme()

        # Check default colors (Pydantic models support hasattr)
        assert hasattr(theme.colors, "primary")
        assert hasattr(theme.colors, "success")
        assert hasattr(theme.colors, "error")
        assert theme.colors.primary == "cyan"

        # Check default spacing
        assert hasattr(theme.spacing, "default")
        assert isinstance(theme.spacing.default, int)

        # Check default glyphs
        assert hasattr(theme.glyphs, "success")
        assert hasattr(theme.glyphs, "error")

    def test_theme_nested_values(self):
        """Test accessing nested theme values."""
        theme = Theme()

        # Test direct attribute access (Pydantic style)
        assert theme.colors.primary == "cyan"
        assert theme.spacing.default == 1
        assert theme.glyphs.success == "✓"

        # Test with getattr for dynamic access
        assert theme.colors.primary == "cyan"
        assert theme.spacing.default == 1
        assert theme.glyphs.success == "✓"

        # Test invalid attributes with defaults
        assert getattr(theme.colors, "nonexistent", "default") == "default"

    def test_theme_pydantic_validation(self):
        """Test Pydantic validation for theme configs."""
        # Valid config
        theme = Theme(
            colors=ColorsConfig(primary="magenta", secondary="purple"),
            spacing=SpacingConfig(xl=5),
        )

        assert theme.colors.primary == "magenta"
        assert theme.colors.secondary == "purple"
        assert theme.spacing.xl == 5

        # Test that extra fields are forbidden (strict validation)
        from pydantic import ValidationError

        try:
            ColorsConfig(primary="cyan", custom="red")
            raise AssertionError("Should have raised ValidationError for extra field")
        except ValidationError as e:
            assert "extra" in str(e).lower() or "forbidden" in str(e).lower()

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
                    "lg": 4,
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

            assert theme.colors.primary == "blue"
            assert theme.colors.success == "bright_green"
            assert theme.spacing.default == 2
            assert theme.glyphs.success == "✓ "
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

            # Check that env-specified values are updated
            assert theme.colors.primary == "red"
            assert theme.spacing.default == 3
            assert theme.glyphs.success == "✔"
        finally:
            # Clean up
            del os.environ["CHALKBOX_THEME_COLORS_PRIMARY"]
            del os.environ["CHALKBOX_THEME_SPACING_DEFAULT"]
            del os.environ["CHALKBOX_THEME_GLYPHS_SUCCESS"]

    def test_theme_get_style(self):
        """Test getting style strings for severity levels."""
        theme = Theme()

        # Test default severity styles
        assert theme.get_style("info") == theme.colors.info
        assert theme.get_style("success") == theme.colors.success
        assert theme.get_style("warning") == theme.colors.warning
        assert theme.get_style("error") == theme.colors.error

        # Test fallback
        assert theme.get_style("unknown") == theme.colors.text

    def test_theme_model_dump(self):
        """Test Pydantic model_dump method."""
        theme = Theme()

        # Test that we can dump the model to dict
        data = theme.model_dump()

        assert "colors" in data
        assert "spacing" in data
        assert "glyphs" in data
        assert "borders" in data

        # Check nested structure
        assert data["colors"]["primary"] == "cyan"
        assert data["spacing"]["default"] == 1


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
        custom_theme.colors = ColorsConfig(primary="yellow")
        set_theme(custom_theme)

        current = get_theme()
        assert current.colors.primary == "yellow"

        # Set with kwargs (using underscore format)
        set_theme(None, colors_primary="green")
        current = get_theme()
        assert current.colors.primary == "green"


class TestThemeIntegration:
    """Integration tests for theme system."""

    def test_theme_with_components(self):
        """Test theme integration with components."""
        from chalkbox import Alert, set_theme

        # Set custom theme using underscore format
        set_theme(
            None,
            colors_success="bright_green",
            glyphs_success="✓ ",
        )

        # Create component
        alert = Alert.success("Test message")

        # Component should use theme
        assert alert.theme.colors.success == "bright_green"
        assert alert.theme.glyphs.success == "✓ "

    def test_theme_precedence(self):
        """Test configuration precedence."""
        # This would test: call-time > env > file > defaults
        # But requires more complex setup with actual file system
        pass
