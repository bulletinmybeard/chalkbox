import time

from rich.panel import Panel
from rich.text import Text

from chalkbox import (
    ColumnLayout,
    Divider,
    MultiPanel,
    Status,
    Table,
    get_console,
    status,
)


def demo_status():
    """Demonstrate Status component."""
    console = get_console()

    console.print("\n[bold cyan]═══ Status Component Demo ═══[/bold cyan]\n")

    Divider.section("Basic Status Display").print()

    # Basic status
    with status("Processing items..."):
        time.sleep(5)

    console.print("[green]✓[/green] Processing complete!\n")

    # Status with custom spinner
    Divider.section("Custom Spinner Styles").print()

    spinners = ["dots", "line", "arc", "arrow", "bounce"]

    for spinner_style in spinners:
        with Status(f"Using '{spinner_style}' spinner...", spinner=spinner_style):
            time.sleep(5)

    console.print("[green]✓[/green] All spinners demonstrated!\n")

    # Status allows console output
    Divider.section("Status with Console Output").print()

    with Status("Background task running...") as s:
        for i in range(5):
            console.print(f"  [dim]Processing item {i + 1}/5[/dim]")
            time.sleep(0.5)
        s.update("Finalizing...")
        time.sleep(0.5)

    console.print("[green]✓[/green] Background task complete!\n")


def demo_columns():
    """Demonstrate ColumnLayout component."""
    console = get_console()

    console.print("\n[bold cyan]═══ ColumnLayout Component Demo ═══[/bold cyan]\n")

    # Simple string columns
    Divider.section("File Listing in Columns").print()

    files = [
        "config.yaml",
        "main.py",
        "utils.py",
        "tests.py",
        "README.md",
        "requirements.txt",
        "setup.py",
        "LICENSE",
        ".gitignore",
        "Dockerfile",
        "docker-compose.yml",
        "Makefile",
    ]

    columns = ColumnLayout.from_strings(files, equal=True)
    columns.print()
    console.print()

    # Styled columns
    Divider.section("Styled Items").print()

    tags = ["python", "cli", "terminal", "ui", "rich", "themes", "components"]
    styled_cols = ColumnLayout.from_strings(tags, style="bold cyan", equal=False)
    styled_cols.print()
    console.print()

    # Dictionary as columns
    Divider.section("Configuration Items").print()

    config = {
        "host": "localhost",
        "port": 8080,
        "debug": True,
        "workers": 4,
        "timeout": 30,
        "ssl": False,
    }

    config_cols = ColumnLayout.from_dict(config, equal=True)
    config_cols.print()
    console.print()

    # Grid layout
    Divider.section("Grid Layout").print()

    colors = [
        Text("Red", style="bold red"),
        Text("Green", style="bold green"),
        Text("Blue", style="bold blue"),
        Text("Yellow", style="bold yellow"),
        Text("Magenta", style="bold magenta"),
        Text("Cyan", style="bold cyan"),
    ]

    grid = ColumnLayout.grid(colors, columns=3)
    grid.print()
    console.print()


