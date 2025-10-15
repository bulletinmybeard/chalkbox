from chalkbox.components.json_view import JsonView


class TestJsonView:
    """Tests for JsonView component."""

    def test_json_from_dict(self):
        """Test JSON view from dictionary."""
        data = {"key": "value", "number": 42}
        view = JsonView(data)
        assert view.data == data
        assert view.indent == 2

    def test_json_from_list(self):
        """Test JSON view from list."""
        data = [1, 2, 3, "test"]
        view = JsonView(data)
        assert view.data == data

    def test_json_from_string(self):
        """Test JSON view from string."""
        json_str = '{"key": "value"}'
        view = JsonView(json_str)
        assert view.data == json_str

    def test_json_custom_indent(self):
        """Test JSON view with custom indentation."""
        data = {"key": "value"}
        view = JsonView(data, indent=4)
        assert view.indent == 4

    def test_json_sort_keys(self):
        """Test JSON view with sorted keys."""
        data = {"z": 1, "a": 2}
        view = JsonView(data, sort_keys=True)
        assert view.sort_keys is True

    def test_json_from_dict_factory(self):
        """Test from_dict factory method."""
        data = {"test": "value"}
        view = JsonView.from_dict(data)
        assert view.data == data

    def test_json_from_list_factory(self):
        """Test from_list factory method."""
        data = [1, 2, 3]
        view = JsonView.from_list(data)
        assert view.data == data

    def test_json_from_string_factory(self):
        """Test from_string factory method."""
        json_str = '{"key": "value"}'
        view = JsonView.from_string(json_str)
        assert view.data == json_str

    def test_json_pretty_factory(self):
        """Test pretty factory method."""
        data = {"key": "value"}
        view = JsonView.pretty(data)
        assert view.indent == 4
        assert view.sort_keys is True

    def test_json_compact_factory(self):
        """Test compact factory method."""
        data = {"key": "value"}
        view = JsonView.compact(data)
        assert view.indent is None

    def test_json_to_string(self):
        """Test converting to string."""
        data = {"key": "value"}
        view = JsonView(data)
        json_str = view.to_string()
        assert "key" in json_str
        assert "value" in json_str

    def test_json_to_dict(self):
        """Test converting to dict."""
        json_str = '{"key": "value"}'
        view = JsonView(json_str)
        result = view.to_dict()
        assert isinstance(result, dict)
        assert result["key"] == "value"

    def test_json_render(self):
        """Test JSON view renders without error."""
        data = {"test": "data"}
        view = JsonView(data)
        rendered = view.__rich__()
        assert rendered is not None
