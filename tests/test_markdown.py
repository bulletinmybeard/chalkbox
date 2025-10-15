from chalkbox.components.markdown import Markdown


class TestMarkdown:
    """Tests for Markdown component."""

    def test_markdown_creation(self):
        """Test basic markdown creation."""
        text = "# Hello World"
        md = Markdown(text)
        assert md.markdown_text == text
        assert md.code_theme == "monokai"

    def test_markdown_custom_code_theme(self):
        """Test markdown with custom code theme."""
        md = Markdown("test", code_theme="vim")
        assert md.code_theme == "vim"

    def test_markdown_custom_justify(self):
        """Test markdown with custom justification."""
        md = Markdown("test", justify="center")
        assert md.justify == "center"

    def test_markdown_heading_factory(self):
        """Test heading factory method."""
        md = Markdown.heading("Test Heading", level=2)
        assert "## Test Heading" in md.markdown_text

    def test_markdown_heading_level_bounds(self):
        """Test heading level is bounded between 1 and 6."""
        md1 = Markdown.heading("Test", level=0)  # Should become 1
        assert md1.markdown_text == "# Test"

        md6 = Markdown.heading("Test", level=10)  # Should become 6
        assert "######" in md6.markdown_text

    def test_markdown_from_list_unordered(self):
        """Test unordered list factory."""
        items = ["Item 1", "Item 2", "Item 3"]
        md = Markdown.from_list(items)
        assert "- Item 1" in md.markdown_text
        assert "- Item 2" in md.markdown_text

    def test_markdown_from_list_ordered(self):
        """Test ordered list factory."""
        items = ["First", "Second", "Third"]
        md = Markdown.from_list(items, ordered=True)
        assert "1. First" in md.markdown_text
        assert "2. Second" in md.markdown_text

    def test_markdown_table_factory(self):
        """Test table factory method."""
        headers = ["Name", "Age"]
        rows = [["Alice", "30"], ["Bob", "25"]]
        md = Markdown.table(headers, rows)
        assert "Name" in md.markdown_text
        assert "Age" in md.markdown_text
        assert "Alice" in md.markdown_text
        assert "---" in md.markdown_text

    def test_markdown_code_block_factory(self):
        """Test code block factory method."""
        code = 'print("Hello")'
        md = Markdown.code_block(code, language="python")
        assert "```python" in md.markdown_text
        assert code in md.markdown_text

    def test_markdown_quote_factory(self):
        """Test quote factory method."""
        text = "This is a quote"
        md = Markdown.quote(text)
        assert "> This is a quote" in md.markdown_text

    def test_markdown_multiline_quote(self):
        """Test multiline quote."""
        text = "Line 1\nLine 2"
        md = Markdown.quote(text)
        assert "> Line 1" in md.markdown_text
        assert "> Line 2" in md.markdown_text

    def test_markdown_render(self):
        """Test markdown renders without error."""
        md = Markdown("# Test")
        rendered = md.__rich__()
        assert rendered is not None
