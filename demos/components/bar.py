import time
from typing import Literal, cast

from chalkbox import Alert, Bar, Divider, KeyValue, Section, get_console

console = get_console()

console.print("\n[bold cyan]Bar Component Demo[/bold cyan]\n")

console.print(Divider("Basic Percentage Bars"))
console.print("\n[bold]Simple percentage displays:[/bold]\n")

console.print("Low usage  (25%): ", end="")
console.print(Bar.percentage(25))

console.print("Medium usage (50%): ", end="")
console.print(Bar.percentage(50))

console.print("High usage (75%): ", end="")
console.print(Bar.percentage(75))

console.print("Full (100%): ", end="")
console.print(Bar.percentage(100))

time.sleep(1)

console.print("\n")
console.print(Divider("Severity-Based Bars"))
console.print("\n[bold]Automatic severity coloring:[/bold]\n")

console.print("✓ Success (45%): ", end="")
console.print(Bar.percentage(45, severity="success"))

console.print("⚠ Warning (75%): ", end="")
console.print(Bar.percentage(75, severity="warning"))

console.print("✖ Error (92%): ", end="")
console.print(Bar.percentage(92, severity="error"))

console.print("ℹ Info (60%): ", end="")
console.print(Bar.percentage(60, severity="info"))

time.sleep(1)

console.print("\n")
console.print(Divider("Fraction Bars"))
console.print("\n[bold]Display fractions (e.g., memory usage):[/bold]\n")

console.print("Memory: ", end="")
console.print(Bar.fraction(512, 1024, severity="success"))
console.print("         512MB / 1024MB\n")

console.print("Disk:   ", end="")
console.print(Bar.fraction(780, 1000, severity="warning"))
console.print("         780GB / 1000GB\n")

console.print("CPU:    ", end="")
console.print(Bar.fraction(95, 100, severity="error"))
console.print("         95% / 100%\n")

time.sleep(1)

console.print("\n")
console.print(Divider("Custom Widths"))
console.print("\n[bold]Bars with different widths:[/bold]\n")

console.print("Width 20: ", end="")
console.print(Bar.percentage(60, width=20))

console.print("Width 40: ", end="")
console.print(Bar.percentage(60, width=40))

console.print("Width 60: ", end="")
console.print(Bar.percentage(60, width=60))

time.sleep(1)

console.print("\n")
console.print(Divider("Ratio Bars"))
console.print("\n[bold]Display ratios (0.0 = 0%, 1.0 = 100%):[/bold]\n")

console.print("Rating 0.25: ", end="")
console.print(Bar.from_ratio(0.25, severity="error"))

console.print("Rating 0.50: ", end="")
console.print(Bar.from_ratio(0.50, severity="warning"))

console.print("Rating 0.75: ", end="")
console.print(Bar.from_ratio(0.75, severity="info"))

console.print("Rating 0.95: ", end="")
console.print(Bar.from_ratio(0.95, severity="success"))

time.sleep(1)

console.print("\n")
console.print(Divider("System Metrics Dashboard"))
console.print("\n[bold]Complete system metrics example:[/bold]\n")

with Section("System Resources", subtitle="Current Usage") as section:
    cpu_percent = 67
    cpu_bar = Bar.percentage(cpu_percent, severity="warning" if cpu_percent > 70 else "success")
    section.add_text(f"CPU:     {cpu_percent}%")
    section.add(cpu_bar)
    section.add_spacing()

    mem_used = 12.4
    mem_total = 16.0
    mem_percent = (mem_used / mem_total) * 100
    mem_severity = cast(
        Literal["success", "warning", "error"],
        "error" if mem_percent > 90 else "warning" if mem_percent > 75 else "success",
    )
    mem_bar = Bar.fraction(mem_used, mem_total, severity=mem_severity)
    section.add_text(f"Memory:  {mem_used:.1f}GB / {mem_total:.1f}GB")
    section.add(mem_bar)
    section.add_spacing()

    disk_used = 450
    disk_total = 500
    disk_percent = (disk_used / disk_total) * 100
    disk_severity = cast(
        Literal["success", "warning", "error"],
        "error" if disk_percent > 90 else "warning" if disk_percent > 80 else "success",
    )
    disk_bar = Bar.fraction(disk_used, disk_total, severity=disk_severity)
    section.add_text(f"Disk:    {disk_used}GB / {disk_total}GB")
    section.add(disk_bar)
    section.add_spacing()

    net_used = 850
    net_limit = 1000
    net_bar = Bar.fraction(net_used, net_limit, severity="info")
    section.add_text(f"Network: {net_used}Mbps / {net_limit}Mbps")
    section.add(net_bar)

