from datetime import datetime
import random
import time

from chalkbox import Table, get_console
from chalkbox.live import LiveComponent, LiveTable


def generate_metrics():
    """Generate random metrics data."""
    return {
        "cpu": random.randint(20, 95),
        "memory": random.randint(40, 90),
        "disk": random.randint(50, 85),
        "network_in": random.randint(10, 100),
        "network_out": random.randint(5, 50),
    }


def demo_simple_live_table():
    """Simple table that stays visible and responsive."""
    console = get_console()

    console.print("\n[bold cyan]═══ Simple Live Table Demo ═══[/bold cyan]")
    console.print("[dim]This table will stay visible and respond to terminal resize[/dim]")
    console.print("[yellow]Press Ctrl+C to stop (will run for 10 seconds)[/yellow]\n")

    # Create a static table
    table = Table(headers=["Metric", "Value", "Status"])
    metrics = generate_metrics()

    for metric, value in metrics.items():
        status = "✓ Normal" if value < 80 else "⚠ High"
        severity = "success" if value < 80 else "warning"
        table.add_row(metric.title(), f"{value}%", status, severity=severity)

    # Make it live - it will respond to resize automatically!
    try:
        with table.live():
            time.sleep(10)
    except KeyboardInterrupt:
        pass

    console.print("[green]✓[/green] Demo completed\n")


def demo_updating_table():
    """Table that updates its content in real-time."""
    console = get_console()

    console.print("\n[bold cyan]═══ Auto-Updating Table Demo ═══[/bold cyan]")
    console.print("[dim]Watch the metrics update in real-time + resize support[/dim]")
    console.print("[yellow]Press Ctrl+C to stop (will run for 10 seconds)[/yellow]\n")

    def create_table():
        """Create table with current metrics."""
        table = Table(
            title=f"System Metrics - {datetime.now().strftime('%H:%M:%S')}",
            headers=["Resource", "Current", "Peak", "Status"],
        )

        metrics = generate_metrics()

        for metric, value in metrics.items():
            peak = value + random.randint(5, 15)
            if value < 70:
                status = "✓ OK"
                severity = "success"
            elif value < 85:
                status = "⚠ Warning"
                severity = "warning"
            else:
                status = "✖ Critical"
                severity = "error"

            table.add_row(
                metric.replace("_", " ").title(),
                f"{value}%",
                f"{peak}%",
                status,
                severity=severity,
            )

        return table

    # Create table with update function
    initial_table = create_table()

    try:
        with initial_table.live(update_fn=create_table, refresh_per_second=2):
            time.sleep(10)
    except KeyboardInterrupt:
        pass

    console.print("[green]✓[/green] Demo completed\n")


def demo_live_table_wrapper():
    """Using LiveTable wrapper for easy updates."""
    console = get_console()

    console.print("\n[bold cyan]═══ LiveTable Wrapper Demo ═══[/bold cyan]")
    console.print("[dim]Using LiveTable for convenient live updates[/dim]")
    console.print("[yellow]Press Ctrl+C to stop (will run for 10 seconds)[/yellow]\n")

    def generate_process_table():
        """Generate a process monitoring table."""
        table = Table(
            title=f"Process Monitor - {datetime.now().strftime('%H:%M:%S')}",
            headers=["PID", "Name", "CPU %", "Memory MB", "Status"],
            show_lines=True,
        )

        processes = [
            ("1234", "nginx", random.randint(1, 15), random.randint(50, 200)),
            ("5678", "postgres", random.randint(5, 30), random.randint(200, 500)),
            ("9012", "python", random.randint(10, 60), random.randint(100, 400)),
            ("3456", "redis", random.randint(1, 10), random.randint(30, 100)),
            ("7890", "node", random.randint(5, 40), random.randint(150, 350)),
        ]

        for pid, name, cpu, mem in processes:
            status = "✓ Running" if cpu < 50 else "⚠ High CPU"
            severity = "success" if cpu < 50 else "warning"
            table.add_row(pid, name, str(cpu), str(mem), status, severity=severity)

        return table

    try:
        with LiveTable(update_fn=generate_process_table, refresh_per_second=2):
            time.sleep(10)
    except KeyboardInterrupt:
        pass

    console.print("[green]✓[/green] Demo completed\n")


def demo_live_component_generic():
    """Using LiveComponent with any component."""
    console = get_console()

    console.print("\n[bold cyan]═══ Generic LiveComponent Demo ═══[/bold cyan]")
    console.print("[dim]LiveComponent works with any ChalkBox component[/dim]")
    console.print("[yellow]Press Ctrl+C to stop (will run for 10 seconds)[/yellow]\n")

    from chalkbox import KeyValue

    def generate_stats():
        """Generate system stats as KeyValue."""
        kv = KeyValue(title="System Statistics")
        kv.add("Timestamp", datetime.now().strftime("%H:%M:%S"))
        kv.add("CPU Usage", f"{random.randint(20, 80)}%")
        kv.add("Memory Used", f"{random.randint(4, 12)} GB")
        kv.add("Disk Free", f"{random.randint(100, 500)} GB")
        kv.add("Active Users", str(random.randint(10, 50)))
        kv.add("Uptime", f"{random.randint(1, 30)} days")
        return kv

    initial_kv = generate_stats()

    try:
        with LiveComponent(initial_kv, update_fn=generate_stats, refresh_per_second=2):
            time.sleep(10)
    except KeyboardInterrupt:
        pass

    console.print("[green]✓[/green] Demo completed\n")


def main():
    """Run all live component demos sequentially."""
    console = get_console()

    console.print(
        "\n[bold magenta]╔════════════════════════════════════════════════╗[/bold magenta]"
    )
    console.print("[bold magenta]║   ChalkBox - Live Components Demo             ║[/bold magenta]")
    console.print(
        "[bold magenta]╚════════════════════════════════════════════════╝[/bold magenta]\n"
    )

    console.print("[bold yellow]Running all demos sequentially...[/bold yellow]\n")

    demos = [
        demo_simple_live_table,
        demo_updating_table,
        demo_live_table_wrapper,
        demo_live_component_generic,
    ]

    for demo_func in demos:
        try:
            demo_func()
        except KeyboardInterrupt:
            console.print("\n[yellow]⚠[/yellow] Demo skipped\n")

    console.print("[bold green]✓  All demos completed![/bold green]\n")


if __name__ == "__main__":
    main()
