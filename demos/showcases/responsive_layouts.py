from datetime import datetime
import random
import time

from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from chalkbox import (
    Alert,
    ColumnLayout,
    KeyValue,
    MultiPanel,
    Table,
    get_console,
)


def get_timestamp() -> str:
    """Get current timestamp string."""
    return datetime.now().strftime("%H:%M:%S")


def generate_metrics() -> dict:
    """Generate simulated system metrics."""
    return {
        "cpu": random.randint(20, 80),
        "memory": random.randint(40, 90),
        "disk": random.randint(60, 95),
        "network_in": random.randint(10, 100),
        "network_out": random.randint(5, 50),
        "processes": random.randint(150, 250),
        "uptime": "3d 14h 27m",
    }


def demo_simple_responsive():
    """Simple responsive table that adjusts to terminal size."""
    console = get_console()

    console.print("\n[bold cyan]═══ Simple Responsive Demo ═══[/bold cyan]")
    console.print("[dim]Resize your terminal to see the table adjust automatically![/dim]")
    console.print("[yellow]Press Ctrl+C to stop[/yellow]\n")

    def make_table():
        """Create a table with current metrics."""
        metrics = generate_metrics()
        table = Table(headers=["Metric", "Value", "Status"])

        # CPU
        cpu_status = "✓ Normal" if metrics["cpu"] < 70 else "⚠ High"
        cpu_severity = "success" if metrics["cpu"] < 70 else "warning"
        table.add_row("CPU Usage", f"{metrics['cpu']}%", cpu_status, severity=cpu_severity)

        # Memory
        mem_status = "✓ Normal" if metrics["memory"] < 80 else "⚠ High"
        mem_severity = "success" if metrics["memory"] < 80 else "warning"
        table.add_row("Memory", f"{metrics['memory']}%", mem_status, severity=mem_severity)

        # Disk
        disk_status = "✓ OK" if metrics["disk"] < 90 else "⚠ Critical"
        disk_severity = "success" if metrics["disk"] < 90 else "error"
        table.add_row("Disk Space", f"{metrics['disk']}%", disk_status, severity=disk_severity)

        # Network
        table.add_row(
            "Network In",
            f"{metrics['network_in']} MB/s",
            "✓ Active",
            severity="success",
        )
        table.add_row(
            "Network Out",
            f"{metrics['network_out']} MB/s",
            "✓ Active",
            severity="success",
        )

        return Panel(
            table,
            title=f"[bold cyan]System Metrics[/bold cyan] - {get_timestamp()}",
            border_style="cyan",
        )

    try:
        with Live(make_table(), refresh_per_second=2, screen=False) as live:
            while True:
                time.sleep(0.5)
                live.update(make_table())
    except KeyboardInterrupt:
        console.print("\n[green]✓[/green] Demo stopped\n")


def demo_dashboard():
    """Full dashboard layout with multiple panels."""
    console = get_console()

    console.print("\n[bold cyan]═══ Responsive Dashboard Demo ═══[/bold cyan]")
    console.print("[dim]Resize your terminal to see the entire layout adjust![/dim]")
    console.print("[yellow]Press Ctrl+C to stop[/yellow]\n")

    def make_dashboard():
        """Create full dashboard layout."""
        layout = Layout()

        # Split into header, body, footer
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3),
        )

        # Split body into sidebar and main
        layout["body"].split_row(
            Layout(name="sidebar", size=30),
            Layout(name="main"),
        )

        # Header
        header_text = Text()
        header_text.append("🔥 ChalkBox Dashboard", style="bold magenta")
        header_text.append(f"    |    {get_timestamp()}", style="dim")
        layout["header"].update(Panel(header_text, border_style="magenta", padding=(0, 2)))

        # Sidebar
        metrics = generate_metrics()
        sidebar_kv = KeyValue()
        sidebar_kv.add("CPU", f"{metrics['cpu']}%")
        sidebar_kv.add("Memory", f"{metrics['memory']}%")
        sidebar_kv.add("Disk", f"{metrics['disk']}%")
        sidebar_kv.add("Processes", str(metrics["processes"]))
        sidebar_kv.add("Uptime", metrics["uptime"])

        layout["sidebar"].update(
            Panel(sidebar_kv, title="[bold]Quick Stats[/bold]", border_style="cyan")
        )

        # Main content
        main_table = Table(headers=["Service", "Status", "Port", "Uptime"])
        services = [
            ("Web Server", "✓ Running", "8080", "3d 14h"),
            ("Database", "✓ Running", "5432", "3d 14h"),
            ("Cache", "✓ Running", "6379", "3d 14h"),
            ("Queue", "⚠ Degraded", "5672", "2h 15m"),
        ]

        for service, status, port, uptime in services:
            severity = "success" if "Running" in status else "warning"
            main_table.add_row(service, status, port, uptime, severity=severity)

        # Add some alerts
        alerts = []
        if metrics["memory"] > 80:
            alerts.append(Alert.warning("High memory usage detected"))
        if metrics["disk"] > 90:
            alerts.append(Alert.error("Disk space critical"))

        main_content = []
        main_content.append(main_table)
        if alerts:
            main_content.extend([Text(), *alerts])

        layout["main"].update(
            Panel(
                "\n".join(str(item) for item in main_content),
                title="[bold]Service Status[/bold]",
                border_style="green",
            )
        )

        # Footer
        footer_text = Text()
        footer_text.append("◉ ", style="green")
        footer_text.append("Connected    ", style="dim")
        footer_text.append(f"Last update: {get_timestamp()}    ", style="dim")
        footer_text.append("[Ctrl+C to exit]", style="yellow dim")

        layout["footer"].update(Panel(footer_text, border_style="blue", padding=(0, 2)))

        return layout

    try:
        with Live(make_dashboard(), refresh_per_second=2, screen=True) as live:
            while True:
                time.sleep(0.5)
                live.update(make_dashboard())
    except KeyboardInterrupt:
        console.print("\n[green]✓[/green] Demo stopped\n")


