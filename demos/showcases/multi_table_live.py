from contextlib import suppress
from datetime import datetime
import random
import sys
import time

from rich.console import Group
from rich.layout import Layout
from rich.panel import Panel

from chalkbox import Table, get_console
from chalkbox.live import Dashboard, LiveComponent


def get_system_metrics():
    """Generate system metrics dictionary."""
    return {
        "CPU": f"{random.randint(20, 80)}%",
        "Memory": f"{random.randint(2, 8)}GB",
        "Disk": f"{random.randint(100, 500)}GB",
        "Network": f"{random.randint(1, 50)}MB/s",
    }


def get_services_list():
    """Generate services list of dictionaries."""
    return [
        {
            "name": "nginx",
            "status": "✓ Running" if random.random() > 0.1 else "✖ Stopped",
            "port": "80",
            "cpu": f"{random.randint(1, 20)}%",
        },
        {
            "name": "postgres",
            "status": "✓ Running" if random.random() > 0.1 else "✖ Stopped",
            "port": "5432",
            "cpu": f"{random.randint(5, 30)}%",
        },
        {
            "name": "redis",
            "status": "✓ Running" if random.random() > 0.1 else "✖ Stopped",
            "port": "6379",
            "cpu": f"{random.randint(1, 10)}%",
        },
        {
            "name": "mongodb",
            "status": "✓ Running" if random.random() > 0.1 else "✖ Stopped",
            "port": "27017",
            "cpu": f"{random.randint(3, 15)}%",
        },
    ]


def get_process_data():
    """Generate detailed process data with many columns."""
    return [
        {
            "PID": str(random.randint(1000, 9999)),
            "Name": "python",
            "CPU": f"{random.randint(10, 60)}%",
            "Memory": f"{random.randint(100, 400)}MB",
            "Disk": f"{random.randint(0, 100)}MB/s",
            "Network": f"{random.randint(0, 50)}MB/s",
            "Status": "Running",
        },
        {
            "PID": str(random.randint(1000, 9999)),
            "Name": "node",
            "CPU": f"{random.randint(5, 40)}%",
            "Memory": f"{random.randint(150, 350)}MB",
            "Disk": f"{random.randint(0, 50)}MB/s",
            "Network": f"{random.randint(0, 30)}MB/s",
            "Status": "Running",
        },
    ]


def get_alerts():
    """Generate alerts list."""
    alerts = []
    if random.random() > 0.7:
        alerts.append(
            {
                "level": "⚠ Warning",
                "message": "High CPU usage",
                "time": datetime.now().strftime("%H:%M:%S"),
            }
        )
    if random.random() > 0.9:
        alerts.append({"level": "✖ Error", "message": "Disk space low", "time": "10:35"})
    if not alerts:
        alerts.append(
            {
                "level": "✓ OK",
                "message": "All systems normal",
                "time": datetime.now().strftime("%H:%M:%S"),
            }
        )
    return alerts


def get_config():
    """Generate configuration dictionary."""
    return {
        "Environment": "Production",
        "Version": "1.2.3",
        "Uptime": "14 days",
        "Region": "us-east-1",
    }


