import contextlib
from datetime import datetime
import random
import time

from rich.panel import Panel
from rich.text import Text

from chalkbox import KeyValue, Table, get_console
from chalkbox.live import Dashboard


def generate_metrics():
    """Generate random system metrics."""
    return {
        "cpu": random.randint(20, 80),
        "memory": random.randint(40, 90),
        "disk": random.randint(50, 85),
        "network_in": random.randint(10, 100),
        "network_out": random.randint(5, 50),
        "processes": random.randint(150, 250),
    }


def demo_simple_dashboard():
    """Simple dashboard with header and main content."""
    console = get_console()

    console.print("\n[bold cyan]═══ Simple Dashboard Demo ═══[/bold cyan]")
    console.print("[dim]Basic dashboard with header and auto-updating main content[/dim]")
    console.print("[yellow]Press Ctrl+C to stop (will run for 10 seconds)[/yellow]\n")

    # Create dashboard
    dashboard = Dashboard.create("header_footer")

    # Set static header
    dashboard.set_header("[bold cyan]System Monitor Dashboard[/bold cyan]")

    # Set dynamic main content
    def update_main():
        metrics = generate_metrics()
        table = Table(headers=["Metric", "Value", "Status"])

        for metric, value in metrics.items():
            status = "✓ OK" if value < 80 else "⚠ Warning"
            severity = "success" if value < 80 else "warning"
            table.add_row(
                metric.replace("_", " ").title(),
                f"{value}{'%' if metric != 'processes' else ''}",
                status,
                severity=severity,
            )

        return Panel(table, title="System Metrics", border_style="green")

    dashboard.set_main(update_fn=update_main)

    # Set dynamic footer
    def update_footer():
        timestamp = datetime.now().strftime("%H:%M:%S")
        return Panel(
            f"[dim]Last updated: {timestamp} | Press Ctrl+C to exit[/dim]",
            border_style="blue",
        )

    dashboard.set_footer(Text(""), update_fn=update_footer)

    # Run for 10 seconds
    with contextlib.suppress(KeyboardInterrupt):
        dashboard.run(refresh_per_second=2, duration=10)

    console.print("\n[green]✓[/green] Demo completed\n")


def demo_sidebar_dashboard():
    """Dashboard with sidebar showing quick stats."""
    console = get_console()

    console.print("\n[bold cyan]═══ Sidebar Dashboard Demo ═══[/bold cyan]")
    console.print("[dim]Dashboard with sidebar for quick stats[/dim]")
    console.print("[yellow]Press Ctrl+C to stop (will run for 10 seconds)[/yellow]\n")

    dashboard = Dashboard.create("sidebar_left")

    # Header
    dashboard.set_header("[bold magenta]Application Monitor[/bold magenta]")

    # Dynamic sidebar
    def update_sidebar():
        metrics = generate_metrics()
        kv = KeyValue(title="Quick Stats")
        kv.add("CPU", f"{metrics['cpu']}%")
        kv.add("Memory", f"{metrics['memory']}%")
        kv.add("Disk", f"{metrics['disk']}%")
        kv.add("Processes", str(metrics["processes"]))
        kv.add("Uptime", "3d 14h")
        return Panel(kv, border_style="cyan")

    dashboard.set_sidebar(Text(""), update_fn=update_sidebar)

    # Dynamic main content
    def update_main():
        table = Table(headers=["Service", "Status", "Port", "CPU %"])

        services = [
            ("nginx", "✓ Running", "80", random.randint(5, 20)),
            ("postgres", "✓ Running", "5432", random.randint(10, 30)),
            ("redis", "✓ Running", "6379", random.randint(2, 10)),
            ("node", "✓ Running", "3000", random.randint(15, 40)),
        ]

        for name, status, port, cpu in services:
            severity = "success" if cpu < 30 else "warning"
            table.add_row(name, status, port, f"{cpu}%", severity=severity)

        return Panel(table, title="Services", border_style="green")

    dashboard.set_main(update_fn=update_main)

    # Footer
    def update_footer():
        return Panel(
            f"[dim]Active: {datetime.now().strftime('%H:%M:%S')}[/dim]",
            border_style="blue",
        )

    dashboard.set_footer(Text(""), update_fn=update_footer)

    with contextlib.suppress(KeyboardInterrupt):
        dashboard.run(refresh_per_second=2, duration=10)

    console.print("\n[green]✓[/green] Demo completed\n")


