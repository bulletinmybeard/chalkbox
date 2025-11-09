from io import StringIO
from unittest.mock import patch

from rich.console import Console as RichConsole

from chalkbox import Table, set_theme
from chalkbox.core.console import Console


class TestTable:
    """Tests for Table component."""

    def test_table_creation(self):
        """Test basic table creation."""
        table = Table(headers=["Name", "Value"])
        table.add_row("Key1", "Value1")
        table.add_row("Key2", "Value2")

        assert len(table.headers) == 2
        assert len(table._rows) == 2

    def test_table_from_dict(self):
        """Test creating table from dictionary."""
        data = {"key1": "value1", "key2": "value2"}
        table = Table.from_dict(data)

        assert len(table.headers) == 2
        assert len(table._rows) == 2

    def test_table_from_list_of_dicts(self):
        """Test creating table from list of dicts."""
        data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
        ]
        table = Table.from_list_of_dicts(data)

        assert "name" in table.headers
        assert "age" in table.headers
        assert len(table._rows) == 2

    def test_table_with_severity(self):
        """Test table with severity styling."""
        table = Table(headers=["Status", "Message"], row_styles="severity")
        table.add_row("Success", "All good", severity="success")
        table.add_row("Error", "Failed", severity="error")

        assert table._row_severities[0] == "success"
        assert table._row_severities[1] == "error"


class TestTableAutoExpand:
    """Tests for Table auto-expand functionality."""

    def test_auto_expand_narrow_table(self):
        """Auto-expand should disable expand for narrow tables (< 5 cols)."""
        table = Table(headers=["A", "B", "C"], expand="auto")
        table.add_row("1", "2", "3")

        assert table._calculate_expand() is False

    def test_auto_expand_wide_table(self):
        """Auto-expand should enable expand for wide tables (>= 5 cols)."""
        table = Table(headers=["A", "B", "C", "D", "E", "F", "G"], expand="auto")
        table.add_row("1", "2", "3", "4", "5", "6", "7")

        assert table._calculate_expand() is True

    def test_auto_expand_threshold_boundary(self):
        """Auto-expand should expand exactly at threshold."""
        table = Table(headers=["A", "B", "C", "D", "E"], expand="auto")
        assert table._calculate_expand() is True  # 5 cols >= 5 threshold

        table = Table(headers=["A", "B", "C", "D"], expand="auto")
        assert table._calculate_expand() is False  # 4 cols < 5 threshold

    def test_explicit_expand_true_overrides_auto(self):
        """Explicit expand=True should always expand."""
        table = Table(headers=list("ABCDEFGH"), expand=True)
        assert table._calculate_expand() is True  # 8 cols but forced True

    def test_explicit_expand_false_overrides_auto(self):
        """Explicit expand=False should never expand."""
        table = Table(headers=["A", "B"], expand=False)
        assert table._calculate_expand() is False  # 2 cols but forced False

    def test_auto_expand_with_dynamic_columns(self):
        """Auto-expand should work with dynamically added columns."""
        table = Table(expand="auto")
        table.add_column("Name")
        table.add_column("Value")
        table.add_column("Status")

        assert len(table.headers) == 3
        assert table._calculate_expand() is False  # 3 cols < 5

    def test_default_expand_false_unchanged(self):
        """Default expand=False behavior should remain unchanged."""
        table = Table(headers=["A", "B", "C"])
        assert table.expand is False
        assert table._calculate_expand() is False

    def test_auto_expand_empty_table(self):
        """Auto-expand with no columns should not expand (0 < 5)."""
        table = Table(expand="auto")
        assert len(table.headers) == 0
        assert table._calculate_expand() is False  # 0 cols < 5

    def test_auto_expand_single_column(self):
        """Auto-expand with single column should not expand."""
        table = Table(headers=["Value"], expand="auto")
        assert table._calculate_expand() is False  # 1 col < 5

    def test_auto_expand_renders_without_error(self):
        """Table with auto-expand should render successfully."""

        output = StringIO()
        console = Console(file=output, width=80)

        table = Table(headers=["Name", "Status"], expand="auto")
        table.add_row("Test", "Pass")

        # Should not raise exception
        console.print(table)
        result = output.getvalue()

        assert "Test" in result
        assert "Pass" in result