# Demo 1: Dashboard pattern with 4 tables of different sizes
def demo_dashboard_pattern():
    """Dashboard with 4 tables - narrow, medium, and wide tables."""
    console = get_console()

    console.print("\n[bold cyan]═══ Dashboard Pattern Demo ═══[/bold cyan]")
    console.print("[dim]4 tables with different sizes, all responsive to resize[/dim]")
    console.print("[dim]- Header: Wide table (7 columns) with expand='auto'[/dim]")
    console.print("[dim]- Sidebar: Narrow table (2 columns) from dict[/dim]")
    console.print("[dim]- Main: Medium table (4 columns) from list of dicts[/dim]")
    console.print("[dim]- Footer: Small table (3 columns) for alerts[/dim]")
    console.print("[yellow]Resize your terminal to see responsive behavior![/yellow]")
    console.print("[yellow]Press Ctrl+C to exit[/yellow]\n")

    time.sleep(3)

    def update_header():
        """Wide table with many columns - will expand on wide terminals."""
        data = get_process_data()
        table = Table.from_list_of_dicts(
            data,
            title=f"Processes - {datetime.now().strftime('%H:%M:%S')}",
            expand="auto",  # Responsive: 7 cols >= 5 threshold
        )
        return Panel(table, border_style="green")

    def update_sidebar():
        """Narrow table from dictionary - stays compact."""
        table = Table.from_dict(
            get_system_metrics(),
            title="System Metrics",
            expand="auto",  # Responsive: 2 cols < 5, stays compact
        )
        return Panel(table, border_style="cyan")

    def update_main():
        """Medium table from list of dicts."""
        table = Table.from_list_of_dicts(
            get_services_list(),
            title="Services",
            expand="auto",  # Responsive: 4 cols < 5, stays compact
        )
        return Panel(table, border_style="blue")

    def update_footer():
        """Small alerts table."""
        table = Table.from_list_of_dicts(
            get_alerts(),
            title="Alerts",
            expand="auto",  # 3 cols, stays compact
        )
        return Panel(table, border_style="yellow")

    # Create dashboard - single .live() manages all 4 tables
    dashboard = Dashboard.create("full")

    # Provide initial content + update functions
    dashboard.set_header(update_header(), update_fn=update_header)
    dashboard.set_sidebar(update_sidebar(), update_fn=update_sidebar)
    dashboard.set_main(update_fn=update_main)  # main allows content=None
    dashboard.set_footer(update_footer(), update_fn=update_footer)

    with suppress(KeyboardInterrupt):
        dashboard.run(refresh_per_second=2)

    console.print("\n[green]✓[/green] Demo completed\n")


# Demo 2: Group pattern with 5+ tables stacked vertically
def demo_group_pattern():
    """Group pattern for vertical stack of many tables."""
    console = get_console()

    console.print("\n[bold cyan]═══ Group Pattern Demo ═══[/bold cyan]")
    console.print("[dim]5 tables stacked vertically, each with different sizes[/dim]")
    console.print("[dim]All tables use expand='auto' for responsive sizing[/dim]")
    console.print("[yellow]Resize terminal to see all tables adapt![/yellow]")
    console.print("[yellow]Press Ctrl+C to exit[/yellow]\n")

    time.sleep(3)

    def create_multi_table_stack():
        """Create vertical stack of 5 different tables."""
        tables = []

        # Table 1: Narrow (2 cols) - from dict
        table1 = Table.from_dict(
            get_system_metrics(),
            title=f"Metrics - {datetime.now().strftime('%H:%M:%S')}",
            expand="auto",
        )
        tables.append(Panel(table1, border_style="green"))

        # Table 2: Medium (4 cols) - from list of dicts
        table2 = Table.from_list_of_dicts(get_services_list(), title="Services", expand="auto")
        tables.append(Panel(table2, border_style="blue"))

        # Table 3: Wide (7 cols) - from list of dicts
        table3 = Table.from_list_of_dicts(get_process_data(), title="Processes", expand="auto")
        tables.append(Panel(table3, border_style="cyan"))

        # Table 4: Small (3 cols) - alerts
        table4 = Table.from_list_of_dicts(get_alerts(), title="Alerts", expand="auto")
        tables.append(Panel(table4, border_style="yellow"))

        # Table 5: Narrow (2 cols) - config
        table5 = Table.from_dict(get_config(), title="Configuration", expand="auto")
        tables.append(Panel(table5, border_style="magenta"))

        return Group(*tables)

    # Single .live() manages all 5 tables
    initial_stack = create_multi_table_stack()

    try:
        with LiveComponent(
            initial_stack,
            update_fn=create_multi_table_stack,
            refresh_per_second=2,
            screen=True,
        ):
            while True:
                time.sleep(0.1)
    except KeyboardInterrupt:
        pass

    console.print("\n[green]✓[/green] Demo completed\n")


