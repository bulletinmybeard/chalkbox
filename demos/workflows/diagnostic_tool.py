import argparse
from datetime import datetime
import platform
import random
import time

import psutil
from rich.panel import Panel
from rich.text import Text

from chalkbox import (
    Alert,
    Dashboard,
    KeyValue,
    Progress,
    Section,
    Spinner,
    Stepper,
    Table,
    get_console,
    setup_logging,
)


class SystemDiagnostic:
    """System diagnostic tool."""

    def __init__(self):
        self.console = get_console()
        self.logger = setup_logging(level="INFO")
        self.issues = []
        self.warnings = []
        self.recommendations = []

    @staticmethod
    def get_system_info():
        """Gather system information."""
        with Spinner("Gathering system information...") as spinner:
            time.sleep(1)

            info = {
                "Hostname": platform.node(),
                "Platform": platform.platform(),
                "Processor": platform.processor() or "Unknown",
                "Python Version": platform.python_version(),
                "CPU Cores": psutil.cpu_count(),
                "Total Memory": f"{psutil.virtual_memory().total / (1024**3):.1f} GB",
                "Boot Time": datetime.fromtimestamp(psutil.boot_time()).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            }

            spinner.success("System information collected")

        return info

    def check_resources(self):
        """Check system resources."""
        self.console.print("\n[bold cyan]💻 System Resources[/bold cyan]\n")

        resources = []

        with Progress() as progress:
            task = progress.add_task("Analyzing resources", total=4)

            # CPU check
            cpu_percent = psutil.cpu_percent(interval=1)
            resources.append(
                {
                    "Resource": "CPU Usage",
                    "Current": f"{cpu_percent}%",
                    "Threshold": "80%",
                    "Status": "⚠ Warning" if cpu_percent > 80 else "✓  OK",
                }
            )
            if cpu_percent > 80:
                self.warnings.append(f"High CPU usage: {cpu_percent}%")
            progress.update(task, advance=1)

            # Memory check
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            resources.append(
                {
                    "Resource": "Memory Usage",
                    "Current": f"{memory_percent}%",
                    "Threshold": "85%",
                    "Status": "⚠ Warning" if memory_percent > 85 else "✓  OK",
                }
            )
            if memory_percent > 85:
                self.warnings.append(f"High memory usage: {memory_percent}%")
            progress.update(task, advance=1)

            # Disk check
            disk = psutil.disk_usage("/")
            disk_percent = disk.percent
            resources.append(
                {
                    "Resource": "Disk Usage",
                    "Current": f"{disk_percent}%",
                    "Threshold": "90%",
                    "Status": "✖ Critical"
                    if disk_percent > 90
                    else "⚠ Warning"
                    if disk_percent > 75
                    else "✓  OK",
                }
            )
            if disk_percent > 90:
                self.issues.append(f"Critical disk usage: {disk_percent}%")
            elif disk_percent > 75:
                self.warnings.append(f"High disk usage: {disk_percent}%")
            progress.update(task, advance=1)

            # Swap check
            swap = psutil.swap_memory()
            swap_percent = swap.percent
            resources.append(
                {
                    "Resource": "Swap Usage",
                    "Current": f"{swap_percent}%",
                    "Threshold": "50%",
                    "Status": "⚠ Warning" if swap_percent > 50 else "✓  OK",
                }
            )
            if swap_percent > 50:
                self.warnings.append(f"High swap usage: {swap_percent}%")
            progress.update(task, advance=1)

        # Display results
        table = Table.from_list_of_dicts(resources, title="Resource Status")
        self.console.print(table)

        return resources

    def check_services(self):
        """Check critical services."""
        self.console.print("\n[bold cyan]Service Health Checks[/bold cyan]\n")

        # Simulate service checks
        services = [
            {"name": "Database", "port": 5432, "critical": True},
            {"name": "Redis Cache", "port": 6379, "critical": True},
            {"name": "Web Server", "port": 80, "critical": True},
            {"name": "API Gateway", "port": 8080, "critical": True},
            {"name": "Message Queue", "port": 5672, "critical": False},
            {"name": "Monitoring", "port": 9090, "critical": False},
        ]

        service_status = []

        for service in services:
            with Spinner(f"Checking {service['name']}...") as spinner:
                time.sleep(random.uniform(0.5, 1))

                # Simulate service check
                if random.random() < 0.85:  # 85% services are healthy
                    status = "Running"
                    response_time = f"{random.randint(10, 100)}ms"
                    health = "✓  Healthy"
                    spinner.success(f"{service['name']} is healthy")
                else:
                    status = random.choice(["Stopped", "Degraded", "Unreachable"])
                    response_time = "N/A"
                    health = "✖ Unhealthy"
                    spinner.error(f"{service['name']} is {status.lower()}")

                    if service["critical"]:
                        self.issues.append(
                            f"Critical service '{service['name']}' is {status.lower()}"
                        )
                    else:
                        self.warnings.append(f"Service '{service['name']}' is {status.lower()}")

                service_status.append(
                    {
                        "Service": service["name"],
                        "Port": service["port"],
                        "Status": status,
                        "Response Time": response_time,
                        "Health": health,
                    }
                )

        # Display results
        table = Table.from_list_of_dicts(service_status, title="Service Status")
        self.console.print(table)

        return service_status

    def check_network(self):
        """Check network connectivity."""
        self.console.print("\n[bold cyan]🌐 Network Connectivity[/bold cyan]\n")

        endpoints = [
            {"name": "Internal Gateway", "host": "10.0.0.1", "type": "internal"},
            {"name": "DNS Server", "host": "8.8.8.8", "type": "dns"},
            {"name": "External API", "host": "api.example.com", "type": "external"},
            {"name": "CDN", "host": "cdn.cloudflare.com", "type": "cdn"},
            {"name": "Database Replica", "host": "db-replica.internal", "type": "internal"},
        ]

        connectivity = []

        with Progress() as progress:
            task = progress.add_task("Testing connectivity", total=len(endpoints))

            for endpoint in endpoints:
                # Simulate ping
                time.sleep(0.5)

                if random.random() < 0.9:  # 90% success rate
                    latency = random.randint(1, 100)
                    packet_loss = random.uniform(0, 2)
                    status = "✓  OK"

                    if latency > 50:
                        self.warnings.append(f"High latency to {endpoint['name']}: {latency}ms")
                        status = "⚠ Slow"
                else:
                    latency = None
                    packet_loss = random.uniform(10, 100)
                    status = "✖ Failed"

                    if endpoint["type"] == "internal":
                        self.issues.append(f"Cannot reach internal endpoint: {endpoint['name']}")
                    else:
                        self.warnings.append(f"Cannot reach external endpoint: {endpoint['name']}")

                connectivity.append(
                    {
                        "Endpoint": endpoint["name"],
                        "Host": endpoint["host"],
                        "Latency": f"{latency}ms" if latency else "N/A",
                        "Packet Loss": f"{packet_loss:.1f}%",
                        "Status": status,
                    }
                )

                progress.update(task, advance=1)

        # Display results
        table = Table.from_list_of_dicts(connectivity, title="Network Status")
        self.console.print(table)

        return connectivity

    def analyze_logs(self):
        """Analyze system logs for issues."""
        self.console.print("\n[bold cyan]📝 Log Analysis[/bold cyan]\n")

        log_stats = {
            "errors": 0,
            "warnings": 0,
            "critical": 0,
        }

        with Spinner("Analyzing system logs...") as spinner:
            # Simulate log analysis
            time.sleep(2)

            # Generate random log statistics
            log_stats["errors"] = random.randint(0, 50)
            log_stats["warnings"] = random.randint(10, 100)
            log_stats["critical"] = random.randint(0, 5)

            if log_stats["critical"] > 0:
                spinner.error(f"Found {log_stats['critical']} critical errors in logs")
                self.issues.append(f"{log_stats['critical']} critical errors found in system logs")
            elif log_stats["errors"] > 20:
                spinner.warning(f"Found {log_stats['errors']} errors in logs")
                self.warnings.append(f"{log_stats['errors']} errors found in system logs")
            else:
                spinner.success("Log analysis complete")

        # Show log summary
        with Section("Log Analysis Summary", subtitle="Last 24 hours") as section:
            # Error breakdown
            error_types = [
                {"Type": "Database Connection", "Count": random.randint(0, 20), "Severity": "High"},
                {"Type": "Authentication", "Count": random.randint(0, 10), "Severity": "Medium"},
                {"Type": "File I/O", "Count": random.randint(0, 15), "Severity": "Low"},
                {"Type": "Network Timeout", "Count": random.randint(0, 25), "Severity": "Medium"},
                {"Type": "Memory Allocation", "Count": random.randint(0, 5), "Severity": "High"},
            ]

            table = Table.from_list_of_dicts(error_types, title="Error Breakdown")
            section.add(table)

            section.add_spacing()

            # Overall stats
            stats = {
                "Total Log Entries": f"{random.randint(100000, 500000):,}",
                "Error Rate": f"{log_stats['errors'] / 1000:.2f}%",
                "Warning Rate": f"{log_stats['warnings'] / 1000:.2f}%",
                "Critical Issues": log_stats["critical"],
                "Log Size": f"{random.randint(100, 500)} MB",
            }

            kv = KeyValue(stats)
            section.add(kv)

        return log_stats

    def run_benchmarks(self):
        """Run performance benchmarks."""
        self.console.print("\n[bold cyan]⚡ Performance Benchmarks[/bold cyan]\n")

        benchmarks = []

        tests = [
            ("CPU (single-core)", "calculations/sec"),
            ("Memory bandwidth", "GB/sec"),
            ("Disk I/O (sequential)", "MB/sec"),
            ("Disk I/O (random)", "IOPS"),
            ("Network throughput", "Mbps"),
        ]

        with Progress() as progress:
            for test_name, unit in tests:
                task = progress.add_task(f"Running {test_name}", total=100)

                # Simulate benchmark
                for _i in range(100):
                    time.sleep(0.01)
                    progress.update(task, advance=1)

                # Generate result
                if "CPU" in test_name:
                    result = random.randint(50000, 100000)
                    baseline = 75000
                elif "Memory" in test_name:
                    result = random.uniform(10, 30)
                    baseline = 20
                elif "sequential" in test_name:
                    result = random.randint(100, 500)
                    baseline = 300
                elif "random" in test_name:
                    result = random.randint(5000, 20000)
                    baseline = 10000
                else:  # Network
                    result = random.randint(100, 1000)
                    baseline = 500

                performance = (result / baseline) * 100

                benchmarks.append(
                    {
                        "Test": test_name,
                        "Result": f"{result:,} {unit}"
                        if isinstance(result, int)
                        else f"{result:.1f} {unit}",
                        "Baseline": f"{baseline:,} {unit}"
                        if isinstance(baseline, int)
                        else f"{baseline:.1f} {unit}",
                        "Performance": f"{performance:.0f}%",
                        "Rating": "🟢 Good"
                        if performance > 90
                        else "🟡 Fair"
                        if performance > 70
                        else "🔴 Poor",
                    }
                )

                if performance < 70:
                    self.warnings.append(
                        f"Poor {test_name} performance: {performance:.0f}% of baseline"
                    )

        # Display results
        table = Table.from_list_of_dicts(benchmarks, title="Performance Benchmarks")
        self.console.print(table)

        return benchmarks

    def generate_recommendations(self):
        """Generate recommendations based on diagnostics."""
        if self.issues:
            self.recommendations.append("🔴 Address critical issues immediately")
            for issue in self.issues[:3]:
                self.recommendations.append(f"  • Fix: {issue}")

        if self.warnings:
            self.recommendations.append("🟡 Review and monitor warnings")
            for warning in self.warnings[:3]:
                self.recommendations.append(f"  • Check: {warning}")

        # General recommendations
        self.recommendations.extend(
            [
                "Schedule regular system maintenance",
                "Implement automated monitoring alerts",
                "Review and optimize resource allocation",
                "Update system and service configurations",
            ]
        )


