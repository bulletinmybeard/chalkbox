from rich.panel import Panel
from rich.text import Text

from chalkbox import Alert, ColumnLayout, get_console


def demo_basic_usage():
    """Basic usage examples."""
    console = get_console()
    console.print("\n[bold cyan]═══ Basic ColumnLayout Usage ═══[/bold cyan]\n")

    # Simple string columns
    items = ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig"]
    columns = ColumnLayout.from_strings(items)
    console.print(columns)
    console.print()

    # Equal width columns
    console.print("[dim]Equal width columns:[/dim]")
    columns_equal = ColumnLayout.from_strings(["Short", "Much Longer Text", "Med", "X"], equal=True)
    console.print(columns_equal)
    console.print()

    # Different alignments
    console.print("[dim]Center aligned:[/dim]")
    columns_center = ColumnLayout.from_strings(
        ["Left", "Center", "Right", "Default"], align="center"
    )
    console.print(columns_center)


def demo_advanced_features():
    """Advanced features and options."""
    console = get_console()
    console.print("\n[bold cyan]═══ Advanced Features ═══[/bold cyan]\n")

    # Styled text columns
    console.print("[dim]Styled columns:[/dim]")
    styled_items = [
        Text("Success", style="bold green"),
        Text("Warning", style="bold yellow"),
        Text("Error", style="bold red"),
        Text("Info", style="bold blue"),
    ]
    columns = ColumnLayout(styled_items, equal=True)
    console.print(columns)
    console.print()

    # Panels in columns
    console.print("[dim]Panels in columns:[/dim]")
    panels = [
        Panel("Database\nConnected", title="Service 1", border_style="green"),
        Panel("Cache\nRunning", title="Service 2", border_style="green"),
        Panel("Queue\nError", title="Service 3", border_style="red"),
    ]
    columns = ColumnLayout(panels, equal=True, expand=True)
    console.print(columns)
    console.print()

    # Mixed content
    console.print("[dim]Mixed content types:[/dim]")
    mixed = ColumnLayout()
    mixed.add(Alert.success("Pass"))
    mixed.add(Alert.warning("Warn"))
    mixed.add(Alert.error("Fail"))
    console.print(mixed)


def demo_styling():
    """Styling and theming options."""
    console = get_console()
    console.print("\n[bold cyan]═══ Styling Options ═══[/bold cyan]\n")

    # From dictionary
    console.print("[dim]Key-value columns from dict:[/dim]")
    config = {
        "Host": "localhost",
        "Port": "5432",
        "Database": "myapp",
        "SSL": "enabled",
    }
    columns = ColumnLayout.from_dict(config, equal=True)
    console.print(columns)
    console.print()

    # Grid layout simulation
    console.print("[dim]Grid of status items:[/dim]")
    status_items = [
        Text("✓ CPU: 45%", style="green"),
        Text("✓ Memory: 2.1GB", style="green"),
        Text("✓ Disk: 156GB", style="green"),
        Text("⚠ Network: High", style="yellow"),
        Text("✓ Uptime: 14d", style="green"),
        Text("✓ Load: 0.8", style="green"),
    ]
    grid = ColumnLayout.grid(status_items, columns=3)
    console.print(grid)
    console.print()

    # Tag cloud
    console.print("[dim]Tag cloud:[/dim]")
    tags = ["python", "cli", "terminal", "ui", "rich", "console", "colors", "themes"]
    tag_items = [Text(f"#{tag}", style="dim cyan") for tag in tags]
    tag_cloud = ColumnLayout(tag_items)
    console.print(tag_cloud)


def main():
    """Run all ColumnLayout demos."""
    console = get_console()

    console.print(
        "\n[bold magenta]╔════════════════════════════════════════════════╗[/bold magenta]"
    )
    console.print("[bold magenta]║   ChalkBox - ColumnLayout Component Demo      ║[/bold magenta]")
    console.print("[bold magenta]╚════════════════════════════════════════════════╝[/bold magenta]")

    demo_basic_usage()
    demo_advanced_features()
    demo_styling()

    console.print("\n[bold green]✓  ColumnLayout demo completed![/bold green]")
    console.print(
        "\n[dim]ColumnLayout is perfect for: multi-column displays, grids, menus, and organized content[/dim]\n"
    )


if __name__ == "__main__":
    main()
