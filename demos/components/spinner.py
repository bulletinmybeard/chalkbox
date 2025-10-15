import time

from chalkbox import Spinner, get_console


def demo_basic_usage():
    """Basic usage examples."""
    console = get_console()
    console.print("\n[bold cyan]═══ Basic Spinner Usage ═══[/bold cyan]\n")

    # Success spinner
    with Spinner("Loading data") as spinner:
        time.sleep(1.5)
        spinner.success("Data loaded successfully!")
    console.print("[green]✓[/green] Data loaded successfully!")

    time.sleep(0.5)

    # Error spinner
    with Spinner("Connecting to database") as spinner:
        time.sleep(1.5)
        spinner.error("Connection failed!")
    console.print("[red]✖[/red] Connection failed!")

    time.sleep(0.5)

    # Warning spinner
    with Spinner("Checking dependencies") as spinner:
        time.sleep(1.5)
        spinner.warning("Some dependencies are outdated")
    console.print("[yellow]⚠[/yellow] Some dependencies are outdated")


def demo_advanced_features():
    """Advanced features and options."""
    console = get_console()
    console.print("\n\n[bold cyan]═══ Advanced Features ═══[/bold cyan]\n")

    # Update message during operation
    with Spinner("Starting process") as spinner:
        time.sleep(0.8)
        spinner.update("Processing data")
        time.sleep(0.8)
        spinner.update("Finalizing")
        time.sleep(0.8)
        spinner.success("Process completed!")
    console.print("[green]✓[/green] Process completed!")

    time.sleep(0.5)

    # Different spinner styles
    console.print("\n[dim]Different spinner styles:[/dim]")
    with Spinner("Loading with dots", spinner="dots") as spinner:
        time.sleep(1)
        spinner.success()
    console.print("[green]✓[/green] Loading with dots")

    with Spinner("Loading with line", spinner="line") as spinner:
        time.sleep(1)
        spinner.success()
    console.print("[green]✓[/green] Loading with line")

    with Spinner("Loading with arc", spinner="arc") as spinner:
        time.sleep(1)
        spinner.success()
    console.print("[green]✓[/green] Loading with arc")


def demo_styling():
    """Styling and theming options."""
    console = get_console()
    console.print("\n\n[bold cyan]═══ Styling Options ═══[/bold cyan]\n")

    # Transient spinner (disappears after completion)
    console.print("[dim]Transient spinner (default - disappears):[/dim]\n")
    with Spinner("Loading configuration", transient=True) as spinner:
        time.sleep(1.5)
        spinner.success("Configuration loaded")
    console.print("[green]✓[/green] Configuration loaded")
    console.print("[dim italic]  (spinner disappeared after completion)[/dim italic]\n")

    time.sleep(0.5)

    # Note about non-transient mode
    console.print("[dim]Non-transient mode:[/dim]")
    console.print(
        "[dim italic]Use transient=False to keep the final message on screen.[/dim italic]"
    )
    console.print(
        "[dim italic]Best for sequential operations where you want a visible log.[/dim italic]"
    )
    console.print(
        "[dim italic](See Sequential Operations section below for example)[/dim italic]\n"
    )

    time.sleep(0.5)

    # Performance tuning with refresh_per_second
    console.print("[dim]Performance tuning with refresh rate:[/dim]\n")

    # Slow refresh for remote/slow terminals
    console.print("[dim italic]Slow refresh (4 fps) - better for slow terminals:[/dim italic]")
    with Spinner("Processing (slow refresh)...", refresh_per_second=4) as spinner:
        time.sleep(2)
        spinner.success("Complete")
    console.print("[green]✓[/green] Processing complete (slow refresh)\n")

    time.sleep(0.3)

    # Default refresh
    console.print("[dim italic]Default refresh (10 fps) - balanced:[/dim italic]")
    with Spinner("Processing (default refresh)...", refresh_per_second=10) as spinner:
        time.sleep(2)
        spinner.success("Complete")
    console.print("[green]✓[/green] Processing complete (default refresh)\n")

    time.sleep(0.3)

    # Fast refresh for smooth animations
    console.print("[dim italic]Fast refresh (20 fps) - smooth on fast terminals:[/dim italic]")
    with Spinner("Processing (fast refresh)...", refresh_per_second=20) as spinner:
        time.sleep(2)
        spinner.success("Complete")
    console.print("[green]✓[/green] Processing complete (fast refresh)\n")

    console.print(
        "[dim italic]Tip: Lower values (4-6 fps) reduce CPU usage and work better on remote connections.[/dim italic]"
    )
    console.print(
        "[dim italic]Higher values (15-20 fps) provide smoother animations on fast local terminals.[/dim italic]"
    )