def run_diagnostic():
    """Run complete system diagnostic."""
    console = get_console()

    console.print("[bold magenta]═══════════════════════════════════════════════[/bold magenta]")
    console.print("[bold magenta]         System Diagnostic Tool v3.0[/bold magenta]")
    console.print("[bold magenta]═══════════════════════════════════════════════[/bold magenta]\n")

    diagnostic = SystemDiagnostic()

    # Diagnostic steps
    steps = [
        "Gather system information",
        "Check system resources",
        "Verify service health",
        "Test network connectivity",
        "Analyze system logs",
        "Run performance benchmarks",
        "Generate report",
    ]

    stepper = Stepper.from_list(steps, title="Diagnostic Process")
    console.print(stepper)
    console.print()

    # Step 1: System info
    stepper.start(0)
    system_info = diagnostic.get_system_info()

    with Section("System Information") as section:
        kv = KeyValue(system_info)
        section.add(kv)

    stepper.complete(0)

    # Step 2: Resources
    stepper.start(1)
    _resources = diagnostic.check_resources()  # Result not used - method called for side effects
    stepper.complete(1)

    # Step 3: Services
    stepper.start(2)
    services = diagnostic.check_services()
    stepper.complete(2)

    # Step 4: Network
    stepper.start(3)
    network = diagnostic.check_network()
    stepper.complete(3)

    # Step 5: Logs
    stepper.start(4)
    _logs = diagnostic.analyze_logs()  # Result not used - method called for side effects
    stepper.complete(4)

    # Step 6: Benchmarks
    stepper.start(5)
    _benchmarks = diagnostic.run_benchmarks()  # Result not used - method called for side effects
    stepper.complete(5)

    # Step 7: Report
    stepper.start(6)
    diagnostic.generate_recommendations()

    # Generate diagnostic report
    console.print("\n[bold cyan]📋 Diagnostic Report[/bold cyan]\n")

    with Section(
        "Diagnostic Summary", subtitle=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ) as section:
        summary = {
            "Critical Issues": len(diagnostic.issues),
            "Warnings": len(diagnostic.warnings),
            "Services Checked": len(services),
            "Network Endpoints": len(network),
            "Overall Health": "Critical"
            if diagnostic.issues
            else "⚠ Warning"
            if diagnostic.warnings
            else "✓  Healthy",
        }

        kv = KeyValue(summary)
        section.add(kv)

        # Issues and warnings
        if diagnostic.issues:
            section.add_spacing()
            section.add_text("Critical Issues:", style="bold red")
            for issue in diagnostic.issues:
                section.add_text(f"  • {issue}", style="red")

        if diagnostic.warnings:
            section.add_spacing()
            section.add_text("Warnings:", style="bold yellow")
            for warning in diagnostic.warnings[:5]:
                section.add_text(f"  • {warning}", style="yellow")
            if len(diagnostic.warnings) > 5:
                section.add_text(f"  ... and {len(diagnostic.warnings) - 5} more", style="dim")

        # Recommendations
        section.add_spacing()
        section.add_text("Recommendations:", style="bold cyan")
        for rec in diagnostic.recommendations[:5]:
            section.add_text(rec, style="cyan")

    stepper.complete(6)

    # Final display
    console.print("\n")
    console.print(stepper)

    # Final status
    console.print("\n")
    if diagnostic.issues:
        console.print(
            Alert.error(
                "System requires immediate attention",
                details=f"Found {len(diagnostic.issues)} critical issues",
            )
        )
    elif diagnostic.warnings:
        console.print(
            Alert.warning(
                "System health is degraded", details=f"Found {len(diagnostic.warnings)} warnings"
            )
        )
    else:
        console.print(
            Alert.success("System is healthy", details="All diagnostics passed successfully")
        )

    diagnostic.logger.info(
        f"Diagnostic complete: {len(diagnostic.issues)} issues, {len(diagnostic.warnings)} warnings"
    )