# Demo 3: Grid layout with tables of different sizes
def demo_grid_pattern():
    """Grid layout (2x2) with tables of varying sizes."""
    console = get_console()

    console.print("\n[bold cyan]═══ Grid Layout Demo ═══[/bold cyan]")
    console.print("[dim]2x2 grid with 4 tables of different sizes[/dim]")
    console.print("[dim]Top-left: Wide table (7 cols)[/dim]")
    console.print("[dim]Top-right: Medium table (4 cols)[/dim]")
    console.print("[dim]Bottom-left: Narrow table (2 cols)[/dim]")
    console.print("[dim]Bottom-right: Small table (3 cols)[/dim]")
    console.print("[yellow]All tables responsive with expand='auto'![/yellow]")
    console.print("[yellow]Press Ctrl+C to exit[/yellow]\n")

    time.sleep(3)

    def create_grid_dashboard():
        """Create 2x2 grid layout with tables."""
        layout = Layout()

        # Split into 2 rows
        layout.split_column(Layout(name="top"), Layout(name="bottom"))

        # Split each row into 2 columns
        layout["top"].split_row(Layout(name="top_left"), Layout(name="top_right"))
        layout["bottom"].split_row(Layout(name="bottom_left"), Layout(name="bottom_right"))

        # Top-left: Wide table (7 columns)
        table_tl = Table.from_list_of_dicts(
            get_process_data(),
            title=f"Processes - {datetime.now().strftime('%H:%M:%S')}",
            expand="auto",
        )
        layout["top_left"].update(Panel(table_tl, border_style="green"))

        # Top-right: Medium table (4 columns)
        table_tr = Table.from_list_of_dicts(get_services_list(), title="Services", expand="auto")
        layout["top_right"].update(Panel(table_tr, border_style="blue"))

        # Bottom-left: Narrow table (2 columns)
        table_bl = Table.from_dict(get_system_metrics(), title="System Metrics", expand="auto")
        layout["bottom_left"].update(Panel(table_bl, border_style="cyan"))

        # Bottom-right: Small table (3 columns)
        table_br = Table.from_list_of_dicts(get_alerts(), title="Alerts", expand="auto")
        layout["bottom_right"].update(Panel(table_br, border_style="yellow"))

        return layout

    # Single .live() manages entire grid
    initial_grid = create_grid_dashboard()

    try:
        with LiveComponent(
            initial_grid,
            update_fn=create_grid_dashboard,
            refresh_per_second=2,
            screen=True,
        ):
            while True:
                time.sleep(0.1)
    except KeyboardInterrupt:
        pass

    console.print("\n[green]✓[/green] Demo completed\n")


