from datetime import datetime
import random
import time

from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from chalkbox import Table, get_console
from chalkbox.live import LiveComponent

DEMO_DURATION_IN_SECONDS = 10


class CarouselState:
    """Manages carousel state with proper timing."""

    def __init__(self):
        self.current_index = 0
        self.start_time = None
        self.started = False
        self.completed = False

    def start(self):
        """Start the carousel timer."""
        self.start_time = time.time()
        self.started = True

    def get_elapsed_time(self):
        """Get elapsed time for current demo."""
        if not self.started or self.start_time is None:
            return 0.0
        return time.time() - self.start_time

    def should_advance(self):
        """Check if it's time to advance to next demo."""
        return self.get_elapsed_time() >= DEMO_DURATION_IN_SECONDS

    def advance(self):
        """Advance to next demo and reset timer."""
        self.current_index += 1

        # Check if we've completed all demos
        if self.current_index >= len(DEMO_SCENARIOS):
            self.completed = True
            self.current_index = len(DEMO_SCENARIOS) - 1  # Stay on last demo
        else:
            self.start_time = time.time()

    def is_completed(self):
        """Check if all demos have been shown."""
        return self.completed


carousel_state = CarouselState()


def get_system_metrics():
    """Generate system metrics dictionary (2 cols)."""
    return {
        "CPU": f"{random.randint(20, 80)}%",
        "Memory": f"{random.randint(2, 8)}GB",
    }


def get_services_list():
    """Generate services list (4 cols)."""
    return [
        {
            "name": "nginx",
            "status": "✓ Running",
            "port": "80",
            "cpu": f"{random.randint(1, 20)}%",
        },
        {
            "name": "postgres",
            "status": "✓ Running",
            "port": "5432",
            "cpu": f"{random.randint(5, 30)}%",
        },
        {
            "name": "redis",
            "status": "✓ Running",
            "port": "6379",
            "cpu": f"{random.randint(1, 10)}%",
        },
    ]


def get_server_metrics():
    """Generate server metrics (7 cols)."""
    return [
        {
            "server": "web-01",
            "cpu": "45%",
            "memory": "2.1GB",
            "disk": "156GB",
            "network": "10MB/s",
            "status": "OK",
            "uptime": "14d",
        },
        {
            "server": "web-02",
            "cpu": "52%",
            "memory": "3.4GB",
            "disk": "189GB",
            "network": "15MB/s",
            "status": "OK",
            "uptime": "14d",
        },
        {
            "server": "db-01",
            "cpu": "68%",
            "memory": "8.2GB",
            "disk": "450GB",
            "network": "5MB/s",
            "status": "OK",
            "uptime": "14d",
        },
    ]


def get_process_data():
    """Generate random process data (7 cols) - changes each call."""
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


def create_demo_1():
    """Demo 1: Small table (2 cols) - Always compact."""
    table = Table.from_dict(
        get_system_metrics(),
        title="System Metrics",
        expand="auto",  # 2 cols < 5, stays compact
    )
    description = "[dim]Narrow table (2 cols) - Always stays compact (< 5 threshold)[/dim]"
    return table, description


def create_demo_2():
    """Demo 2: Medium table (4 cols) - Stays compact."""
    table = Table.from_list_of_dicts(
        get_services_list(),
        title="Services",
        expand="auto",  # 4 cols < 5, stays compact
        row_styles="alternate",
    )
    description = "[dim]Medium table (4 cols) - Stays compact (< 5 threshold)[/dim]"
    return table, description


def create_demo_3():
    """Demo 3: Wide table (7 cols) - Responsive expand."""
    table = Table.from_list_of_dicts(
        get_server_metrics(),
        title="Server Metrics Dashboard",
        expand="auto",  # 7 cols >= 5, expands on wide terminals
        row_styles="alternate",
    )
    description = "[dim]Wide table (7 cols) - Responsive expand (>= 5 threshold)[/dim]"
    return table, description


def create_demo_4():
    """Demo 4: Dynamic updates (7 cols) - Live changing data."""
    table = Table.from_list_of_dicts(
        get_process_data(),
        title=f"Live Process Monitor - {datetime.now().strftime('%H:%M:%S')}",
        expand="auto",  # 7 cols >= 5, expands on wide terminals
        row_styles="severity",
    )
    description = "[dim]Live updates (7 cols) - Data changes every refresh[/dim]"
    return table, description


def create_demo_5():
    """Demo 5: Size comparison - All 3 sizes stacked."""
    small_table = Table.from_dict(get_system_metrics(), title="Narrow (2 cols)", expand="auto")
    small_panel = Panel(small_table, border_style="green", title="Always Compact")

    medium_table = Table.from_list_of_dicts(
        get_services_list(), title="Medium (4 cols)", expand="auto"
    )
    medium_panel = Panel(medium_table, border_style="blue", title="< 5 Threshold")

    wide_table = Table.from_list_of_dicts(
        get_server_metrics()[:2],
        title="Wide (7 cols)",
        expand="auto",  # 2 servers only
    )
    wide_panel = Panel(wide_table, border_style="magenta", title=">= 5 Threshold")

    comparison = Group(small_panel, medium_panel, wide_panel)
    description = "[dim]Size comparison - See all 3 responsive behaviors[/dim]"
    return comparison, description


