import time

from chalkbox import Alert, Divider, Section, StatusCard, get_console

console = get_console()

console.print("\n[bold cyan]StatusCard Component Demo[/bold cyan]\n")

# ═══════════════════════════════════════════════════════════════════════════════
# Basic Status Cards
# ═══════════════════════════════════════════════════════════════════════════════

console.print(Divider("Basic Status Cards"))
console.print("\n[bold]Simple status cards with different status levels:[/bold]\n")

# Healthy service
card_healthy = StatusCard(
    title="Database Service",
    status="healthy",
    subtitle="PostgreSQL 15.2",
    metrics={"Uptime": "24d 5h 32m", "Connections": "42/100", "Response Time": "12ms"},
)
console.print(card_healthy)
console.print()

# Warning service
card_warning = StatusCard(
    title="Cache Service",
    status="warning",
    subtitle="Redis 7.0",
    metrics={"Uptime": "12d 8h", "Memory Usage": "78%", "Hit Rate": "89%"},
)
console.print(card_warning)
console.print()

# Error service
card_error = StatusCard(
    title="Queue Service",
    status="error",
    subtitle="RabbitMQ 3.11",
    metrics={"Uptime": "2h 15m", "Messages": "12,453 pending", "Consumers": "0"},
)
console.print(card_error)
console.print()

# Unknown service
card_unknown = StatusCard(
    title="External API",
    status="unknown",
    subtitle="Monitoring Unavailable",
    metrics={"Last Check": "3h ago", "Status": "Unknown"},
)
console.print(card_unknown)

time.sleep(1)

# ═══════════════════════════════════════════════════════════════════════════════
# Status Cards with Bars (Explicit Severity!)
# ═══════════════════════════════════════════════════════════════════════════════

console.print("\n")
console.print(Divider("Status Cards with Bars (Explicit Severity)"))
console.print("\n[bold]Display metrics with explicit severity levels (4-tuple format):[/bold]\n")

card_with_bars = StatusCard(
    title="API Gateway",
    status="warning",
    subtitle="gateway-prod-01 • us-east-1a",
    metrics={"Uptime": "15d 3h", "Requests/sec": "1,234", "Error Rate": "0.8%"},
    bars=[
        ("Throughput", 85.0, 100.0, "warning"),
        ("Response Time", 145.0, 200.0, "success"),
        ("Error Rate", 0.8, 1.0, "warning"),
    ],
)
console.print(card_with_bars)

time.sleep(1)

# ═══════════════════════════════════════════════════════════════════════════════
# Status Cards with Alerts
# ═══════════════════════════════════════════════════════════════════════════════

console.print("\n")
console.print(Divider("Status Cards with Contextual Alerts"))
console.print("\n[bold]Combine with Alert component for additional context:[/bold]\n")

card_with_alert = StatusCard(
    title="API Gateway",
    status="warning",
    subtitle="gateway-prod-02",
    metrics={"Requests/sec": "5,234", "Rate Limit": "4,500/5,000", "Latency": "145ms"},
    bars=[("Rate Limit Usage", 4500.0, 5000.0)],
    alert=Alert.warning(
        "Rate limit approaching", details="You have used 90% of your hourly quota (resets in 8m)"
    ),
)
console.print(card_with_alert)
console.print()

card_error_with_alert = StatusCard(
    title="Email Service",
    status="error",
    subtitle="smtp-server-03",
    metrics={"Queue Size": "2,453", "Failed": "1,823", "Success Rate": "25%"},
    alert=Alert.error(
        "SMTP connection failed",
        details="Unable to connect to mail.example.com:587 (connection refused)",
    ),
)
console.print(card_error_with_alert)

time.sleep(1)

# ═══════════════════════════════════════════════════════════════════════════════
# Using from_health_check Factory
# ═══════════════════════════════════════════════════════════════════════════════

console.print("\n")
console.print(Divider("from_health_check Factory Method"))
console.print("\n[bold]Create StatusCards from health check data:[/bold]\n")

health_data = {
    "status": "healthy",
    "version": "3.2.1",
    "uptime": "42d 17h 23m",
    "active_connections": "156/500",
    "requests_per_second": "2,345",
    "average_response_time": "23ms",
    "error_rate": "0.01%",
}

card_from_health = StatusCard.from_health_check("Web Server", health_data, subtitle="nginx/1.24")
console.print(card_from_health)

time.sleep(1)

# ═══════════════════════════════════════════════════════════════════════════════
# Bars with Auto-Calculated Severity (bar_thresholds)
# ═══════════════════════════════════════════════════════════════════════════════

console.print("\n")
console.print(Divider("Bars with Auto-Calculated Severity"))
console.print(
    "\n[bold]Let StatusCard calculate severity based on your thresholds (3-tuple format):[/bold]\n"
)

# Define thresholds: (warning_percent, error_percent)
thresholds = {
    "CPU": (70.0, 90.0),
    "Memory": (80.0, 95.0),
    "Disk": (75.0, 90.0),
}

# Healthy system (all metrics below warning threshold)
card_auto_healthy = StatusCard(
    title="Server A",
    status="healthy",
    subtitle="192.168.1.10",
    metrics={"Uptime": "30d 12h", "Load": "1.2"},
    bars=[
        ("CPU", 45.0, 100.0),
        ("Memory", 8.2, 16.0),
        ("Disk", 320.0, 500.0),
    ],
    bar_thresholds=thresholds,
)
console.print(card_auto_healthy)
console.print()

