from chalkbox.components.code import CodeBlock


class TestCodeBlock:
    """Tests for CodeBlock component."""

    def test_code_creation(self):
        """Test basic code block creation."""
        code = 'print("Hello, World!")'
        block = CodeBlock(code)
        assert block.code == code
        assert block.language == "python"
        assert block.theme_name == "monokai"
        assert block.line_numbers is True

    def test_code_custom_language(self):
        """Test code block with custom language."""
        code = 'console.log("test");'
        block = CodeBlock(code, language="javascript")
        assert block.language == "javascript"

    def test_code_custom_theme(self):
        """Test code block with custom theme."""
        code = "# Test"
        block = CodeBlock(code, theme="vim")
        assert block.theme_name == "vim"

    def test_code_no_line_numbers(self):
        """Test code block without line numbers."""
        code = "test code"
        block = CodeBlock(code, line_numbers=False)
        assert block.line_numbers is False

    def test_code_highlight_lines(self):
        """Test code block with highlighted lines."""
        code = "line 1\nline 2\nline 3"
        block = CodeBlock(code, highlight_lines={2})
        assert block.highlight_lines == {2}

    def test_code_python_factory(self):
        """Test Python factory method."""
        code = 'print("test")'
        block = CodeBlock.python(code)
        assert block.language == "python"
        assert block.code == code

    def test_code_javascript_factory(self):
        """Test JavaScript factory method."""
        code = 'console.log("test");'
        block = CodeBlock.javascript(code)
        assert block.language == "javascript"

    def test_code_json_factory(self):
        """Test JSON factory method."""
        code = '{"key": "value"}'
        block = CodeBlock.json(code)
        assert block.language == "json"

    def test_code_bash_factory(self):
        """Test Bash factory method."""
        code = "echo 'test'"
        block = CodeBlock.bash(code)
        assert block.language == "bash"

    def test_code_sql_factory(self):
        """Test SQL factory method."""
        code = "SELECT * FROM users;"
        block = CodeBlock.sql(code)
        assert block.language == "sql"

    def test_code_yaml_factory(self):
        """Test YAML factory method."""
        code = "key: value"
        block = CodeBlock.yaml(code)
        assert block.language == "yaml"

    def test_code_markdown_factory(self):
        """Test Markdown factory method."""
        code = "# Heading"
        block = CodeBlock.markdown(code)
        assert block.language == "markdown"

    def test_code_diff_factory(self):
        """Test diff factory method."""
        code = "+ added line\n- removed line"
        block = CodeBlock.diff(code)
        assert block.language == "diff"

    def test_code_render(self):
        """Test code block renders without error."""
        code = 'print("test")'
        block = CodeBlock(code)
        rendered = block.__rich__()
        assert rendered is not None