# Demo 4: Size comparison - show responsive breakpoints
def demo_size_comparison():
    """Show how different table sizes respond to terminal width."""
    console = get_console()

    console.print("\n[bold cyan]═══ Table Size Comparison Demo ═══[/bold cyan]")
    console.print("[dim]3 tables with different column counts[/dim]")
    console.print("[dim]Watch how they respond differently to terminal width:[/dim]")
    console.print("[dim]  • Narrow (2 cols): Always compact[/dim]")
    console.print("[dim]  • Medium (4 cols): Stays compact (< 5 threshold)[/dim]")
    console.print("[dim]  • Wide (7 cols): Expands when terminal is wide enough[/dim]")
    console.print("[yellow]Try resizing: < 60 cols, 60-80 cols, > 80 cols[/yellow]")
    console.print("[yellow]Press Ctrl+C to exit[/yellow]\n")

    time.sleep(3)

    def create_size_comparison():
        """Create tables of different sizes for comparison."""
        tables = []

        # Show current terminal width
        term_width = get_console().width
        if term_width < 60:
            breakpoint = "[red]Compact[/red] (< 60 cols) - All tables stay narrow"
        elif term_width < 80:
            breakpoint = "[yellow]Medium[/yellow] (60-80 cols) - Wide table gets calculated width"
        else:
            breakpoint = "[green]Wide[/green] (> 80 cols) - Wide table expands (7 cols >= 5)"

        header = Panel(
            f"[bold]Terminal Width: {term_width} cols[/bold]\n{breakpoint}",
            border_style="cyan",
        )
        tables.append(header)

        # Narrow table (2 columns) - always compact
        table1 = Table.from_dict(
            {"CPU": f"{random.randint(20, 80)}%", "Memory": f"{random.randint(2, 8)}GB"},
            title="Narrow Table (2 cols) - Always Compact",
            expand="auto",
        )
        tables.append(Panel(table1, border_style="green", title="2 cols < 5 threshold"))

        # Medium table (4 columns) - stays compact
        services = get_services_list()[:2]  # Only 2 services for cleaner display
        table2 = Table.from_list_of_dicts(
            services, title="Medium Table (4 cols) - Stays Compact", expand="auto"
        )
        tables.append(Panel(table2, border_style="blue", title="4 cols < 5 threshold"))

        # Wide table (7 columns) - responsive expand
        table3 = Table.from_list_of_dicts(
            get_process_data(),
            title="Wide Table (7 cols) - Responsive Expand",
            expand="auto",
        )
        tables.append(Panel(table3, border_style="magenta", title="7 cols >= 5 threshold"))

        return Group(*tables)

    initial_comparison = create_size_comparison()

    try:
        with LiveComponent(
            initial_comparison,
            update_fn=create_size_comparison,
            refresh_per_second=4,
            screen=True,
        ):
            while True:
                time.sleep(0.1)
    except KeyboardInterrupt:
        pass

    console.print("\n[green]✓[/green] Demo completed\n")


def main():
    """Run multi-table live demos."""
    console = get_console()

    console.print(
        "\n[bold magenta]╔════════════════════════════════════════════════╗[/bold magenta]"
    )
    console.print("[bold magenta]║   ChalkBox - Multi-Table Live Demo            ║[/bold magenta]")
    console.print(
        "[bold magenta]╚════════════════════════════════════════════════╝[/bold magenta]\n"
    )

    demos = {
        "1": demo_dashboard_pattern,
        "2": demo_group_pattern,
        "3": demo_grid_pattern,
        "4": demo_size_comparison,
    }

    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        # Show menu
        console.print("[bold]Select a demo:[/bold]\n")
        console.print("  [cyan]1[/cyan] - Dashboard Pattern (4 tables in structured layout)")
        console.print("  [cyan]2[/cyan] - Group Pattern (5 tables stacked vertically)")
        console.print("  [cyan]3[/cyan] - Grid Pattern (2x2 grid layout)")
        console.print("  [cyan]4[/cyan] - Size Comparison (responsive behavior demo)")
        console.print("  [cyan]5[/cyan] - Run All Demos")
        console.print("  [cyan]q[/cyan] - Quit\n")

        try:
            choice = input("[bold yellow]Enter choice (1-5 or q):[/bold yellow] ").strip()
        except EOFError:
            # Non-interactive mode (e.g., piped input) - run all demos
            choice = "5"

    if choice == "5":
        for demo_func in demos.values():
            try:
                demo_func()
            except KeyboardInterrupt:
                console.print("\n[yellow]⚠[/yellow] Demo skipped\n")
        console.print("[bold green]✓  All demos completed![/bold green]\n")
    elif choice in demos:
        demos[choice]()
    elif choice.lower() == "q":
        console.print("[dim]Goodbye![/dim]\n")
    else:
        console.print("[red]Invalid choice![/red]\n")


if __name__ == "__main__":
    main()
