from chalkbox import Table, get_console


def demo_basic_usage():
    """Basic usage examples."""
    console = get_console()
    console.print("\n[bold cyan]═══ Basic Table Usage ═══[/bold cyan]\n")

    # Simple table
    console.print("[dim]Simple table:[/dim]")
    table = Table(headers=["Name", "Age", "City"])
    table.add_row("Alice", "30", "New York")
    table.add_row("Bob", "25", "San Francisco")
    table.add_row("Charlie", "35", "Chicago")
    console.print(table)
    console.print()

    # Table with title
    console.print("[dim]Table with title:[/dim]")
    table2 = Table(title="Employee Records", headers=["ID", "Name", "Department"])
    table2.add_row("101", "Alice Smith", "Engineering")
    table2.add_row("102", "Bob Jones", "Marketing")
    table2.add_row("103", "Carol White", "Sales")
    console.print(table2)


def demo_advanced_features():
    """Advanced features and options."""
    console = get_console()
    console.print("\n\n[bold cyan]═══ Advanced Features ═══[/bold cyan]\n")

    # From dictionary
    console.print("[dim]Table from dictionary:[/dim]")
    data_dict = {"host": "localhost", "port": 5432, "database": "myapp", "timeout": 30}
    table_dict = Table.from_dict(data_dict, title="Database Config")
    console.print(table_dict)
    console.print()

    # From list of dicts
    console.print("[dim]Table from list of dicts:[/dim]")
    users = [
        {"name": "Alice", "role": "Admin", "status": "Active"},
        {"name": "Bob", "role": "User", "status": "Active"},
        {"name": "Charlie", "role": "User", "status": "Inactive"},
    ]
    table_list = Table.from_list_of_dicts(users, title="Users")
    console.print(table_list)
    console.print()

    # Table with lines
    console.print("[dim]Table with row lines:[/dim]")
    table_lines = Table(
        title="Service Status", headers=["Service", "Status", "Uptime", "Port"], show_lines=True
    )
    table_lines.add_row("API", "Running", "14d 3h", "8000")
    table_lines.add_row("Database", "Running", "14d 3h", "5432")
    table_lines.add_row("Cache", "Running", "14d 3h", "6379")
    console.print(table_lines)


def demo_styling():
    """Styling and theming options."""
    console = get_console()
    console.print("\n\n[bold cyan]═══ Styling Options ═══[/bold cyan]\n")

    # Alternate row styles
    console.print("[dim]Alternate row styles:[/dim]")
    table_alt = Table(
        title="Product Inventory",
        headers=["SKU", "Product", "Stock", "Price"],
        row_styles="alternate",
    )
    table_alt.add_row("001", "Widget A", "150", "$9.99")
    table_alt.add_row("002", "Widget B", "85", "$14.99")
    table_alt.add_row("003", "Widget C", "220", "$19.99")
    table_alt.add_row("004", "Widget D", "42", "$24.99")
    console.print(table_alt)
    console.print()

    # Severity-based row styling
    console.print("[dim]Severity-based styling:[/dim]")
    table_severity = Table(
        title="System Alerts", headers=["Time", "Component", "Message"], row_styles="severity"
    )
    table_severity.add_row("10:00", "API", "Service started", severity="success")
    table_severity.add_row("10:15", "DB", "Connection pool low", severity="warning")
    table_severity.add_row("10:30", "Cache", "Out of memory", severity="error")
    table_severity.add_row("10:45", "API", "Health check passed", severity="success")
    console.print(table_severity)
    console.print()

    # Expanded table
    console.print("[dim]Expanded table (full width):[/dim]")
    table_exp = Table(
        title="Wide Data Table",
        headers=["Column 1", "Column 2", "Column 3", "Column 4"],
        expand=True,
    )
    table_exp.add_row("Data A1", "Data A2", "Data A3", "Data A4")
    table_exp.add_row("Data B1", "Data B2", "Data B3", "Data B4")
    console.print(table_exp)
    console.print()

    # Custom border styles for color-coding
    console.print("[dim]Custom border styles for theming:[/dim]")

    # Success table with green border
    success_table = Table(
        title="✓ Successful Operations",
        headers=["Operation", "Time", "Result"],
        border_style="bright_green",
    )
    success_table.add_row("Database backup", "10:00", "Complete")
    success_table.add_row("Cache clear", "10:05", "Complete")
    console.print(success_table)
    console.print()

    # Error table with red border
    error_table = Table(
        title="✖ Failed Operations",
        headers=["Operation", "Time", "Error"],
        border_style="bright_red",
    )
    error_table.add_row("API deployment", "10:15", "Connection timeout")
    error_table.add_row("Email send", "10:20", "Authentication failed")
    console.print(error_table)
    console.print()

    # Info table with cyan border
    info_table = Table(
        title="Configuration Details", headers=["Setting", "Value"], border_style="bright_cyan"
    )
    info_table.add_row("Environment", "production")
    info_table.add_row("Version", "2.0.1")
    info_table.add_row("Debug Mode", "false")
    console.print(info_table)
    console.print()

    # Subtle table with dim border
    subtle_table = Table(
        title="Additional Information", headers=["Key", "Value"], border_style="dim white"
    )
    subtle_table.add_row("Build Date", "2025-01-15")
    subtle_table.add_row("Commit Hash", "abc1234")
    console.print(subtle_table)


