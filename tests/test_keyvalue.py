from chalkbox import KeyValue


class TestKeyValue:
    """Tests for KeyValue component."""

    def test_kv_creation(self):
        """Test basic key-value creation."""
        data = {"key1": "value1", "key2": "value2"}
        kv = KeyValue(data)

        assert kv.data == data

    def test_kv_secret_masking(self):
        """Test secret key masking."""
        data = {
            "username": "admin",
            "password": "secret123",
            "api_key": "sk-1234567890",
        }
        kv = KeyValue(data, mask_secrets=True)

        assert kv._should_mask("password")
        assert kv._should_mask("api_key")
        assert not kv._should_mask("username")

    def test_kv_format_value(self):
        """Test value formatting."""
        kv = KeyValue()

        # Test None (use `name` instead of `key` to avoid masking)
        assert kv._format_value("name", None) == "(empty)"

        # Test boolean
        assert kv._format_value("name", True) == "✓"
        assert kv._format_value("name", False) == "✖"

        # Test list
        assert kv._format_value("name", []) == "(empty list)"
        assert kv._format_value("name", [1, 2, 3]) == "1, 2, 3"
        assert "... (5 items)" in kv._format_value("name", [1, 2, 3, 4, 5])

    def test_kv_reveal_secrets(self):
        """Test revealing secrets with reveal flag."""
        data = {"password": "secret123"}

        kv_masked = KeyValue(data, mask_secrets=True, reveal=False)
        assert kv_masked._should_mask("password")

        kv_revealed = KeyValue(data, mask_secrets=True, reveal=True)
        assert not kv_revealed._should_mask("password")
