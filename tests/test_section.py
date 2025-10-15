from rich.text import Text

from chalkbox import Section


class TestSection:
    """Tests for Section component."""

    def test_section_creation(self):
        """Test basic section creation."""
        section = Section("Test Section", subtitle="Subtitle")
        assert section.title == "Test Section"
        assert section.subtitle == "Subtitle"

    def test_section_content(self):
        """Test adding content to section."""
        section = Section("Test")
        section.add_text("Line 1")
        section.add_text("Line 2", style="bold")
        section.add_spacing(2)

        assert len(section._content) == 4  # 2 text + 2 spacing

    def test_section_collapsible(self):
        """Test collapsible section."""
        content = Text("Content here")
        collapsed = Section.create_collapsible("Collapsible", content, collapsed=True)
        assert "▶" in collapsed.title

        expanded = Section.create_collapsible("Collapsible", content, collapsed=False)
        assert "▼" in expanded.title