class TestTableResponsiveMode:
    """Tests for Table responsive mode (media query-like behavior)."""

    def test_responsive_mode_compact_terminal(self):
        """Compact terminal (< 60 cols) should never expand."""

        set_theme(table_responsive_mode=True)

        with patch.object(Console, "width", 50):
            # Wide table (7 cols >= 5 threshold)
            table = Table(headers=["A", "B", "C", "D", "E", "F", "G"], expand="auto")
            result = table._calculate_expand()

            # Should NOT expand in compact terminal
            assert result is False

        set_theme(table_responsive_mode=False)

    def test_responsive_mode_medium_terminal_narrow_table(self):
        """Medium terminal (60-80 cols) with narrow table should not expand."""

        set_theme(table_responsive_mode=True)

        with patch.object(Console, "width", 70):
            # Narrow table (3 cols < 5 threshold)
            table = Table(headers=["A", "B", "C"], expand="auto")
            result = table._calculate_expand()

            # Should NOT expand (below threshold)
            assert result is False

        set_theme(table_responsive_mode=False)

    def test_responsive_mode_medium_terminal_wide_table(self):
        """Medium terminal (60-80 cols) with wide table should return calculated width."""

        set_theme(table_responsive_mode=True)

        # Mock console width to 70 (medium)
        with patch.object(Console, "width", 70):
            # Wide table (7 cols >= 5 threshold)
            table = Table(headers=["A", "B", "C", "D", "E", "F", "G"], expand="auto")
            result = table._calculate_expand()

            # Should return int (calculated width)
            assert isinstance(result, int)
            assert result > 0
            # Should be capped at terminal_width - 4
            assert result <= 66  # 70 - 4

        set_theme(table_responsive_mode=False)

    def test_responsive_mode_wide_terminal(self):
        """Wide terminal (> 80 cols) should use threshold logic."""

        set_theme(table_responsive_mode=True)

        # Mock console width to 120 (wide)
        with patch.object(Console, "width", 120):
            # Wide table (7 cols >= 5 threshold)
            wide_table = Table(headers=["A", "B", "C", "D", "E", "F", "G"], expand="auto")
            assert wide_table._calculate_expand() is True  # Above threshold

            # Narrow table (3 cols < 5 threshold)
            narrow_table = Table(headers=["A", "B", "C"], expand="auto")
            assert narrow_table._calculate_expand() is False  # Below threshold

        set_theme(table_responsive_mode=False)

    def test_responsive_mode_disabled(self):
        """When responsive_mode=False, should use simple threshold logic."""

        set_theme(table_responsive_mode=False)

        wide_table = Table(headers=["A", "B", "C", "D", "E", "F", "G"], expand="auto")
        assert wide_table._calculate_expand() is True

        narrow_table = Table(headers=["A", "B", "C"], expand="auto")
        assert narrow_table._calculate_expand() is False

        # Reset to default (False)
        set_theme(table_responsive_mode=False)

    def test_responsive_custom_breakpoints(self):
        """Custom breakpoints should be respected."""

        set_theme(
            table_responsive_mode=True,
            table_responsive_breakpoints={
                "compact": 50,  # < 50 cols: compact
                "medium": 70,  # 50-70 cols: medium
                "wide": 71,  # > 70 cols: wide
            }
        )

        with patch.object(Console, "width", 60):
            table = Table(headers=["A", "B", "C", "D", "E", "F", "G"], expand="auto")
            result = table._calculate_expand()

            assert isinstance(result, int)

        # Reset to defaults
        set_theme(
            table_responsive_mode=False,
            table_responsive_breakpoints={
                "compact": 60,
                "medium": 80,
                "wide": 81,
            }
        )

    def test_isinstance_bool_vs_int_check_order(self):
        """Critical: bool check must come before int check (bool is subclass of int)."""
        table = Table(headers=["Name", "Status"], expand="auto")
        result = table._calculate_expand()

        assert isinstance(result, bool)
        assert result is False

        assert isinstance(result, bool) is True  # bool check
        assert isinstance(result, int) is True  # bool is also int!

        rich_table = table.__rich__()
        assert rich_table.expand is False

    def test_responsive_renders_with_content(self):
        """Responsive tables should render with content, not empty cells."""

        output = StringIO()
        console = RichConsole(file=output, width=80)

        table = Table(headers=["Name", "Status"], expand="auto")
        table.add_row("Test", "Pass")

        console.print(table)
        result = output.getvalue()

        assert "Test" in result
        assert "Pass" in result
        assert "Name" in result
        assert "Status" in result
