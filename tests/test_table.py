from chalkbox import Table


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