def demo_use_cases():
    """Common use cases for spinners."""
    console = get_console()
    console.print("\n\n[bold cyan]═══ Use Cases ═══[/bold cyan]\n")

    # API request simulation
    with Spinner("Fetching user data from API") as spinner:
        time.sleep(1.2)
        spinner.success("Retrieved 150 users")
    console.print("  → 150 users retrieved from API\n")

    time.sleep(0.3)

    # File processing
    with Spinner("Processing images") as spinner:
        time.sleep(1.0)
        spinner.update("Resizing images")
        time.sleep(1.0)
        spinner.success("Processed 45 images")
    console.print("  → 45 images resized and optimized\n")

    time.sleep(0.3)

    # Installation workflow
    console.print("[dim]Multi-step installation workflow:[/dim]\n")
    with Spinner("Downloading dependencies") as spinner:
        time.sleep(1.0)
        spinner.success("Downloaded")
    console.print("  → Dependencies downloaded successfully")

    with Spinner("Installing packages") as spinner:
        time.sleep(1.2)
        spinner.success("Installed 23 packages")
    console.print("  → 23 packages installed")

    with Spinner("Configuring environment") as spinner:
        time.sleep(0.8)
        spinner.success("Configuration complete")
    console.print("  → Environment configured\n")

    time.sleep(0.3)

    # Error handling
    with Spinner("Deploying application") as spinner:
        time.sleep(1.0)
        spinner.update("Checking prerequisites")
        time.sleep(0.8)
        spinner.error("Deployment failed: missing credentials")
    console.print("  → Check credentials and try again\n")


def demo_sequential_operations():
    """Demonstrate sequential operations with spinners."""
    console = get_console()
    console.print("\n\n[bold cyan]═══ Sequential Operations ═══[/bold cyan]\n")

    operations = [
        ("Validating configuration", 0.8, "success", "Configuration valid"),
        ("Connecting to server", 1.0, "success", "Connected"),
        ("Authenticating", 0.9, "success", "Authenticated"),
        ("Uploading data", 1.2, "warning", "Upload completed with warnings"),
        ("Verifying upload", 0.7, "success", "Verification passed"),
    ]

    for text, duration, result_type, result_text in operations:
        with Spinner(text) as spinner:
            time.sleep(duration)

            if result_type == "success":
                spinner.success(result_text)
                style = "green"
                glyph = "✓"
            elif result_type == "error":
                spinner.error(result_text)
                style = "red"
                glyph = "✖"
            elif result_type == "warning":
                spinner.warning(result_text)
                style = "yellow"
                glyph = "⚠"

        console.print(f"[{style}]{glyph}[/{style}] {result_text}")
        time.sleep(0.2)


def main():
    """Run all Spinner demos."""
    console = get_console()

    console.print(
        "\n[bold magenta]╔════════════════════════════════════════════════╗[/bold magenta]"
    )
    console.print("[bold magenta]║   ChalkBox - Spinner Component Demo           ║[/bold magenta]")
    console.print("[bold magenta]╚════════════════════════════════════════════════╝[/bold magenta]")

    demo_basic_usage()
    demo_advanced_features()
    demo_styling()
    demo_use_cases()
    demo_sequential_operations()

    console.print("\n[bold green]✓  Spinner demo completed![/bold green]")
    console.print(
        "\n[dim]Spinner is perfect for: async operations, loading states, API calls, and file processing[/dim]"
    )
    console.print(
        "[dim]Configurable refresh rate for performance tuning on different terminals[/dim]\n"
    )


if __name__ == "__main__":
    main()
