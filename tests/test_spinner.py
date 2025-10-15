from chalkbox.components.spinner import Spinner


class TestSpinner:
    """Tests for Spinner component."""

    def test_spinner_creation(self):
        """Test basic spinner creation."""
        spinner = Spinner("Loading data...")
        assert spinner.text == "Loading data..."
        assert spinner.spinner_style == "dots"
        assert spinner.transient is True
        assert spinner._status is None

    def test_spinner_custom_style(self):
        """Test spinner with custom style."""
        spinner = Spinner("Processing...", spinner="arc")
        assert spinner.text == "Processing..."
        assert spinner.spinner_style == "arc"

    def test_spinner_success_method(self):
        """Test marking spinner as successful."""
        spinner = Spinner("Loading...")
        spinner.success("Completed!")

        assert spinner._status is not None
        assert "Completed!" in str(spinner._status)

    def test_spinner_error_method(self):
        """Test marking spinner as failed."""
        spinner = Spinner("Loading...")
        spinner.error("Operation failed")

        assert spinner._status is not None
        assert "Operation failed" in str(spinner._status)

    def test_spinner_warning_method(self):
        """Test marking spinner with warning."""
        spinner = Spinner("Processing...")
        spinner.warning("Partial success")

        assert spinner._status is not None
        assert "Partial success" in str(spinner._status)

    def test_spinner_default_messages(self):
        """Test default messages for status methods."""
        spinner = Spinner("Loading data...")

        # Success with no text uses original text
        spinner.success()
        assert "Loading data..." in str(spinner._status)

        # Error with no text prepends "Failed:"
        spinner2 = Spinner("Saving...")
        spinner2.error()
        assert "Failed:" in str(spinner2._status)
        assert "Saving..." in str(spinner2._status)