# Warning system (one metric above warning threshold)
card_auto_warning = StatusCard(
    title="Server B",
    status="warning",
    subtitle="192.168.1.11",
    metrics={"Uptime": "8d 4h", "Load": "3.8"},
    bars=[
        ("CPU", 78.0, 100.0),  # 78% > 70% warning
        ("Memory", 14.5, 16.0),  # 90.6% > 80% warning
        ("Disk", 420.0, 500.0),  # 84% > 75% warning
    ],
    bar_thresholds=thresholds,
)
console.print(card_auto_warning)
console.print()

# Error system (one metric above error threshold)
card_auto_error = StatusCard(
    title="Server C",
    status="error",
    subtitle="192.168.1.12",
    metrics={"Uptime": "2d 1h", "Load": "8.2"},
    bars=[
        ("CPU", 96.0, 100.0),  # 96% > 90% error
        ("Memory", 15.2, 16.0),  # 95% >= 95% error
        ("Disk", 485.0, 500.0),  # 97% > 90% error
    ],
    bar_thresholds=thresholds,
)
console.print(card_auto_error)

time.sleep(1)

# ═══════════════════════════════════════════════════════════════════════════════
# Mixed Bar Formats
# ═══════════════════════════════════════════════════════════════════════════════

console.print("\n")
console.print(Divider("Mixed Bar Formats"))
console.print("\n[bold]Combine explicit severity (4-tuple) and auto-calculated (3-tuple):[/bold]\n")

# Custom thresholds for specific bars
custom_thresholds = {
    "GPU": (50.0, 80.0),  # Lower thresholds for GPU
    "Temperature": (70.0, 80.0),  # Stricter thresholds for temp
}

card_mixed = StatusCard(
    title="ML Training Server",
    status="warning",
    subtitle="GPU Node 01",
    metrics={"Model": "ResNet-50", "Batch Size": "128", "Epoch": "42/100"},
    bars=[
        ("GPU", 65.0, 100.0),  # 3-tuple: auto-calc using thresholds (65% > 50% warning)
        ("VRAM", 7.2, 10.0, "success"),  # 4-tuple: explicit severity
        ("Temperature", 75.0, 85.0),  # 3-tuple: auto-calc (88% > 80% error)
    ],
    bar_thresholds=custom_thresholds,
)
console.print(card_mixed)

time.sleep(1)

# ═══════════════════════════════════════════════════════════════════════════════
# Multi-Service Dashboard
# ═══════════════════════════════════════════════════════════════════════════════

console.print("\n")
console.print(Divider("Multi-Service Dashboard"))
console.print("\n[bold]Combine multiple StatusCards for a service dashboard:[/bold]\n")

with Section("Infrastructure Status", subtitle="Production Environment") as section:
    # Database
    db_card = StatusCard(
        title="Primary Database",
        status="healthy",
        metrics={"Connections": "87/200", "QPS": "1,234", "Replication": "0s lag"},
        bars=[("Connections", 87.0, 200.0)],
    )
    section.add(db_card)
    section.add_spacing()

    # Cache
    cache_card = StatusCard(
        title="Cache Layer",
        status="warning",
        metrics={"Memory": "12.8GB/16GB", "Hit Rate": "94%"},
        bars=[("Memory", 12.8, 16.0)],
        alert=Alert.warning("Memory usage high", details="Consider scaling cache instances"),
    )
    section.add(cache_card)
    section.add_spacing()

    # Queue
    queue_card = StatusCard(
        title="Message Queue",
        status="healthy",
        metrics={"Messages": "23 pending", "Consumers": "8 active"},
        bars=[("Queue Depth", 23.0, 1000.0)],
    )
    section.add(queue_card)

time.sleep(1)

# ═══════════════════════════════════════════════════════════════════════════════
# API Rate Limit Tracking
# ═══════════════════════════════════════════════════════════════════════════════

console.print("\n")
console.print(Divider("API Rate Limit Tracking"))
console.print("\n[bold]Monitor API quotas and usage:[/bold]\n")

api_cards = [
    {
        "name": "GitHub API",
        "metrics": {"Used": "4,500/5,000", "Resets": "in 42m"},
        "bars": [("Usage", 4500.0, 5000.0)],
        "status": "warning",
    },
    {
        "name": "OpenAI API",
        "metrics": {"Used": "9,850/10,000", "Resets": "in 3m"},
        "bars": [("Usage", 9850.0, 10000.0)],
        "status": "error",
    },
    {
        "name": "Stripe API",
        "metrics": {"Used": "650/1,000", "Resets": "in 28m"},
        "bars": [("Usage", 650.0, 1000.0)],
        "status": "healthy",
    },
]

with Section("API Rate Limits", subtitle="Hourly Quotas") as section:
    for i, api in enumerate(api_cards):
        card = StatusCard(
            title=api["name"],
            status=api["status"],
            metrics=api["metrics"],
            bars=api["bars"],
        )
        section.add(card)
        if i < len(api_cards) - 1:
            section.add_spacing()

time.sleep(1)

# ═══════════════════════════════════════════════════════════════════════════════
# Summary
# ═══════════════════════════════════════════════════════════════════════════════

console.print("\n")
console.print(Divider("Summary"))
console.print()

console.print(
    Alert.success(
        "StatusCard Component Features",
        details=(
            "Composite design • Explicit severity (4-tuple) • Auto-calculated severity (3-tuple) • "
            "Factory method (from_health_check) • Metrics + Bars + Alerts"
        ),
    )
)

console.print(
    "\n[dim]StatusCard is a generic composition component - you control all severity and styling. "
    "Perfect for dashboards, monitoring tools, and health checks![/dim]\n"
)