DEMO_SCENARIOS = [
    ("Compact (2 cols)", create_demo_1),
    ("Medium (4 cols)", create_demo_2),
    ("Wide (7 cols)", create_demo_3),
    ("Live Updates", create_demo_4),
    ("Comparison", create_demo_5),
]


def build_horizontal_stepper(current_index):
    """Build horizontal progress stepper with status indicators."""
    parts = []

    for i, (name, _) in enumerate(DEMO_SCENARIOS):
        if i < current_index:
            # Completed
            parts.append(f"[green]✓ {name}[/green]")
        elif i == current_index:
            # Current
            parts.append(f"[bold yellow]◐ {name}[/bold yellow]")
        else:
            # Pending
            parts.append(f"[dim]○ {name}[/dim]")

    stepper_text = " | ".join(parts)
    return Panel(stepper_text, title="[bold]Progress[/bold]", border_style="blue")


def build_header(current_index, elapsed_time):
    """
    Build header panel with counter and countdown timer.

    Shows: `Demo 2/5 | Next: 8s`
    """
    total_demos = len(DEMO_SCENARIOS)
    counter = f"[bold cyan]Demo {current_index + 1}/{total_demos}[/bold cyan]"

    if carousel_state.is_completed():
        timer = "[bold green]✓ Complete![/bold green]"
    else:
        seconds_remaining = max(0, int(DEMO_DURATION_IN_SECONDS - elapsed_time))
        timer = f"[dim]Next: {seconds_remaining}s[/dim]"

    terminal_width = get_console().width

    if terminal_width < 60:
        breakpoint_info = "[red]Compact[/red] (< 60 cols)"
    elif terminal_width < 80:
        breakpoint_info = "[yellow]Medium[/yellow] (60-80 cols)"
    else:
        breakpoint_info = "[green]Wide[/green] (> 80 cols)"

    header_text = f"{counter} | {timer} | Terminal: {terminal_width} cols ({breakpoint_info})"
    return Panel(header_text, border_style="cyan")


def create_demo_display():
    """Create complete display: header + stepper + current demo table.

    This function is called every 0.1s to update the display.
    """
    if carousel_state.should_advance():
        carousel_state.advance()

    elapsed_time = carousel_state.get_elapsed_time()

    header = build_header(carousel_state.current_index, elapsed_time)
    stepper = build_horizontal_stepper(carousel_state.current_index)

    demo_name, demo_func = DEMO_SCENARIOS[carousel_state.current_index]
    demo_content, description = demo_func()

    demo_panel = Panel(
        Group(Text(description, style="dim italic"), Text(""), demo_content),
        title=f"[bold]{demo_name}[/bold]",
        border_style="magenta",
    )

    return Group(header, stepper, demo_panel)


def main():
    """Run auto-playing carousel demo."""
    console = get_console()

    console.print("\n[bold cyan]═══ Auto-Playing Responsive Table Carousel ═══[/bold cyan]\n")
    console.print("[dim]This demo automatically cycles through 5 table scenarios:[/dim]")
    console.print("[dim]  1. Compact (2 cols) - Always narrow[/dim]")
    console.print("[dim]  2. Medium (4 cols) - Stays compact[/dim]")
    console.print("[dim]  3. Wide (7 cols) - Responsive expand[/dim]")
    console.print("[dim]  4. Live Updates - Data changes in real-time[/dim]")
    console.print("[dim]  5. Comparison - All 3 sizes side-by-side[/dim]")
    console.print()
    console.print("[yellow]Each demo runs for 10 seconds, then auto-advances.[/yellow]")
    console.print("[yellow]Resize the terminal anytime to see responsive behavior![/yellow]")
    console.print("[bold yellow]Press Ctrl+C to exit.[/bold yellow]\n")

    time.sleep(3)

    carousel_state.start()

    initial_display = create_demo_display()

    try:
        with LiveComponent(
            initial_display,
            update_fn=create_demo_display,
            refresh_per_second=10,
            screen=True,
        ) as live:
            while not carousel_state.is_completed():
                time.sleep(0.1)
                live.refresh()

    except KeyboardInterrupt:
        pass

    console.print("\n[green]✓ Carousel demo exited gracefully![/green]")
    console.print("\n[bold]What you saw:[/bold]")
    console.print("  • [cyan]5 different table scenarios[/cyan] cycling automatically")
    console.print("  • [cyan]Horizontal stepper[/cyan] showing progress (✓ ◐ ○)")
    console.print("  • [cyan]Live countdown[/cyan] timer for each demo")
    console.print("  • [cyan]Responsive sizing[/cyan] with expand='auto'")
    console.print("  • [cyan]Terminal width detection[/cyan] and breakpoint display")
    console.print("\n[bold]Responsive breakpoints:[/bold]")
    console.print("  • [red]Compact[/red] (< 60 cols): All tables stay narrow")
    console.print("  • [yellow]Medium[/yellow] (60-80 cols): Wide tables get calculated width")
    console.print("  • [green]Wide[/green] (> 80 cols): Wide tables expand (>= 5 cols)")
    console.print("\n[dim]Try resizing the terminal and running again![/dim]\n")


if __name__ == "__main__":
    main()
