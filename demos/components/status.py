import time

from chalkbox import Status, get_console, status


def demo_basic_usage():
    """Basic usage examples."""
    console = get_console()
    console.print("\n[bold cyan]═══ Basic Status Usage ═══[/bold cyan]\n")

    # Simple status
    console.print("[dim]Simple status indicator:[/dim]")
    with status("Processing data..."):
        time.sleep(2)
    console.print("[green]✓ Processing complete[/green]\n")

    # Custom message
    console.print("[dim]Custom status message:[/dim]")
    with Status("Loading configuration files"):
        time.sleep(1.5)
    console.print("[green]✓ Configuration loaded[/green]")


def demo_advanced_features():
    """Advanced features and options."""
    console = get_console()
    console.print("\n\n[bold cyan]═══ Advanced Features ═══[/bold cyan]\n")

    # Updating status message
    console.print("[dim]Updating status message:[/dim]")
    with Status("Starting process") as st:
        time.sleep(1)
        st.update("Connecting to database")
        time.sleep(1)
        st.update("Fetching records")
        time.sleep(1)
        st.update("Processing results")
        time.sleep(1)
    console.print("[green]✓ Process completed[/green]\n")

    # Different spinner styles
    console.print("[dim]Different spinner:[/dim]")
    with Status("Loading", spinner="line"):
        time.sleep(1.5)
    console.print("[green]✓ Done[/green]\n")

    # Allowing console output during status
    console.print("[dim]Status with console output:[/dim]")
    with Status("Running long operation"):
        time.sleep(0.5)
        console.print("  [dim]Step 1 completed[/dim]")
        time.sleep(0.5)
        console.print("  [dim]Step 2 completed[/dim]")
        time.sleep(0.5)
        console.print("  [dim]Step 3 completed[/dim]")
        time.sleep(0.5)
    console.print("[green]✓ Operation completed[/green]")


def demo_styling():
    """Styling and theming options."""
    console = get_console()
    console.print("\n\n[bold cyan]═══ Styling Options ═══[/bold cyan]\n")

    # Custom spinner speed
    console.print("[dim]Fast spinner:[/dim]")
    with Status("Fast loading", speed=2.0):
        time.sleep(1.5)
    console.print("[green]✓ Done[/green]\n")

    # Slow spinner
    console.print("[dim]Slow spinner:[/dim]")
    with Status("Slow loading", speed=0.5):
        time.sleep(1.5)
    console.print("[green]✓ Done[/green]")


def demo_use_cases():
    """Common use cases for status displays."""
    console = get_console()
    console.print("\n\n[bold cyan]═══ Use Cases ═══[/bold cyan]\n")

    # File processing with progress updates
    console.print("[dim]File processing:[/dim]")
    files = ["app.py", "config.yaml", "data.json", "utils.py"]
    with Status("Processing files") as st:
        for i, file in enumerate(files, 1):
            st.update(f"Processing {file} ({i}/{len(files)})")
            time.sleep(0.5)
    console.print("[green]✓ All files processed[/green]\n")

    # API request with retries
    console.print("[dim]API request with retries:[/dim]")
    with Status("Fetching data from API") as st:
        for attempt in range(1, 4):
            st.update(f"Attempt {attempt}/3")
            time.sleep(0.8)
    console.print("[green]✓ Data fetched successfully[/green]\n")

    # Database migration
    console.print("[dim]Database migration:[/dim]")
    with Status("Running database migration") as st:
        st.update("Backing up database")
        time.sleep(0.7)
        st.update("Applying migration 001_create_users")
        time.sleep(0.9)
        st.update("Applying migration 002_add_roles")
        time.sleep(0.8)
        st.update("Verifying schema")
        time.sleep(0.6)
    console.print("[green]✓ Migration completed[/green]\n")

    # Installation workflow
    console.print("[dim]Installation:[/dim]")
    steps = [
        "Downloading packages",
        "Verifying checksums",
        "Extracting files",
        "Installing dependencies",
        "Configuring application",
        "Running post-install scripts",
    ]
    with Status("Installing application") as st:
        for step in steps:
            st.update(step)
            time.sleep(0.6)
    console.print("[green]✓ Installation successful[/green]")


def demo_comparison_with_spinner():
    """Show the difference between Status and Spinner."""
    console = get_console()
    console.print("\n\n[bold cyan]═══ Status vs Spinner ═══[/bold cyan]\n")

    console.print("[bold]Status allows console output during operation:[/bold]\n")

    with Status("Running tests"):
        time.sleep(0.3)
        console.print("  test_auth.py ... [green]PASSED[/green]")
        time.sleep(0.3)
        console.print("  test_database.py ... [green]PASSED[/green]")
        time.sleep(0.3)
        console.print("  test_api.py ... [green]PASSED[/green]")
        time.sleep(0.3)

    console.print(
        "\n[dim]Status is ideal when you need to show progress messages "
        "while still indicating the operation is ongoing.[/dim]"
    )


def main():
    """Run all Status demos."""
    console = get_console()

    console.print(
        "\n[bold magenta]╔════════════════════════════════════════════════╗[/bold magenta]"
    )
    console.print("[bold magenta]║   ChalkBox - Status Component Demo            ║[/bold magenta]")
    console.print("[bold magenta]╚════════════════════════════════════════════════╝[/bold magenta]")

    demo_basic_usage()
    demo_advanced_features()
    demo_styling()
    demo_use_cases()
    demo_comparison_with_spinner()

    console.print("\n[bold green]✓  Status demo completed![/bold green]")
    console.print(
        "\n[dim]Status is perfect for: long operations, file processing, API calls, and when you need console output during work[/dim]\n"
    )


if __name__ == "__main__":
    main()
