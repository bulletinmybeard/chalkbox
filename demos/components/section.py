from chalkbox import Alert, KeyValue, Section, Table, get_console


def demo_basic_usage():
    """Basic usage examples."""
    console = get_console()
    console.print("\n[bold cyan]═══ Basic Section Usage ═══[/bold cyan]\n")

    # Simple section with text
    with Section("Configuration") as section:
        section.add_text("host: localhost")
        section.add_text("port: 5432")
        section.add_text("database: myapp")

    # Section with subtitle
    with Section("Build Results", subtitle="Generated at 2024-01-15 14:30") as section:
        section.add_text("✓ Build successful")
        section.add_text("✓ All tests passed")
        section.add_text("Duration: 45.3 seconds")


def demo_advanced_features():
    """Advanced features and options."""
    console = get_console()
    console.print("\n[bold cyan]═══ Advanced Features ═══[/bold cyan]\n")

    # Section with mixed content
    with Section("Application Status") as section:
        section.add(Alert.success("All services operational"))
        section.add_spacing()

        table = Table(headers=["Service", "Status", "Uptime"])
        table.add_row("API", "Running", "14d 3h")
        table.add_row("Database", "Running", "14d 3h")
        table.add_row("Cache", "Running", "14d 3h")
        section.add(table)

        section.add_spacing()
        section.add(Alert.info("Last health check: 30 seconds ago"))

    # Section with footer
    with Section("Deployment Summary", footer="Completed at 2024-01-15 14:30:00") as section:
        section.add_text("Environment: production")
        section.add_text("Version: 2.0.1")
        section.add_text("Status: Success")

    # Collapsible section (static demo)
    console.print("\n[dim]Collapsible section:[/dim]")
    collapsed = Section.create_collapsible(
        "Advanced Settings",
        Alert.info("Advanced configuration options would appear here"),
        collapsed=False,
    )
    console.print(collapsed)


def demo_styling():
    """Styling and theming options."""
    console = get_console()
    console.print("\n[bold cyan]═══ Styling Options ═══[/bold cyan]\n")

    # Custom border style
    with Section("Success Section", border_style="bold green") as section:
        section.add_text("✓ Operation completed successfully")
        section.add_text("✓ No errors detected")

    # Warning section
    with Section("Warning Section", border_style="bold yellow") as section:
        section.add_text("⚠ Some issues require attention")
        section.add_text("⚠ Review the logs for details")

    # Error section
    with Section("Error Section", border_style="bold red") as section:
        section.add_text("✖ Operation failed")
        section.add_text("✖ Check configuration and try again")

    # Expanded section
    with Section("Full Width Section", expand=True) as section:
        section.add_text("This section expands to full terminal width")

    console.print("\n[dim]Title alignment options:[/dim]")

    # Centered title for emphasis
    with Section("Welcome Message", title_align="center") as section:
        section.add_text("Thank you for using ChalkBox!", style="bold cyan")
        section.add_text("Centered titles are great for headers and welcome screens")

    # Right-aligned title
    with Section("Build Metadata", title_align="right") as section:
        section.add_text("Version: 1.0.0")
        section.add_text("Built: 2025-01-15")
        section.add_text("Right-aligned titles work well for metadata")

    # Custom title and subtitle alignment
    with Section(
        "Status Report",
        footer="Generated: 2025-01-15 14:30:00",
        title_align="center",
        subtitle_align="center",
    ) as section:
        section.add_text("All systems operational", style="bold green")
        section.add_text("Centered title and footer for balanced appearance")

    # Custom padding - more spacious section
    with Section("Important Notice", padding=(2, 3)) as section:
        section.add_text("This section has extra padding for emphasis", style="bold")
        section.add_text("Use larger padding for important messages")


def demo_use_cases():
    """Common use cases for sections."""
    console = get_console()
    console.print("\n[bold cyan]═══ Use Cases ═══[/bold cyan]\n")

    # Configuration summary
    with Section("Configuration Summary") as section:
        config = {
            "Environment": "production",
            "Debug": False,
            "Workers": 4,
            "Port": 8000,
        }
        section.add(KeyValue(config))

    # Test results
    with Section(
        "Test Results", subtitle="Suite: unit tests", footer="Duration: 12.3 seconds"
    ) as section:
        section.add(Alert.success("150 tests passed"))
        section.add_spacing()

        failures_table = Table(headers=["Test", "Error"])
        failures_table.add_row("test_auth", "AssertionError")
        failures_table.add_row("test_db", "ConnectionError")
        section.add(failures_table)

    # Deployment steps
    with Section("Deployment Pipeline") as section:
        section.add_text("1. ✓ Build application")
        section.add_text("2. ✓ Run tests")
        section.add_text("3. ✓ Build Docker image")
        section.add_text("4. ✓ Push to registry")
        section.add_text("5. ⏳ Deploy to production")

    # System information
    with Section("System Information", subtitle="Collected at startup") as section:
        system_info = {
            "OS": "Linux 5.15.0",
            "Python": "3.12.0",
            "CPU": "Intel i7-9700K @ 3.60GHz",
            "Memory": "16.0 GB",
            "Disk": "512 GB SSD",
        }
        section.add(KeyValue(system_info))


def main():
    """Run all Section demos."""
    console = get_console()

    console.print(
        "\n[bold magenta]╔════════════════════════════════════════════════╗[/bold magenta]"
    )
    console.print("[bold magenta]║   ChalkBox - Section Component Demo           ║[/bold magenta]")
    console.print("[bold magenta]╚════════════════════════════════════════════════╝[/bold magenta]")

    demo_basic_usage()
    demo_advanced_features()
    demo_styling()
    demo_use_cases()

    console.print("\n[bold green]✓  Section demo completed![/bold green]")
    console.print(
        "\n[dim]Section is perfect for: grouping related content, summaries, reports, and structured output[/dim]"
    )
    console.print(
        "[dim]Customizable title/subtitle alignment and padding for better visual hierarchy[/dim]\n"
    )


if __name__ == "__main__":
    main()