def demo_layout():
    """Demonstrate MultiPanel component."""
    console = get_console()

    console.print("\n[bold cyan]═══ MultiPanel Component Demo ═══[/bold cyan]\n")

    # Simple sidebar layout
    Divider.section("Sidebar Layout").print()

    sidebar_content = Panel(
        "[bold]Navigation[/bold]\n\n" "• Home\n" "• Projects\n" "• Settings\n" "• Help",
        title="Menu",
        border_style="cyan",
    )

    main_content = Panel(
        "[bold]Main Content Area[/bold]\n\n"
        "This is where your main content goes.\n"
        "The sidebar is on the left with navigation items.",
        title="Content",
        border_style="green",
    )

    sidebar_layout = MultiPanel.create_sidebar(
        sidebar_content, main_content, sidebar_width=25, sidebar_position="left"
    )
    sidebar_layout.print()
    console.print()

    # Header/Footer layout
    Divider.section("Header and Footer Layout").print()

    header = Panel("[bold cyan]Application Header[/bold cyan]", border_style="cyan", padding=(0, 1))

    content = Panel(
        "Main application content area.\n"
        "This is the scrollable content section between header and footer.",
        border_style="green",
        padding=(1, 2),
    )

    footer = Panel(
        "[dim]Status: Ready | User: Admin | Time: 12:34[/dim]",
        border_style="blue",
        padding=(0, 1),
    )

    hf_layout = MultiPanel.create_header_footer(
        header, content, footer, header_size=3, footer_size=3
    )
    hf_layout.print()
    console.print()

    # Grid layout
    Divider.section("2x2 Grid Layout").print()

    panels = {
        "CPU": Panel("CPU: 45%\n[green]████████░░[/green]", border_style="yellow"),
        "Memory": Panel("RAM: 67%\n[yellow]██████████[/yellow]", border_style="yellow"),
        "Disk": Panel("Disk: 82%\n[red]████████████[/red]", border_style="yellow"),
        "Network": Panel("Net: 23 MB/s\n[green]████░░░░░░[/green]", border_style="yellow"),
    }

    grid_layout = MultiPanel.create_grid(panels, rows=2, cols=2)
    grid_layout.print()
    console.print()

    # Dashboard layout
    Divider.section("Full Dashboard Layout").print()

    dashboard_header = Panel(
        "[bold magenta]System Dashboard[/bold magenta]",
        border_style="magenta",
        padding=(0, 2),
    )

    dashboard_sidebar = Panel(
        "[bold]Quick Stats[/bold]\n\n" "Uptime: 3d 4h\n" "Tasks: 42\n" "Users: 127\n" "Alerts: 3",
        title="Info",
        border_style="cyan",
    )

    # Create a metrics table for main content
    metrics_table = Table(headers=["Metric", "Value", "Status"])
    metrics_table.add_row("CPU Usage", "45%", "✓ Normal", severity="success")
    metrics_table.add_row("Memory", "67%", "⚠ High", severity="warning")
    metrics_table.add_row("Disk Space", "82%", "⚠ High", severity="warning")
    metrics_table.add_row("Network", "23 MB/s", "✓ Normal", severity="success")

    dashboard_main = Panel(metrics_table, title="System Metrics", border_style="green")

    dashboard_footer = Panel(
        "[dim]Last updated: Just now | Refresh: 5s[/dim]",
        border_style="blue",
        padding=(0, 2),
    )

    dashboard = MultiPanel.create_dashboard(
        dashboard_header,
        dashboard_sidebar,
        dashboard_main,
        dashboard_footer,
        header_size=3,
        sidebar_width=20,
        footer_size=3,
    )
    dashboard.print()
    console.print()


def demo_combined():
    """Demonstrate combining Phase 2 components."""
    console = get_console()

    console.print("\n[bold cyan]═══ Combined Components Demo ═══[/bold cyan]\n")

    Divider.section("Building a CLI Tool").print()

    # Show status while "loading"
    with status("Initializing application..."):
        time.sleep(1)

    # Show available commands in columns
    console.print("\n[bold]Available Commands:[/bold]")
    commands = ["init", "build", "test", "deploy", "status", "logs", "config", "help"]
    cmd_cols = ColumnLayout.from_strings(commands, style="cyan", equal=True)
    cmd_cols.print()

    console.print()
    Divider.separator().print()
    console.print()

    # Show a dashboard with project info
    project_info = Panel(
        "[bold]Project: my-app[/bold]\n" "Version: 1.0.0\n" "Status: Running",
        title="Info",
        border_style="cyan",
    )

    recent_logs = Panel(
        "[dim]2025-01-15 12:34:56[/dim] Server started\n"
        "[dim]2025-01-15 12:35:01[/dim] Connected to database\n"
        "[dim]2025-01-15 12:35:02[/dim] [green]Ready to accept requests[/green]",
        title="Recent Logs",
        border_style="green",
    )

    app_layout = MultiPanel.create_sidebar(
        project_info, recent_logs, sidebar_width=25, sidebar_position="left"
    )
    app_layout.print()

    console.print("\n[green]✓[/green] Application initialized!\n")


def main():
    """Run all Phase 2 demos."""
    console = get_console()

    console.print(
        "\n[bold magenta]╔════════════════════════════════════════════════╗[/bold magenta]"
    )
    console.print("[bold magenta]║   ChalkBox - Phase 2 Components Demo          ║[/bold magenta]")
    console.print(
        "[bold magenta]╚════════════════════════════════════════════════╝[/bold magenta]\n"
    )

    demo_status()
    demo_columns()
    demo_layout()
    demo_combined()

    console.print("\n[bold green]✓  Phase 2 demo completed![/bold green]")
    console.print(
        "\nNew components: [cyan]Status[/cyan], [cyan]ColumnLayout[/cyan], [cyan]MultiPanel[/cyan]\n"
    )


if __name__ == "__main__":
    main()
