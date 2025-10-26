import time

from chalkbox import Alert, Align, Divider, KeyValue, Padding, Section, Table, get_console

console = get_console()

console.print("\n[bold cyan]Padding Component Demo[/bold cyan]\n")

# 1. Basic padding levels
console.print(Divider("Theme-Based Padding Levels"))
console.print("\n[bold]Use theme spacing tokens for consistency:[/bold]\n")

alert = Alert.info("Sample message")

console.print("[dim]No padding:[/dim]")
console.print(Padding.none(alert))
console.print()

time.sleep(0.5)

console.print("[dim]Extra small (xs):[/dim]")
console.print(Padding.xs(alert))
console.print()

time.sleep(0.5)

console.print("[dim]Small (sm):[/dim]")
console.print(Padding.small(alert))
console.print()

time.sleep(0.5)

console.print("[dim]Medium (md - 2 lines):[/dim]")
console.print(Padding.medium(alert))
console.print()

time.sleep(0.5)

console.print("[dim]Large (lg - 3 lines):[/dim]")
console.print(Padding.large(alert))
console.print()

time.sleep(0.5)

console.print("[dim]Extra large (xl - 4 lines):[/dim]")
console.print(Padding.xl(alert))
console.print()

time.sleep(1)

# 2. Symmetric padding
console.print(Divider("Symmetric Padding"))
console.print("\n[bold]Different vertical and horizontal spacing:[/bold]\n")

table = Table(headers=["Item", "Status"])
table.add_row("API", "Running", severity="success")
table.add_row("DB", "Connected", severity="success")

console.print("[dim]Symmetric (1 vertical, 4 horizontal):[/dim]")
console.print(Padding.symmetric(table, vertical=1, horizontal=4))
console.print()

time.sleep(0.5)

console.print("[dim]Symmetric (2 vertical, 8 horizontal):[/dim]")
console.print(Padding.symmetric(table, vertical=2, horizontal=8))
console.print()

time.sleep(1)

# 3. Vertical padding only
console.print(Divider("Vertical Padding"))
console.print("\n[bold]Add spacing above and below:[/bold]\n")

section = Section("Server Info")
section.add_text("Uptime: 99.9%")
section.add_text("Region: US-East")

console.print("[dim]No vertical padding:[/dim]")
console.print(section)
console.print()

time.sleep(0.5)

console.print("[dim]Vertical padding (2 lines):[/dim]")
console.print(Padding.vertical(section, amount=2))
console.print()

time.sleep(1)

# 4. Horizontal padding only
console.print(Divider("Horizontal Padding"))
console.print("\n[bold]Add spacing on left and right:[/bold]\n")

alert_msg = Alert.success("Deployment complete")

console.print("[dim]No horizontal padding:[/dim]")
console.print(alert_msg)
console.print()

time.sleep(0.5)

console.print("[dim]Horizontal padding (4 spaces):[/dim]")
console.print(Padding.horizontal(alert_msg, amount=4))
console.print()

time.sleep(0.5)

console.print("[dim]Horizontal padding (8 spaces):[/dim]")
console.print(Padding.horizontal(alert_msg, amount=8))
console.print()

time.sleep(1)

# 5. Custom padding (all sides)
console.print(Divider("Custom Padding"))
console.print("\n[bold]Specify each side individually:[/bold]\n")

kv = KeyValue({"Name": "MyApp", "Version": "1.0.0", "Status": "Running"})

console.print("[dim]Custom: top=1, right=8, bottom=2, left=4:[/dim]")
console.print(Padding.custom(kv, top=1, right=8, bottom=2, left=4))
console.print()

time.sleep(1)

# 6. Combining padding with alignment
console.print(Divider("Padding + Alignment"))
console.print("\n[bold]Combine for precise layout control:[/bold]\n")

centered_alert = Align.center(Alert.info("Centered with padding"))

console.print("[dim]Centered alert with large padding:[/dim]")
console.print(Padding.large(centered_alert))
console.print()

time.sleep(1)

# 7. Creating visual sections
console.print(Divider("Visual Separation"))
console.print("\n[bold]Use padding to create visual hierarchy:[/bold]\n")