def demo_monitoring():
    """Real-time monitoring view with columns and live updates."""
    console = get_console()

    console.print("\n[bold cyan]═══ Live Monitoring Demo ═══[/bold cyan]")
    console.print("[dim]Watch metrics update in real-time - resize to see adaptation![/dim]")
    console.print("[yellow]Press Ctrl+C to stop[/yellow]\n")

    iteration = 0

    def make_monitoring():
        """Create monitoring layout."""
        nonlocal iteration
        iteration += 1

        layout = Layout()
        layout.split_column(
            Layout(name="header", size=5),
            Layout(name="metrics"),
            Layout(name="columns", size=8),
            Layout(name="footer", size=3),
        )

        # Header with title and divider
        header_content = Text()
        header_content.append("⚡ Real-Time System Monitor\n", style="bold yellow")
        header_content.append("─" * 60 + "\n", style="dim")
        header_content.append(f"Iteration: {iteration}  |  ", style="dim")
        header_content.append(f"Time: {get_timestamp()}", style="cyan")

        layout["header"].update(Panel(header_content, border_style="yellow"))

        # Metrics table
        metrics = generate_metrics()
        metrics_table = Table(headers=["Resource", "Current", "Average", "Peak"])

        cpu_severity = (
            "error" if metrics["cpu"] > 75 else "warning" if metrics["cpu"] > 60 else "success"
        )
        metrics_table.add_row(
            "CPU",
            f"{metrics['cpu']}%",
            f"{metrics['cpu'] - 5}%",
            "87%",
            severity=cpu_severity,
        )

        mem_severity = (
            "error"
            if metrics["memory"] > 85
            else "warning"
            if metrics["memory"] > 70
            else "success"
        )
        metrics_table.add_row(
            "Memory",
            f"{metrics['memory']}%",
            f"{metrics['memory'] - 3}%",
            "92%",
            severity=mem_severity,
        )

        disk_severity = (
            "error" if metrics["disk"] > 90 else "warning" if metrics["disk"] > 80 else "success"
        )
        metrics_table.add_row(
            "Disk",
            f"{metrics['disk']}%",
            f"{metrics['disk'] - 2}%",
            "95%",
            severity=disk_severity,
        )

        layout["metrics"].update(
            Panel(metrics_table, title="[bold]Resource Usage[/bold]", border_style="green")
        )

        # Columns with network stats
        network_data = {
            "In (MB/s)": str(metrics["network_in"]),
            "Out (MB/s)": str(metrics["network_out"]),
            "Processes": str(metrics["processes"]),
            "Threads": str(metrics["processes"] * 3),
        }

        columns = ColumnLayout.from_dict(network_data, equal=True)
        layout["columns"].update(
            Panel(columns, title="[bold]Network & Processes[/bold]", border_style="blue")
        )

        # Footer
        footer_text = Text()
        footer_text.append("● ", style="bold green")
        footer_text.append("System monitoring active    ", style="dim")
        footer_text.append(f"Uptime: {metrics['uptime']}", style="cyan")

        layout["footer"].update(Panel(footer_text, border_style="dim", padding=(0, 2)))

        return layout

    try:
        with Live(make_monitoring(), refresh_per_second=2, screen=True) as live:
            while True:
                time.sleep(0.5)
                live.update(make_monitoring())
    except KeyboardInterrupt:
        console.print("\n[green]✓[/green] Demo stopped\n")


