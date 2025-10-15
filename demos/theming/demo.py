from pathlib import Path
import sys

from chalkbox import Alert, KeyValue, Section, Table, get_console, set_theme
from chalkbox.core.theme import Theme


def show_components():
    """Display various components to showcase the theme."""
    console = get_console()

    # Header
    console.print("\n[bold]ChalkBox Theme Demo[/bold]\n")

    # Alerts showcase
    with Section("Alerts & Notifications", subtitle="Different severity levels") as section:
        section.add(Alert.info("System check in progress"))
        section.add(Alert.success("All tests passed successfully"))
        section.add(Alert.warning("High memory usage detected", details="Using 8.5GB of 10GB"))
        section.add(Alert.error("Connection failed", details="Could not reach database"))

    console.print()

    # Table showcase
    with Section("Service Status", subtitle="Production environment") as section:
        table = Table(headers=["Service", "Status", "Response Time", "Uptime"])
        table.add_row("Web API", "Running", "45ms", "99.9%", severity="success")
        table.add_row("Database", "Running", "12ms", "99.99%", severity="success")
        table.add_row("Cache", "Degraded", "230ms", "98.5%", severity="warning")
        table.add_row("Queue", "Down", "timeout", "85.2%", severity="error")
        section.add(table)

    console.print()

    # Configuration showcase
    with Section("Configuration", subtitle="Application settings") as section:
        config = KeyValue(title="Environment Variables")
        config.add("Environment", "production")
        config.add("Region", "us-east-1")
        config.add("Debug Mode", "false")
        config.add("API_KEY", "sk-1234567890abcdef")  # Automatically masked
        config.add("Max Workers", "4")
        section.add(config)


def main():
    """Run the theme demo with optional theme selection."""
    # Determine which theme to use
    theme_name = sys.argv[1] if len(sys.argv) > 1 else "default"

    if theme_name == "dark":
        # Load dark theme from file
        theme_path = Path(__file__).parent / "theme-dark.toml"
        if theme_path.exists():
            custom_theme = Theme.from_file(theme_path)
            set_theme(custom_theme)
            print(f"✓ Loaded dark theme from: {theme_path}\n")
        else:
            print(f"✖ Theme file not found: {theme_path}")
            sys.exit(1)

    elif theme_name == "light":
        # Load light theme from file
        theme_path = Path(__file__).parent / "theme-light.toml"
        if theme_path.exists():
            custom_theme = Theme.from_file(theme_path)
            set_theme(custom_theme)
            print(f"✓ Loaded light theme from: {theme_path}\n")
        else:
            print(f"✖ Theme file not found: {theme_path}")
            sys.exit(1)

    elif theme_name != "default":
        print(f"Unknown theme: {theme_name}")
        print("Usage: python demos/theming/demo.py [default|dark|light]")
        sys.exit(1)

    # Show components with the selected theme
    show_components()

    # Show theme info
    console = get_console()
    console.print(f"\n[dim]Theme: {theme_name}[/dim]")
    console.print("[dim]Try: poetry run python demos/theming/demo.py [default|dark|light][/dim]\n")


if __name__ == "__main__":
    main()
