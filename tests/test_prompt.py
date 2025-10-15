import pytest

from chalkbox.components.prompt import Confirm, Input, NumberInput, Select


class TestInput:
    """Tests for Input prompt component."""

    def test_input_creation(self):
        """Test basic input prompt creation."""
        prompt = Input("Enter name")
        assert prompt.prompt == "Enter name"
        assert prompt.default is None
        assert prompt.password is False

    def test_input_with_default(self):
        """Test input with default value."""
        prompt = Input("Enter name", default="John")
        assert prompt.default == "John"

    def test_input_with_choices(self):
        """Test input with choices."""
        choices = ["option1", "option2", "option3"]
        prompt = Input("Select option", choices=choices)
        assert prompt.choices == choices

    def test_input_password_mode(self):
        """Test password mode."""
        prompt = Input("Enter password", password=True)
        assert prompt.password is True


class TestConfirm:
    """Tests for Confirm prompt component."""

    def test_confirm_creation(self):
        """Test basic confirmation prompt creation."""
        prompt = Confirm("Continue?")
        assert prompt.prompt == "Continue?"
        assert prompt.default is False

    def test_confirm_with_default_true(self):
        """Test confirmation with default True."""
        prompt = Confirm("Proceed?", default=True)
        assert prompt.default is True

    def test_confirm_hide_default(self):
        """Test hiding default value."""
        prompt = Confirm("Continue?", show_default=False)
        assert prompt.show_default is False


class TestSelect:
    """Tests for Select prompt component."""

    def test_select_creation(self):
        """Test basic selection prompt creation."""
        choices = ["red", "blue", "green"]
        prompt = Select("Choose color", choices)
        assert prompt.prompt == "Choose color"
        assert prompt.choices == choices

    def test_select_with_default(self):
        """Test selection with custom default."""
        choices = ["a", "b", "c"]
        prompt = Select("Choose", choices, default="b")
        assert prompt.default == "b"

    def test_select_default_first_choice(self):
        """Test selection defaults to first choice."""
        choices = ["first", "second", "third"]
        prompt = Select("Choose", choices)
        assert prompt.default == "first"

    def test_select_case_sensitive(self):
        """Test case-sensitive selection."""
        choices = ["Yes", "No"]
        prompt = Select("Confirm", choices, case_sensitive=True)
        assert prompt.case_sensitive is True

    def test_select_empty_choices_raises_error(self):
        """Test that empty choices raises ValueError."""
        with pytest.raises(ValueError, match="at least one choice"):
            Select("Choose", [])


class TestNumberInput:
    """Tests for NumberInput prompt component."""

    def test_number_input_creation(self):
        """Test basic number input creation."""
        prompt = NumberInput("Enter age")
        assert prompt.prompt == "Enter age"
        assert prompt.default is None
        assert prompt.integer_only is False

    def test_number_input_with_default(self):
        """Test number input with default."""
        prompt = NumberInput("Enter value", default=42)
        assert prompt.default == 42

    def test_number_input_with_range(self):
        """Test number input with min/max range."""
        prompt = NumberInput("Enter score", min_value=0, max_value=100)
        assert prompt.min_value == 0
        assert prompt.max_value == 100

    def test_number_input_integer_only(self):
        """Test integer-only number input."""
        prompt = NumberInput("Enter count", integer_only=True)
        assert prompt.integer_only is True

    def test_number_input_validation(self):
        """Test number input validation."""
        prompt = NumberInput("Enter", min_value=10, max_value=20)
        assert prompt._validate(15) is True
        assert prompt._validate(5) is False
        assert prompt._validate(25) is False
