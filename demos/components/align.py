import time

from chalkbox import Align, Alert, Divider, KeyValue, Section, Table, get_console

console = get_console()

console.print("\n[bold cyan]Align Component Demo[/bold cyan]\n")

console.print(Divider("Horizontal Alignment"))
console.print("\n[bold]Align content left, center, or right:[/bold]\n")

alert = Alert.info("This is an alert message")

console.print("[dim]Left (default):[/dim]")
console.print(Align.left(alert))
console.print()

time.sleep(0.5)

console.print("[dim]Center:[/dim]")
console.print(Align.center(alert))
console.print()

time.sleep(0.5)

console.print("[dim]Right:[/dim]")
console.print(Align.right(alert))
console.print()

time.sleep(1)

console.print(Divider("Aligning Various Components"))
console.print("\n[bold]Align tables, sections, and alerts:[/bold]\n")

table = Table(headers=["Item", "Value"])
table.add_row("CPU", "45%", severity="success")
table.add_row("Memory", "78%", severity="warning")
table.add_row("Disk", "92%", severity="error")

console.print("[dim]Centered table:[/dim]")
console.print(Align.center(table))
console.print()

time.sleep(0.5)

section = Section("Server Status", subtitle="Production")
section.add_text("✓ API responding")
section.add_text("✓ Database connected")
section.add_text("⚠ High memory usage")

console.print("[dim]Right-aligned section:[/dim]")
console.print(Align.right(section))
console.print()

time.sleep(1)

console.print(Divider("Vertical Alignment"))
console.print("\n[bold]Align content vertically (requires height):[/bold]\n")

small_alert = Alert.success("Centered both ways!")

console.print("[dim]Top (default):[/dim]")
console.print(Align.top(small_alert, height=5))
console.print()

time.sleep(0.5)

console.print("[dim]Middle:[/dim]")
console.print(Align.middle(small_alert, height=5))
console.print()

time.sleep(0.5)

console.print("[dim]Bottom:[/dim]")
console.print(Align.bottom(small_alert, height=5))
console.print()

time.sleep(1)

console.print(Divider("Header/Content/Footer Pattern"))
console.print("\n[bold]Common layout pattern for CLI apps:[/bold]\n")

header = Alert.info("MyApp v1.0.0 - System Status", details=None)
console.print(Align.center(header))
console.print()

content = Section("Current Tasks", subtitle="In Progress")
content.add_text("• Processing data batch #1234")
content.add_text("• Running health checks")
content.add_text("• Syncing with remote")
console.print(content)
console.print()

footer_kv = KeyValue({"Last Update": "2025-10-17 15:30:00", "Status": "✓ Healthy"})
console.print(Align.right(footer_kv))
console.print()

time.sleep(1)

console.print(Divider("Centered Alerts for Emphasis"))
console.print("\n[bold]Center important messages:[/bold]\n")

console.print(Align.center(Alert.success("Deployment Successful")))
console.print()
time.sleep(0.5)

console.print(Align.center(Alert.warning("API Rate Limit: 90% Used")))
console.print()
time.sleep(0.5)

console.print(Align.center(Alert.error("Connection Failed")))
console.print()

time.sleep(1)

console.print(Divider("Menu Navigation Pattern"))
console.print("\n[bold]Create balanced menus:[/bold]\n")

menu = Table(headers=["Option", "Key"])
menu.add_row("View Dashboard", "[D]", severity="info")
menu.add_row("Run Tests", "[T]", severity="info")
menu.add_row("Deploy", "[P]", severity="success")
menu.add_row("Quit", "[Q]", severity="error")

console.print(Align.center(menu))
console.print()

time.sleep(1)

console.print(Divider("Advanced Composition"))
console.print("\n[bold]Combine alignment with sections:[/bold]\n")

with Section("Dashboard", subtitle="Centered Content") as dash_section:
    metrics_table = Table(headers=["Metric", "Value", "Status"])
    metrics_table.add_row("Uptime", "99.9%", "✓", severity="success")
    metrics_table.add_row("Response Time", "45ms", "✓", severity="success")
    metrics_table.add_row("Error Rate", "0.01%", "✓", severity="success")

    dash_section.add(Align.center(metrics_table))

time.sleep(1)

console.print("\n")
console.print(Divider("Width Control"))
console.print("\n[bold]Control alignment width:[/bold]\n")

alert_msg = Alert.info("Short message")

console.print("[dim]Default width (console):[/dim]")
console.print(Align.center(alert_msg))
console.print()

console.print("[dim]Fixed width (60 chars):[/dim]")
console.print(Align.center(alert_msg, width=60))
console.print()

console.print("[dim]Fixed width (40 chars):[/dim]")
console.print(Align.center(alert_msg, width=40))
console.print()

time.sleep(1)

console.print(Divider("Welcome Screen Example"))
console.print("\n[bold]Complete welcome screen layout:[/bold]\n")

title = Alert.success("DataSync Pro", details="Enterprise Data Synchronization Tool")
console.print(Align.center(title))
console.print()

info_section = Section("System Information")
info_section.add_text("Version: 2.1.0")
info_section.add_text("Environment: Production")
info_section.add_text("Region: US-East-1")
console.print(Align.center(info_section))
console.print()

options = Table(headers=["Action", "Command"])
options.add_row("Start Sync", "sync start", severity="success")
options.add_row("View Status", "sync status", severity="info")
options.add_row("View Logs", "sync logs", severity="info")
options.add_row("Configuration", "sync config", severity="warning")
console.print(Align.center(options))
console.print()

time.sleep(1)

console.print(Divider("Summary"))
console.print()

console.print(
    Align.center(
        Alert.success(
            "Align Component Features",
            details="Horizontal & vertical alignment • Width control • Perfect for layouts",
        )
    )
)

console.print()

stats = {
    "Horizontal": "left, center, right",
    "Vertical": "top, middle, bottom",
    "Use Cases": "Headers, footers, menus, emphasis",
    "Composable": "Works with all ChalkBox components",
}

with Section("Align Component Stats") as section:
    kv = KeyValue(stats)
    section.add(kv)

console.print(Align.center(section))

console.print(
    "\n[dim]Try combining Align with Padding for precise control over layout![/dim]\n"
)
