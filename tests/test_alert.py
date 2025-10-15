from chalkbox import Alert


class TestAlert:
    """Tests for Alert component."""

    def test_alert_levels(self):
        """Test alert creation with different levels."""
        info = Alert.info("Info message")
        assert info.level == "info"
        assert info.message == "Info message"

        success = Alert.success("Success message")
        assert success.level == "success"

        warning = Alert.warning("Warning message")
        assert warning.level == "warning"

        error = Alert.error("Error message")
        assert error.level == "error"

    def test_alert_with_details(self):
        """Test alert with details."""
        alert = Alert("Main message", level="warning", details="Additional details here")
        assert alert.message == "Main message"
        assert alert.details == "Additional details here"

    def test_alert_render(self):
        """Test alert renders without error."""
        alert = Alert.success("Test message")
        # Should be renderable
        rendered = alert.__rich__()
        assert rendered is not None