def demo_full_dashboard():
    """Full dashboard with all sections."""
    console = get_console()

    console.print("\n[bold cyan]═══ Full Dashboard Demo ═══[/bold cyan]")
    console.print("[dim]Complete dashboard with header, sidebar, main, and footer[/dim]")
    console.print("[yellow]Press Ctrl+C to stop (will run for 10 seconds)[/yellow]\n")

    dashboard = Dashboard.create("full")

    # Dynamic header
    def update_header():
        return Panel(
            f"[bold yellow]Live System Dashboard[/bold yellow] - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            border_style="yellow",
        )

    dashboard.set_header(Text(""), update_fn=update_header)

    # Sidebar
    def update_sidebar():
        metrics = generate_metrics()
        content = Text()
        content.append("[bold]System Info[/bold]\n\n", style="cyan")
        content.append(f"CPU: {metrics['cpu']}%\n")
        content.append(f"RAM: {metrics['memory']}%\n")
        content.append(f"Disk: {metrics['disk']}%\n")
        content.append("\n[bold]Network[/bold]\n\n", style="cyan")
        content.append(f"↓ {metrics['network_in']} MB/s\n")
        content.append(f"↑ {metrics['network_out']} MB/s\n")
        content.append("\n[bold]Status[/bold]\n\n", style="cyan")
        content.append("● ", style="green")
        content.append("All systems operational")
        return Panel(content, title="Overview", border_style="cyan")

    dashboard.set_sidebar(Text(""), update_fn=update_sidebar)

    # Main
    def update_main():
        metrics = generate_metrics()
        table = Table(
            headers=["Resource", "Current", "Average", "Peak"],
            show_lines=True,
        )

        resources = [
            ("CPU", metrics["cpu"], metrics["cpu"] - 5, metrics["cpu"] + 10),
            ("Memory", metrics["memory"], metrics["memory"] - 3, metrics["memory"] + 8),
            ("Disk I/O", metrics["disk"], metrics["disk"] - 10, metrics["disk"] + 5),
        ]

        for name, current, avg, peak in resources:
            severity = "success" if current < 70 else "warning" if current < 85 else "error"
            table.add_row(
                name,
                f"{current}%",
                f"{avg}%",
                f"{peak}%",
                severity=severity,
            )

        return Panel(table, title="Resource Usage", border_style="green")

    dashboard.set_main(update_fn=update_main)

    # Footer
    def update_footer():
        metrics = generate_metrics()
        return Panel(
            f"[dim]Processes: {metrics['processes']} | Last update: {datetime.now().strftime('%H:%M:%S')}[/dim]",
            border_style="blue",
        )

    dashboard.set_footer(Text(""), update_fn=update_footer)

    with contextlib.suppress(KeyboardInterrupt):
        dashboard.run(refresh_per_second=2, duration=10)

    console.print("\n[green]✓[/green] Demo completed\n")


def demo_quick_monitor():
    """Using the quick_monitor helper."""
    console = get_console()

    console.print("\n[bold cyan]═══ Quick Monitor Demo ═══[/bold cyan]")
    console.print("[dim]Using Dashboard.quick_monitor() helper[/dim]")
    console.print("[yellow]Press Ctrl+C to stop (will run for 10 seconds)[/yellow]\n")

    def metrics_fn():
        metrics = generate_metrics()
        table = Table(headers=["Metric", "Value", "Threshold", "Status"])

        data = [
            ("CPU", metrics["cpu"], 75),
            ("Memory", metrics["memory"], 80),
            ("Disk", metrics["disk"], 85),
        ]

        for name, value, threshold in data:
            status = "✓ OK" if value < threshold else "⚠ High"
            severity = "success" if value < threshold else "warning"
            table.add_row(name, f"{value}%", f"{threshold}%", status, severity=severity)

        return table

    def sidebar_fn():
        kv = KeyValue()
        kv.add("Uptime", "3d 14h 27m")
        kv.add("Users", str(random.randint(10, 50)))
        kv.add("Load Avg", f"{random.uniform(1.0, 3.0):.2f}")
        return kv

    try:
        # This will run indefinitely, so we'll wrap it in a timer
        import threading

        def run_monitor():
            Dashboard.quick_monitor(
                title="Quick System Monitor",
                metrics_fn=metrics_fn,
                sidebar_fn=sidebar_fn,
                refresh_per_second=2,
            )

        thread = threading.Thread(target=run_monitor, daemon=True)
        thread.start()
        time.sleep(10)

    except KeyboardInterrupt:
        pass

    console.print("\n[green]✓[/green] Demo completed\n")


def main():
    """Run all dashboard builder demos sequentially."""
    console = get_console()

    console.print(
        "\n[bold magenta]╔════════════════════════════════════════════════╗[/bold magenta]"
    )
    console.print("[bold magenta]║   ChalkBox - Dashboard Builder Demo           ║[/bold magenta]")
    console.print(
        "[bold magenta]╚════════════════════════════════════════════════╝[/bold magenta]\n"
    )

    console.print("[bold yellow]Running all demos sequentially...[/bold yellow]\n")

    demos = [
        demo_simple_dashboard,
        demo_sidebar_dashboard,
        demo_full_dashboard,
        demo_quick_monitor,
    ]

    for demo_func in demos:
        try:
            demo_func()
        except KeyboardInterrupt:
            console.print("\n[yellow]⚠[/yellow] Demo skipped\n")

    console.print("[bold green]✓  All demos completed![/bold green]\n")


if __name__ == "__main__":
    main()
