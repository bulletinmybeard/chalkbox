from rich.panel import Panel

from chalkbox import Alert, Divider, get_console


def demo_basic_alerts():
    """Basic alert types."""
    console = get_console()
    console.print()
    console.print(Divider(title="Basic Alert Types (6 Levels)", style="bold cyan"))
    console.print()

    console.print(Alert.debug("Verbose mode enabled for debugging"))
    console.print(Alert.info("This is an informational message"))
    console.print(Alert.success("Operation completed successfully!"))
    console.print(Alert.warning("Warning: Resource usage is high"))
    console.print(Alert.error("Error: Connection failed"))
    console.print(Alert.critical("Critical: System shutdown imminent"))


def demo_alerts_with_details():
    """Alerts with additional details."""
    console = get_console()
    console.print()
    console.print(Divider(title="Alerts with Details", style="bold cyan"))
    console.print()

    console.print(
        Alert.debug(
            "Request trace enabled",
            details="All HTTP requests will be logged with full headers and body",
        )
    )

    console.print(
        Alert.info(
            "System update available",
            details="Version 2.0.0 includes new features and bug fixes",
        )
    )

    console.print(
        Alert.success(
            "Backup completed",
            details="Backed up 1,234 files (2.5 GB) to remote storage",
        )
    )

    console.print(
        Alert.warning(
            "API rate limit approaching",
            details="You have used 950/1000 requests. Limit resets in 45 minutes.",
        )
    )

    console.print(
        Alert.error(
            "Database connection failed",
            details="Could not connect to postgres://localhost:5432. Check that the server is running.",
        )
    )

    console.print(
        Alert.critical(
            "System overload detected",
            details="CPU usage at 98%, memory at 95%. Automatic shutdown in 60 seconds.",
        )
    )


def demo_alert_use_cases():
    """Common use cases for alerts."""
    console = get_console()
    console.print()
    console.print(Divider(title="Common Use Cases", style="bold cyan"))
    console.print()

    # Configuration issues
    console.print(
        Alert.warning(
            "Configuration file not found",
            details="Using default settings. Create config.yaml to customize.",
        )
    )

    # Permission issues
    console.print(
        Alert.error(
            "Permission denied",
            details="You don't have write access to /var/log. Run with sudo or check permissions.",
        )
    )

    # Deprecation warnings
    console.print(
        Alert.warning(
            "Deprecated feature",
            details="The --old-flag option is deprecated. Use --new-flag instead.",
        )
    )

    # Successful operations
    console.print(
        Alert.success(
            "Deployment successful",
            details="Application deployed to production in 45 seconds",
        )
    )

    # Informational messages
    console.print(
        Alert.info(
            "Cache cleared",
            details="Removed 234 MB of cached data",
        )
    )


def demo_custom_styling():
    """Custom styling options for alerts."""
    console = get_console()
    console.print()
    console.print(Divider(title="Custom Styling Options", style="bold cyan"))
    console.print()

    # Title alignment
    console.print(
        Alert.success(
            "Welcome to ChalkBox!",
            title="Getting Started",
            title_align="center",
        )
    )

    console.print(
        Alert.debug(
            "Request ID: abc-123-xyz",
            title="Debug Info",
            title_align="right",
        )
    )

    # Custom padding
    console.print(
        Alert.info(
            "Compact alert with no padding",
            padding=0,
        )
    )

    console.print(
        Alert.warning(
            "Alert with extra vertical spacing",
            padding=(2, 1),  # (vertical, horizontal)
        )
    )

    console.print(
        Alert.error(
            "Alert with custom padding on all sides",
            padding=(1, 3),  # More horizontal space
            details="This alert has extra horizontal padding for emphasis",
        )
    )

    # Custom border style
    console.print(
        Alert.warning(
            "Deprecated API endpoint",
            border_style="yellow dim",
        )
    )


def demo_multiline_details():
    """Alerts with multi-line details."""
    console = get_console()
    console.print()
    console.print(Divider(title="Multi-line Details", style="bold cyan"))
    console.print()

    console.print(
        Alert.error(
            "Multiple errors detected",
            details="""Found 3 critical issues:
  • Database connection timeout
  • Redis server not responding
  • API endpoint returning 500 errors

Please check system logs for more information.""",
        )
    )

    console.print(
        Alert.info(
            "Installation complete",
            details="""Installed the following packages:
  • requests (2.31.0)
  • click (8.1.7)
  • rich (13.7.0)

Total installation time: 12.3 seconds""",
        )
    )


def demo_alerts_in_workflow():
    """Alerts used in a typical CLI workflow."""
    console = get_console()
    console.print()
    console.print(Divider(title="Workflow Example", style="bold cyan"))
    console.print()

    console.print("[bold]Starting deployment process...[/bold]\n")

    console.print(Alert.info("Validating configuration files"))
    console.print(Alert.success("Configuration validated successfully"))

    console.print(
        Alert.warning(
            "Outdated dependencies detected",
            details="Consider running 'npm update' before deploying",
        )
    )

    console.print(Alert.info("Building application"))
    console.print(Alert.success("Build completed in 23.4s"))

    console.print(Alert.info("Running tests"))
    console.print(
        Alert.error(
            "Test suite failed",
            details="3 tests failed in the authentication module. See test-results.xml for details.",
        )
    )

    console.print(
        Alert.warning(
            "Deployment aborted",
            details="Fix test failures before deploying to production",
        )
    )


def main():
    """Run all alert demos."""
    console = get_console()

    console.print()
    console.print(
        Panel(
            "[bold]ChalkBox - Alert Component Demo[/bold]",
            style="magenta",
            expand=False,
        )
    )

    demo_basic_alerts()
    demo_alerts_with_details()
    demo_custom_styling()
    demo_alert_use_cases()
    demo_multiline_details()
    demo_alerts_in_workflow()

    console.print("\n[bold green]✓  Alert demo completed![/bold green]")
    console.print(
        "\n[dim]Alerts now support 6 severity levels with customizable title alignment and padding[/dim]\n"
    )


if __name__ == "__main__":
    main()
