from chalkbox.components.divider import Divider


class TestDivider:
    """Tests for Divider component."""

    def test_divider_creation(self):
        """Test basic divider creation."""
        divider = Divider()
        assert divider.title == ""
        assert divider.align == "center"
        assert divider.characters == "─"
        assert divider.custom_style is None

    def test_divider_with_title(self):
        """Test divider with title."""
        divider = Divider("Section Title")
        assert divider.title == "Section Title"
        assert divider.align == "center"

    def test_divider_with_custom_alignment(self):
        """Test divider with custom alignment."""
        divider = Divider("Title", align="left")
        assert divider.align == "left"

    def test_divider_with_custom_characters(self):
        """Test divider with custom characters."""
        divider = Divider(characters="═")
        assert divider.characters == "═"

    def test_divider_render(self):
        """Test divider renders without error."""
        divider = Divider("Test Section")
        rendered = divider.__rich__()
        assert rendered is not None

    def test_divider_section_factory(self):
        """Test section factory method."""
        divider = Divider.section("Section Heading")
        assert divider.title == "Section Heading"
        assert divider.align == "left"

    def test_divider_separator_factory(self):
        """Test separator factory method."""
        divider = Divider.separator()
        assert divider.title == ""

    def test_divider_double_factory(self):
        """Test double-line factory method."""
        divider = Divider.double("Title")
        assert divider.characters == "═"
        assert divider.title == "Title"

    def test_divider_heavy_factory(self):
        """Test heavy-line factory method."""
        divider = Divider.heavy()
        assert divider.characters == "━"

    def test_divider_light_factory(self):
        """Test light-line factory method."""
        divider = Divider.light("Title")
        assert divider.characters == "─"

    def test_divider_dotted_factory(self):
        """Test dotted-line factory method."""
        divider = Divider.dotted()
        assert divider.characters == "·"

    def test_divider_dashed_factory(self):
        """Test dashed-line factory method."""
        divider = Divider.dashed()
        assert divider.characters == "╌"
