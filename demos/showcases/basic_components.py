import time

from chalkbox import (
    Alert,
    Divider,
    KeyValue,
    Progress,
    Section,
    Spinner,
    Stepper,
    Table,
    get_console,
    setup_logging,
)


def demo_spinner():
    """Demonstrate spinner usage."""
    console = get_console()
    console.print("\n[bold cyan]Spinner Demo[/bold cyan]")

    # Basic spinner
    with Spinner("Loading configuration...") as spinner:
        time.sleep(2)
        spinner.success("Configuration loaded!")

    # Spinner with error
    with Spinner("Connecting to database...") as spinner:
        time.sleep(1)
        spinner.error("Connection failed!")

    # Spinner with warning
    with Spinner("Checking dependencies...") as spinner:
        time.sleep(1)
        spinner.warning("Some dependencies are outdated")


def demo_progress():
    """Demonstrate progress bar usage."""
    console = get_console()
    console.print("\n[bold cyan]Progress Bar Demo[/bold cyan]")

    with Progress() as progress:
        # Single task
        task1 = progress.add_task("Processing files", total=100)

        for _ in range(100):
            progress.update(task1, advance=1)
            time.sleep(0.01)

        # Multiple tasks
        task2 = progress.add_task("Downloading data", total=50)
        task3 = progress.add_task("Analyzing results", total=75)

        for i in range(max(50, 75)):
            if i < 50:
                progress.update(task2, advance=1)
            if i < 75:
                progress.update(task3, advance=1)
            time.sleep(0.02)


def demo_alerts():
    """Demonstrate alert components."""
    console = get_console()
    console.print("\n[bold cyan]Alert Demo[/bold cyan]")

    console.print(Alert.info("This is an informational message"))
    console.print(Alert.success("Operation completed successfully!"))
    console.print(
        Alert.warning("API rate limit approaching", details="You have 100 requests remaining")
    )
    console.print(
        Alert.error(
            "Failed to connect to server", details="Check your network connection and try again"
        )
    )


def demo_sections():
    """Demonstrate section components."""
    console = get_console()
    console.print("\n[bold cyan]Section Demo[/bold cyan]")

    # Basic section
    with Section("Configuration Settings") as section:
        section.add_text("Database: PostgreSQL")
        section.add_text("Port: 5432")
        section.add_text("SSL: Enabled")

    # Section with mixed content
    with Section("Analysis Results", subtitle="Generated at 2024-01-01") as section:
        section.add(Alert.success("All tests passed"))
        section.add_spacing()

        table = Table(headers=["Metric", "Value", "Status"])
        table.add_row("Performance", "98%", "✓ ")
        table.add_row("Memory", "512MB", "✓ ")
        table.add_row("Errors", "0", "✓ ")
        section.add(table)


def demo_tables():
    """Demonstrate table components."""
    console = get_console()
    console.print("\n[bold cyan]Table Demo[/bold cyan]")

    # Basic table
    table = Table(
        title="User Statistics",
        headers=["Name", "Role", "Status", "Last Login"],
        row_styles="alternate",
    )

    table.add_row("Alice Smith", "Admin", "Active", "2024-01-01")
    table.add_row("Bob Jones", "User", "Active", "2024-01-02")
    table.add_row("Charlie Brown", "User", "Inactive", "2023-12-15")

    console.print(table)

    # Table from list of dicts
    data = [
        {"name": "Python", "version": "3.11", "status": "installed"},
        {"name": "Node.js", "version": "20.0", "status": "installed"},
        {"name": "Rust", "version": "1.75", "status": "not installed"},
    ]

    table2 = Table.from_list_of_dicts(data, title="Development Tools")
    console.print(table2)


def demo_key_value():
    """Demonstrate key-value lists."""
    console = get_console()
    console.print("\n[bold cyan]Key-Value List Demo[/bold cyan]")

    # Configuration display
    config = {
        "host": "localhost",
        "port": 5432,
        "database": "myapp",
        "username": "admin",
        "password": "secret123",
        "api_key": "sk-1234567890abcdef",
        "debug": True,
        "features": ["auth", "logging", "caching"],
    }

    kv = KeyValue(config, title="Application Configuration")
    console.print(kv)

    # Environment variables (partial)
    import os

    env_vars = dict(list(os.environ.items())[:5])
    kv2 = KeyValue(env_vars, title="Environment Variables (sample)")
    console.print(kv2)


def demo_stepper():
    """Demonstrate stepper component."""
    console = get_console()
    console.print("\n[bold cyan]Stepper Demo[/bold cyan]")

    steps = [
        "Initialize project",
        "Install dependencies",
        "Run tests",
        "Build application",
        "Deploy to server",
    ]

    with Stepper.from_list(steps, title="Deployment Pipeline", live=True) as stepper:
        for i in range(len(steps)):
            stepper.start(i)
            time.sleep(1)

            # Simulate some failures/skips
            if i == 2:
                stepper.fail(i, "3 tests failed")
            elif i == 4:
                stepper.skip(i)
            else:
                stepper.complete(i)


def demo_logging():
    """Demonstrate logging setup."""
    console = get_console()
    console.print("\n[bold cyan]Logging Demo[/bold cyan]")

    # Setup logging
    logger = setup_logging(level="DEBUG")

    # Log at different levels
    logger.debug("Debug message with details")
    logger.info("Application started successfully")
    logger.warning("Configuration file not found, using defaults")
    logger.error("Failed to connect to database")

    try:
        _ = 1 / 0  # Intentionally trigger ZeroDivisionError for demo
    except Exception:
        logger.exception("An error occurred during calculation")


def main():
    """Run all demos."""
    console = get_console()
    console.print("[bold magenta]ChalkBox Demo Suite[/bold magenta]\n")

    demos = [
        ("Spinner", demo_spinner),
        ("Progress", demo_progress),
        ("Alerts", demo_alerts),
        ("Sections", demo_sections),
        ("Tables", demo_tables),
        ("Key-Value Lists", demo_key_value),
        ("Stepper", demo_stepper),
        ("Logging", demo_logging),
    ]

    for _name, demo_func in demos:
        console.print()
        console.print(Divider(style="dim"))
        demo_func()
        time.sleep(0.5)

    console.print()
    console.print(Divider(style="dim"))
    console.print("\n[bold green]✓  All demos completed![/bold green]")


if __name__ == "__main__":
    main()