def demo_multipanel_live():
    """Show MultiPanel component in live mode."""
    console = get_console()

    console.print("\n[bold cyan]═══ MultiPanel Live Demo ═══[/bold cyan]")
    console.print("[dim]ChalkBox MultiPanel components adapt to terminal size![/dim]")
    console.print("[yellow]Press Ctrl+C to stop[/yellow]\n")

    def make_multipanel():
        """Create MultiPanel layout."""
        metrics = generate_metrics()

        # Create panels for grid
        panels = {
            "CPU": Panel(
                f"[bold]{metrics['cpu']}%[/bold]\n{'█' * (metrics['cpu'] // 10)}{'░' * (10 - metrics['cpu'] // 10)}",
                border_style="yellow",
            ),
            "Memory": Panel(
                f"[bold]{metrics['memory']}%[/bold]\n{'█' * (metrics['memory'] // 10)}{'░' * (10 - metrics['memory'] // 10)}",
                border_style="yellow",
            ),
            "Disk": Panel(
                f"[bold]{metrics['disk']}%[/bold]\n{'█' * (metrics['disk'] // 10)}{'░' * (10 - metrics['disk'] // 10)}",
                border_style="yellow",
            ),
            "Network": Panel(
                f"[bold]↓ {metrics['network_in']} MB/s[/bold]\n[bold]↑ {metrics['network_out']} MB/s[/bold]",
                border_style="yellow",
            ),
        }

        # Create header
        header = Panel(
            f"[bold magenta]System Dashboard[/bold magenta] - {get_timestamp()}",
            border_style="magenta",
        )

        # Create sidebar
        sidebar_content = f"[bold]Status[/bold]\n\nProcesses: {metrics['processes']}\nUptime: {metrics['uptime']}\n\n[green]● Online[/green]"
        sidebar = Panel(sidebar_content, title="Info", border_style="cyan")

        # Create main content with grid
        main = Panel(
            MultiPanel.create_grid(panels, rows=2, cols=2),
            title="Metrics Grid",
            border_style="green",
        )

        # Create footer
        footer = Panel(
            f"[dim]Last updated: {get_timestamp()} | Press Ctrl+C to exit[/dim]",
            border_style="blue",
        )

        # Combine into dashboard
        return MultiPanel.create_dashboard(
            header, sidebar, main, footer, header_size=3, sidebar_width=22, footer_size=3
        )

    try:
        with Live(make_multipanel(), refresh_per_second=2, screen=True) as live:
            while True:
                time.sleep(0.5)
                live.update(make_multipanel())
    except KeyboardInterrupt:
        console.print("\n[green]✓[/green] Demo stopped\n")


def main():
    """Run all responsive demos sequentially."""
    console = get_console()

    console.print(
        "\n[bold magenta]╔════════════════════════════════════════════════╗[/bold magenta]"
    )
    console.print("[bold magenta]║   ChalkBox - Responsive TUI Demo              ║[/bold magenta]")
    console.print(
        "[bold magenta]╚════════════════════════════════════════════════╝[/bold magenta]\n"
    )

    console.print("[bold yellow]Running all demos sequentially...[/bold yellow]")
    console.print("[dim]Each demo runs for ~10 seconds[/dim]\n")

    demos = [
        ("Simple Responsive Table", demo_simple_responsive),
        ("Full Dashboard", demo_dashboard),
        ("Live Monitoring", demo_monitoring),
        ("MultiPanel Live", demo_multipanel_live),
    ]

    for name, demo_func in demos:
        console.print(f"\n[bold cyan]▶ Starting: {name}[/bold cyan]")
        try:
            # Run each demo for limited time
            import signal

            def timeout_handler(signum, frame):
                raise KeyboardInterrupt

            # Set timeout for demo
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(10)  # 10 second timeout

            try:
                demo_func()
            except KeyboardInterrupt:
                signal.alarm(0)  # Cancel alarm
                console.print(f"[green]✓[/green] {name} completed\n")
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] Demo skipped: {e}\n")

    console.print("[bold green]✓  All demos completed![/bold green]\n")


if __name__ == "__main__":
    main()