# Header
header = Alert.success("System Status Report", details=None)
console.print(Padding.symmetric(Align.center(header), vertical=1, horizontal=0))

# Content with padding
content = Section("Metrics", subtitle="Current")
content.add_text("CPU: 45%")
content.add_text("Memory: 2.1GB")
content.add_text("Disk: 450GB")
console.print(Padding.medium(content))

# Footer
footer = KeyValue({"Generated": "2025-10-17 15:30", "Report ID": "RPT-001"})
console.print(Padding.symmetric(Align.right(footer), vertical=1, horizontal=0))

time.sleep(1)

# 8. Nested sections with padding
console.print("\n")
console.print(Divider("Nested Sections"))
console.print("\n[bold]Create depth with nested padding:[/bold]\n")

outer_section = Section("Deployment Pipeline", subtitle="Production")

stage1 = Alert.success("Build", details="Completed in 2m 34s")
outer_section.add(Padding.small(stage1))

stage2 = Alert.success("Test", details="All 156 tests passed")
outer_section.add(Padding.small(stage2))

stage3 = Alert.warning("Deploy", details="In progress (45%)")
outer_section.add(Padding.small(stage3))

console.print(Padding.medium(outer_section))

time.sleep(1)

# 9. Card-like layouts
console.print("\n")
console.print(Divider("Card Layouts"))
console.print("\n[bold]Create card-like containers:[/bold]\n")

# Card 1
card1_content = Section("Database Status")
card1_content.add_text("Connections: 42 active")
card1_content.add_text("Queries/sec: 1,234")
card1_content.add_text("Response: 12ms")
console.print(Padding.symmetric(card1_content, vertical=1, horizontal=2))

console.print()

# Card 2
card2_content = Section("Cache Status")
card2_content.add_text("Hit Rate: 94.2%")
card2_content.add_text("Size: 2.3GB")
card2_content.add_text("Evictions: 45/min")
console.print(Padding.symmetric(card2_content, vertical=1, horizontal=2))

console.print()

# Card 3
card3_content = Section("Queue Status")
card3_content.add_text("Pending: 1,234 jobs")
card3_content.add_text("Processing: 8 workers")
card3_content.add_text("Throughput: 500/min")
console.print(Padding.symmetric(card3_content, vertical=1, horizontal=2))

time.sleep(1)

# 10. Interactive menu with spacing
console.print("\n")
console.print(Divider("Interactive Menu"))
console.print("\n[bold]Well-spaced menu options:[/bold]\n")

menu_title = Alert.info("Main Menu", details="Select an option")
console.print(Padding.symmetric(Align.center(menu_title), vertical=1, horizontal=0))

menu_table = Table(headers=["Option", "Key", "Description"])
menu_table.add_row("Dashboard", "[D]", "View system dashboard", severity="info")
menu_table.add_row("Logs", "[L]", "View application logs", severity="info")
menu_table.add_row("Config", "[C]", "Edit configuration", severity="warning")
menu_table.add_row("Exit", "[Q]", "Quit application", severity="error")

console.print(Padding.symmetric(Align.center(menu_table), vertical=2, horizontal=4))

time.sleep(1)

# 11. Summary
console.print("\n")
console.print(Divider("Summary"))
console.print()

summary_alert = Alert.success(
    "Padding Component Features",
    details="Theme spacing • Symmetric & asymmetric • Vertical & horizontal",
)
console.print(Padding.medium(Align.center(summary_alert)))

stats = {
    "Theme Levels": "xs, sm, md, lg, xl (from theme.spacing)",
    "Patterns": "symmetric, vertical, horizontal, custom",
    "Use Cases": "Visual hierarchy, spacing, cards, layouts",
    "Composable": "Combines with Align, Section, all components",
}

with Section("Padding Component Stats") as stats_section:
    kv_stats = KeyValue(stats)
    stats_section.add(kv_stats)

console.print(Padding.medium(Align.center(stats_section)))

console.print(
    "\n[dim]Padding uses your theme's spacing tokens for consistent layouts![/dim]\n"
)
