from rich.panel import Panel
from rich.text import Text

from chalkbox import Alert, Divider, KeyValue, MultiPanel, Table, get_console


def demo_basic_usage():
    """Basic usage examples."""
    console = get_console()
    console.print()
    console.print(Divider(title="Basic MultiPanel Usage", style="bold cyan"))
    console.print()

    # Simple header and footer layout
    header = Panel("Application Header", style="bold blue")
    main_content = Text("Main content area\nThis is where your primary content goes")
    footer = Panel("Status: Ready", style="dim")

    layout = MultiPanel.create_header_footer(
        header_content=header,
        main_content=main_content,
        footer_content=footer,
        header_size=3,
        footer_size=3,
    )
    console.print(layout)
    console.print("\n[dim]Press Ctrl+C to continue...[/dim]")

    # Sidebar layout
    console.print("\n[dim]Sidebar layout:[/dim]")
    sidebar_content = Panel("Navigation\n\n• Home\n• Settings\n• About", title="Menu")
    main = Panel("Main content with sidebar", style="green")

    layout_sidebar = MultiPanel.create_sidebar(
        sidebar_content=sidebar_content,
        main_content=main,
        sidebar_width=25,
        sidebar_position="left",
    )
    console.print(layout_sidebar)


def demo_advanced_features():
    """Advanced features and options."""
    console = get_console()
    console.print("\n\n[bold cyan]═══ Advanced Features ═══[/bold cyan]\n")

    # Dashboard layout
    header = Panel("[bold]System Dashboard[/bold]", style="blue")

    # Sidebar with stats
    stats = KeyValue(
        {"Uptime": "14 days", "CPU": "45%", "Memory": "2.1GB", "Disk": "156GB"}, title="Stats"
    )

    # Main content with table
    table = Table(headers=["Service", "Status", "Port"])
    table.add_row("API Server", "Running", "8000")
    table.add_row("Database", "Running", "5432")
    table.add_row("Cache", "Running", "6379")

    footer = Panel("Last updated: 2024-01-15 14:30:00", style="dim")

    dashboard = MultiPanel.create_dashboard(
        header=header,
        sidebar=stats,
        main=table,
        footer=footer,
        header_size=3,
        sidebar_width=25,
        footer_size=3,
    )
    console.print(dashboard)


def demo_styling():
    """Styling and theming options."""
    console = get_console()
    console.print("\n\n[bold cyan]═══ Styling Options ═══[/bold cyan]\n")

    # Grid layout
    panels_data = {
        "panel1": Panel("CPU\n45%", style="green"),
        "panel2": Panel("Memory\n2.1GB", style="yellow"),
        "panel3": Panel("Disk\n156GB", style="blue"),
        "panel4": Panel("Network\nHigh", style="red"),
    }

    grid = MultiPanel.create_grid(panels_data, rows=2, cols=2)
    console.print(grid)

    # Custom split
    console.print("\n[dim]Custom vertical split:[/dim]")
    root = MultiPanel()

    top = MultiPanel("top")
    top.update(Panel("Top Panel", style="cyan"))

    bottom = MultiPanel("bottom")
    bottom.update(Panel("Bottom Panel", style="magenta"))

    root.split_column(top, bottom)
    console.print(root)


def demo_use_cases():
    """Common use cases for multi-panel layouts."""
    console = get_console()
    console.print("\n\n[bold cyan]═══ Use Cases ═══[/bold cyan]\n")

    # Monitoring dashboard
    header = Panel("[bold]Server Monitor[/bold]", style="blue")

    sidebar_text = Text()
    sidebar_text.append("Quick Actions\n\n", style="bold")
    sidebar_text.append("• Restart\n", style="green")
    sidebar_text.append("• Stop\n", style="red")
    sidebar_text.append("• Logs\n", style="yellow")
    sidebar_panel = Panel(sidebar_text)

    main_table = Table(headers=["Metric", "Value", "Status"], row_styles="alternate")
    main_table.add_row("Response Time", "45ms", "✓")
    main_table.add_row("Error Rate", "0.01%", "✓")
    main_table.add_row("Throughput", "1.2K req/s", "✓")

    monitor = MultiPanel.create_dashboard(
        header=header, sidebar=sidebar_panel, main=main_table, header_size=3, sidebar_width=20
    )
    console.print(monitor)

    # Application layout
    console.print("\n[dim]Application layout:[/dim]")
    app_header = Panel("[bold cyan]MyApp v1.0[/bold cyan]", style="blue")
    app_content = Alert.info("Welcome to the application!")
    app_footer = Panel("Help: Press ? for commands | Quit: Ctrl+C", style="dim")

    app_layout = MultiPanel.create_header_footer(
        header_content=app_header, main_content=app_content, footer_content=app_footer
    )
    console.print(app_layout)


def main():
    """Run all MultiPanel demos."""
    console = get_console()

    console.print()
    console.print(
        Panel(
            "[bold]ChalkBox - MultiPanel Component Demo[/bold]",
            style="magenta",
            expand=False,
        )
    )

    demo_basic_usage()
    demo_advanced_features()
    demo_styling()
    demo_use_cases()

    console.print("\n[bold green]✓  MultiPanel demo completed![/bold green]")
    console.print(
        "\n[dim]MultiPanel is perfect for: dashboards, complex layouts, monitoring UIs, and app frameworks[/dim]\n"
    )


if __name__ == "__main__":
    main()
