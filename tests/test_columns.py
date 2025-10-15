from chalkbox.components.columns import ColumnLayout


class TestColumnLayout:
    """Tests for ColumnLayout component."""

    def test_columns_creation(self):
        """Test basic column layout creation."""
        items = ["Item 1", "Item 2", "Item 3"]
        layout = ColumnLayout(items)
        assert layout.items == items
        assert layout.equal is False
        assert layout.expand is False
        assert layout.align == "left"

    def test_columns_empty(self):
        """Test empty column layout."""
        layout = ColumnLayout()
        assert layout.items == []

    def test_columns_add_item(self):
        """Test adding single item."""
        layout = ColumnLayout()
        layout.add("Item 1")
        assert len(layout.items) == 1
        assert layout.items[0] == "Item 1"

    def test_columns_add_many(self):
        """Test adding multiple items."""
        layout = ColumnLayout()
        layout.add_many(["Item 1", "Item 2", "Item 3"])
        assert len(layout.items) == 3

    def test_columns_equal_width(self):
        """Test equal width columns."""
        layout = ColumnLayout(equal=True)
        assert layout.equal is True

    def test_columns_expand(self):
        """Test expanded columns."""
        layout = ColumnLayout(expand=True)
        assert layout.expand is True

    def test_columns_custom_padding(self):
        """Test custom padding."""
        layout = ColumnLayout(padding=(1, 2))
        assert layout.padding == (1, 2)

    def test_columns_custom_alignment(self):
        """Test custom alignment."""
        layout = ColumnLayout(align="center")
        assert layout.align == "center"

    def test_columns_from_list(self):
        """Test from_list factory method."""
        items = ["A", "B", "C"]
        layout = ColumnLayout.from_list(items, equal=True)
        assert layout.items == items
        assert layout.equal is True

    def test_columns_from_strings(self):
        """Test from_strings factory method."""
        strings = ["Text 1", "Text 2"]
        layout = ColumnLayout.from_strings(strings, style="bold")
        assert len(layout.items) == 2

    def test_columns_from_dict(self):
        """Test from_dict factory method."""
        data = {"key1": "value1", "key2": "value2"}
        layout = ColumnLayout.from_dict(data)
        assert len(layout.items) == 2
        assert layout.equal is True

    def test_columns_grid(self):
        """Test grid factory method."""
        items = ["1", "2", "3", "4", "5", "6"]
        layout = ColumnLayout.grid(items, columns=3)
        assert layout.items == items
        assert layout.equal is True
        assert layout.expand is True

    def test_columns_render(self):
        """Test column layout renders without error."""
        items = ["Item 1", "Item 2"]
        layout = ColumnLayout(items)
        rendered = layout.__rich__()
        assert rendered is not None

    def test_columns_render_empty(self):
        """Test empty column layout renders without error."""
        layout = ColumnLayout()
        rendered = layout.__rich__()
        assert rendered is not None