def demo_use_cases():
    """Common use cases for tables."""
    console = get_console()
    console.print("\n\n[bold cyan]═══ Use Cases ═══[/bold cyan]\n")

    # Server monitoring
    console.print("[dim]Server monitoring:[/dim]")
    servers = Table(
        title="Server Status",
        headers=["Server", "CPU", "Memory", "Disk", "Status"],
        row_styles="severity",
    )
    servers.add_row("web-01", "45%", "2.1GB", "156GB", "OK", severity="success")
    servers.add_row("web-02", "78%", "5.8GB", "89GB", "High Load", severity="warning")
    servers.add_row("db-01", "92%", "14.2GB", "12GB", "Critical", severity="error")
    servers.add_row("cache-01", "35%", "1.2GB", "445GB", "OK", severity="success")
    console.print(servers)
    console.print()

    # Test results
    console.print("[dim]Test results:[/dim]")
    tests = Table(
        title="Test Suite Results",
        headers=["Test File", "Tests", "Passed", "Failed", "Duration"],
        row_styles="alternate",
    )
    tests.add_row("test_auth.py", "15", "15", "0", "1.2s")
    tests.add_row("test_api.py", "32", "30", "2", "3.4s")
    tests.add_row("test_database.py", "28", "28", "0", "2.1s")
    tests.add_row("test_utils.py", "45", "45", "0", "0.8s")
    console.print(tests)
    console.print()

    # Sales report
    console.print("[dim]Sales report:[/dim]")
    sales = Table(
        title="Q1 2024 Sales",
        headers=["Region", "Revenue", "Growth", "Customers"],
        row_styles="alternate",
    )
    sales.add_row("North", "$1.2M", "+15%", "1,234")
    sales.add_row("South", "$890K", "+8%", "892")
    sales.add_row("East", "$1.5M", "+22%", "1,567")
    sales.add_row("West", "$2.1M", "+18%", "2,045")
    console.print(sales)
    console.print()

    # Package versions
    console.print("[dim]Package inventory:[/dim]")
    packages = [
        {"package": "requests", "version": "2.31.0", "status": "current"},
        {"package": "click", "version": "8.1.7", "status": "current"},
        {"package": "rich", "version": "13.7.0", "status": "current"},
        {"package": "pydantic", "version": "2.5.0", "status": "outdated"},
    ]
    pkg_table = Table.from_list_of_dicts(packages, title="Python Packages")
    console.print(pkg_table)


def main():
    """Run all Table demos."""
    console = get_console()

    console.print(
        "\n[bold magenta]╔════════════════════════════════════════════════╗[/bold magenta]"
    )
    console.print("[bold magenta]║   ChalkBox - Table Component Demo             ║[/bold magenta]")
    console.print("[bold magenta]╚════════════════════════════════════════════════╝[/bold magenta]")

    demo_basic_usage()
    demo_advanced_features()
    demo_styling()
    demo_use_cases()

    console.print("\n[bold green]✓  Table demo completed![/bold green]")
    console.print(
        "\n[dim]Table is perfect for: data display, reports, status dashboards, and structured information[/dim]"
    )
    console.print(
        "[dim]Customizable border styles for color-coded tables and visual theming[/dim]\n"
    )


if __name__ == "__main__":
    main()
