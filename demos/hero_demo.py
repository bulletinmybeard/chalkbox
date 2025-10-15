import time

from rich.text import Text

from chalkbox import (
    Alert,
    CodeBlock,
    Divider,
    JsonView,
    KeyValue,
    Progress,
    Section,
    Spinner,
    Stepper,
    Table,
    get_console,
)

console = get_console()


def main() -> None:
    """Run the hero demo with timing for GIF recording."""

    console.clear()
    console.print("\n[bold cyan]ChalkBox - CLI UI Kit[/bold cyan]\n")
    time.sleep(2.0)

    # 1. Console logs with styling
    console.print("[bold]1. Styled Console Output:[/bold]")
    console.print("  [cyan]→[/cyan] Initializing application...")
    time.sleep(0.7)
    console.print("  [cyan]→[/cyan] Loading configuration...")
    time.sleep(0.7)
    console.print("  [green]✓[/green] Ready!\n")
    time.sleep(1.3)

    # 2. Multiple Alert levels
    console.print("[bold]2. Alert Levels (info, success, warning, error):[/bold]\n")
    console.print(Alert.info("Processing 1,234 records"))
    time.sleep(1.0)
    console.print(Alert.success("Database connection established"))
    time.sleep(1.0)
    console.print(Alert.warning("API rate limit: 85% used"))
    time.sleep(1.0)
    console.print(Alert.error("Failed to send notification", details="Retry scheduled"))
    time.sleep(1.5)

    # 3. Divider
    console.print(Divider(title="Data Processing"))
    time.sleep(1.2)

    # 4. Spinner with loading operation
    console.print("\n[bold]3. Spinner (loading states):[/bold]\n")
    with Spinner("Fetching remote data") as spinner:
        time.sleep(2.0)
        spinner.success("Data fetched successfully!")

    console.print("  [green]✓[/green] Data fetched successfully!\n")
    time.sleep(1.2)

    # 5. Progress bar showing multiple tasks
    console.print("[bold]4. Progress Bar (multi-task tracking):[/bold]\n")
    with Progress() as progress:
        # Task 1
        task1 = progress.add_task("Building...", total=100)
        for _ in range(100):
            progress.update(task1, advance=1)
            time.sleep(0.012)

        time.sleep(0.3)

        # Task 2
        task2 = progress.add_task("Testing...", total=100)
        for _ in range(100):
            progress.update(task2, advance=1)
            time.sleep(0.010)

        time.sleep(0.3)

        # Task 3
        task3 = progress.add_task("Deploying...", total=100)
        for _ in range(100):
            progress.update(task3, advance=1)
            time.sleep(0.008)

    time.sleep(1.3)

    # 6. Table with severity styling
    console.print("\n[bold]5. Table (data with severity styling):[/bold]\n")
    table = Table(headers=["Service", "Status", "Response Time"])
    table.add_row("API Gateway", "✓ Running", "45ms", severity="success")
    table.add_row("Database", "✓ Running", "12ms", severity="success")
    table.add_row("Cache", "⚠ Degraded", "230ms", severity="warning")
    table.add_row("Message Queue", "✖ Down", "timeout", severity="error")
    console.print(table)
    time.sleep(1.5)

    # 7. KeyValue for config/stats
    console.print("\n[bold]6. KeyValue (config & stats with masking):[/bold]\n")
    kv = KeyValue(title="System Info")
    kv.add("Hostname", "prod-server-01")
    kv.add("Region", "us-east-1")
    kv.add("Uptime", "42 days, 8 hours")
    kv.add("Load Average", "0.45, 0.52, 0.48")
    kv.add("API Key", "sk-1234567890abcdef")  # Auto-masked
    console.print(kv)
    time.sleep(1.5)

    # 8. Stepper for workflow tracking with mixed states
    console.print("\n[bold]7. Stepper (workflow tracking):[/bold]\n")
    stepper = Stepper()
    stepper.add_step("Initialize")
    stepper.add_step("Configure")
    stepper.add_step("Deploy")
    stepper.add_step("Verify")
    # Set different states to show variety
    stepper.complete(0)  # Initialize ✓
    stepper.complete(1)  # Configure ✓
    stepper.fail(2)  # Deploy ✖
    stepper.skip(3)  # Verify ⊘ (skipped due to deploy failure)
    console.print(stepper)
    time.sleep(1.5)

    # 9. Section for content organization
    console.print("\n[bold]8. Section (content organization):[/bold]\n")
    section = Section(title="API Response", subtitle="GET /api/v1/users")
    status_text = Text()
    status_text.append("Status: ", style="cyan")
    status_text.append("200 OK")
    section.add(status_text)
    time_text = Text()
    time_text.append("Response Time: ", style="cyan")
    time_text.append("142ms")
    section.add(time_text)
    console.print(section)
    time.sleep(1.5)

    # 10. CodeBlock for syntax-highlighted code
    console.print("\n[bold]9. CodeBlock (syntax highlighting):[/bold]\n")
    code = '''def hello_world():
    """Simple greeting function."""
    return "Hello, World!"'''
    code_section = Section(title="example.py")
    code_section.add(CodeBlock(code, language="python"))
    console.print(code_section)
    time.sleep(1.5)

    # 11. JsonView for formatted JSON
    console.print("\n[bold]10. JsonView (formatted JSON):[/bold]\n")
    data = {
        "user": "johndoe",
        "status": "active",
        "permissions": ["read", "write"],
        "last_login": "2025-10-09T10:30:00Z",
    }
    json_section = Section(title="User Profile")
    json_section.add(JsonView(data))
    console.print(json_section)


if __name__ == "__main__":
    main()