def run_live_monitoring():
    """Run live system monitoring dashboard."""
    console = get_console()

    console.print("[bold magenta]═══════════════════════════════════════════════[/bold magenta]")
    console.print("[bold magenta]     Live System Monitoring Dashboard[/bold magenta]")
    console.print("[bold magenta]═══════════════════════════════════════════════[/bold magenta]\n")

    console.print("[dim]Starting live monitoring. Resize terminal to see responsive layout.[/dim]")
    console.print("[yellow]Press Ctrl+C to stop[/yellow]\n")

    time.sleep(2)

    # Create dashboard
    dashboard = Dashboard.create("full")

    # Header with timestamp
    def update_header():
        return Panel(
            f"[bold cyan]System Monitor[/bold cyan] - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            border_style="cyan",
        )

    dashboard.set_header(Text(""), update_fn=update_header)

    # Sidebar with system info
    def update_sidebar():
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        kv = KeyValue(title="Quick Stats")
        kv.add("CPU", f"{cpu_percent:.1f}%")
        kv.add("Memory", f"{memory.percent:.1f}%")
        kv.add("Disk", f"{disk.percent:.1f}%")
        kv.add("Processes", str(len(psutil.pids())))

        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        days = uptime.days
        hours = uptime.seconds // 3600
        kv.add("Uptime", f"{days}d {hours}h")

        return Panel(kv, border_style="cyan")

    dashboard.set_sidebar(Text(""), update_fn=update_sidebar)

    # Main content with detailed metrics
    def update_main():
        # Get current metrics
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        net = psutil.net_io_counters()

        table = Table(
            headers=["Resource", "Current", "Total", "Status"],
            show_lines=True,
        )

        # CPU
        cpu_status = (
            "✓ Normal" if cpu_percent < 70 else "⚠ High" if cpu_percent < 85 else "✖ Critical"
        )
        cpu_severity = "success" if cpu_percent < 70 else "warning" if cpu_percent < 85 else "error"
        table.add_row(
            "CPU Usage",
            f"{cpu_percent:.1f}%",
            f"{psutil.cpu_count()} cores",
            cpu_status,
            severity=cpu_severity,
        )

        # Memory
        mem_used_gb = memory.used / (1024**3)
        mem_total_gb = memory.total / (1024**3)
        mem_status = (
            "✓ Normal" if memory.percent < 75 else "⚠ High" if memory.percent < 90 else "✖ Critical"
        )
        mem_severity = (
            "success" if memory.percent < 75 else "warning" if memory.percent < 90 else "error"
        )
        table.add_row(
            "Memory",
            f"{memory.percent:.1f}% ({mem_used_gb:.1f} GB)",
            f"{mem_total_gb:.1f} GB",
            mem_status,
            severity=mem_severity,
        )

        # Disk
        disk_used_gb = disk.used / (1024**3)
        disk_total_gb = disk.total / (1024**3)
        disk_status = (
            "✓ Normal" if disk.percent < 80 else "⚠ High" if disk.percent < 90 else "✖ Critical"
        )
        disk_severity = (
            "success" if disk.percent < 80 else "warning" if disk.percent < 90 else "error"
        )
        table.add_row(
            "Disk Space",
            f"{disk.percent:.1f}% ({disk_used_gb:.0f} GB)",
            f"{disk_total_gb:.0f} GB",
            disk_status,
            severity=disk_severity,
        )

        # Network
        net_in_mb = net.bytes_recv / (1024**2)
        net_out_mb = net.bytes_sent / (1024**2)
        table.add_row(
            "Network I/O",
            f"↓ {net_in_mb:.0f} MB / ↑ {net_out_mb:.0f} MB",
            "Since boot",
            "✓ Active",
            severity="success",
        )

        return Panel(table, title="Resource Usage", border_style="green")

    dashboard.set_main(update_fn=update_main)

    # Footer with status
    def update_footer():
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory_percent = psutil.virtual_memory().percent

        status_text = "● "
        if cpu_percent > 85 or memory_percent > 90:
            status_text += "[red]Critical[/red]"
        elif cpu_percent > 70 or memory_percent > 75:
            status_text += "[yellow]Warning[/yellow]"
        else:
            status_text += "[green]Healthy[/green]"

        return Panel(
            f"[dim]Status: {status_text} | Last updated: {datetime.now().strftime('%H:%M:%S')} | Press Ctrl+C to exit[/dim]",
            border_style="blue",
        )

    dashboard.set_footer(Text(""), update_fn=update_footer)

    # Run the dashboard
    try:
        dashboard.run(refresh_per_second=2)
    except KeyboardInterrupt:
        console.print("\n[green]✓[/green] Monitoring stopped\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="System Diagnostic Tool - Check system health or monitor in real-time",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s              Run complete diagnostic (default)
  %(prog)s --live       Start live monitoring dashboard

The live mode shows real-time system metrics with automatic terminal resize support.
        """,
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Run live monitoring dashboard (responsive to terminal resize)",
    )

    args = parser.parse_args()

    if args.live:
        run_live_monitoring()
    else:
        run_diagnostic()