time.sleep(1)

console.print("\n")
console.print(Divider("API Rate Limits"))
console.print("\n[bold]Track API quotas and limits:[/bold]\n")

apis = [
    {"name": "GitHub API", "used": 4500, "limit": 5000, "resets": "1h"},
    {"name": "Twitter API", "used": 850, "limit": 1000, "resets": "15m"},
    {"name": "Stripe API", "used": 650, "limit": 1000, "resets": "30m"},
    {"name": "OpenAI API", "used": 9800, "limit": 10000, "resets": "1m"},
]

with Section("API Rate Limits", subtitle="Usage Status") as section:
    for api in apis:
        used = cast(int, api["used"])
        limit = cast(int, api["limit"])
        usage_percent = (used / limit) * 100
        severity = cast(
            Literal["success", "warning", "error"],
            "error" if usage_percent > 95 else "warning" if usage_percent > 85 else "success",
        )

        bar = Bar.fraction(used, limit, severity=severity, width=30)
        section.add_text(
            f"{api['name']:<15} {api['used']:>5}/{api['limit']} (resets in {api['resets']})"
        )
        section.add(bar)
        if api != apis[-1]:
            section.add_spacing()

time.sleep(1)

console.print("\n")
console.print(Divider("Task Progress"))
console.print("\n[bold]Track task completion:[/bold]\n")

tasks = [
    {"task": "Build", "progress": 100, "status": "success"},
    {"task": "Test", "progress": 75, "status": "warning"},
    {"task": "Deploy", "progress": 30, "status": "info"},
    {"task": "Verify", "progress": 0, "status": "info"},
]

with Section("Deployment Pipeline", subtitle="Stage Progress") as section:
    for task in tasks:
        progress = cast(int, task["progress"])
        status_str = cast(str, task["status"])
        task_severity = cast(
            Literal["success", "warning", "error", "info"],
            status_str,
        )
        bar = Bar.percentage(
            progress,
            severity=task_severity,
            width=35,
        )
        status_symbol = "✓" if progress == 100 else "◐" if progress > 0 else "○"
        section.add_text(f"{status_symbol} {task['task']:<10} {task['progress']}%")
        section.add(bar)
        if task != tasks[-1]:  # Add spacing between items except after last one
            section.add_spacing()

time.sleep(1)

console.print("\n")
console.print(Divider("Custom Styling"))
console.print("\n[bold]Bars with custom colors:[/bold]\n")

console.print("Cyan bar:         ", end="")
console.print(Bar.percentage(65, width=40, complete_style="cyan"))

console.print("Bright magenta:   ", end="")
console.print(Bar.percentage(65, width=40, complete_style="bright_magenta"))

console.print("Green on white:   ", end="")
console.print(Bar.percentage(65, width=40, complete_style="green", style="white"))

time.sleep(1)

console.print("\n")
console.print(Divider("Summary"))
console.print()

console.print(
    Alert.success(
        "Bar Component Features",
        details="Percentage, fraction, ratio displays • Severity coloring • Custom widths",
    )
)

stats = {
    "Total Styles": "6 (percentage, fraction, ratio, indeterminate, custom)",
    "Severities": "4 (success, warning, error, info)",
    "Width Range": "1-console width characters",
    "Use Cases": "Metrics, quotas, progress, ratings",
}

console.print()
with Section("Bar Component Stats") as section:
    kv = KeyValue(stats)
    section.add(kv)

console.print(
    "\n[dim]Try combining Bar with Section, KeyValue, and Alert for rich dashboards![/dim]\n"
)
