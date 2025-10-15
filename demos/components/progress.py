import time

from chalkbox import Progress, get_console


def demo_basic_usage():
    """Basic usage examples."""
    console = get_console()
    console.print("\n[bold cyan]═══ Basic Progress Usage ═══[/bold cyan]\n")

    # Single task progress
    console.print("[dim]Single task:[/dim]")
    with Progress() as progress:
        task = progress.add_task("Processing files", total=100)

        for _i in range(100):
            time.sleep(0.02)
            progress.update(task, advance=1)

    console.print("[green]✓ Task completed[/green]\n")


def demo_advanced_features():
    """Advanced features and options."""
    console = get_console()
    console.print("\n[bold cyan]═══ Advanced Features ═══[/bold cyan]\n")

    # Multiple concurrent tasks
    console.print("[dim]Multiple tasks:[/dim]")
    with Progress() as progress:
        # Add multiple tasks
        download_task = progress.add_task("Downloading data", total=50)
        process_task = progress.add_task("Processing data", total=75)
        upload_task = progress.add_task("Uploading results", total=30)

        # Simulate work
        for i in range(75):
            time.sleep(0.02)

            if i < 50:
                progress.update(download_task, advance=1)
            if i < 75:
                progress.update(process_task, advance=1)
            if i < 30:
                progress.update(upload_task, advance=1)

    console.print("[green]✓ All tasks completed[/green]\n")

    # Unknown total
    console.print("[dim]Indeterminate progress:[/dim]")
    with Progress() as progress:
        task = progress.add_task("Scanning files", total=None)

        for _ in range(50):
            time.sleep(0.02)
            progress.update(task, advance=1)

        # Set total once known
        progress.update(task, total=100)

        for _ in range(50):
            time.sleep(0.02)
            progress.update(task, advance=1)

    console.print("[green]✓ Scan completed[/green]\n")


def demo_styling():
    """Styling and theming options."""
    console = get_console()
    console.print("\n[bold cyan]═══ Styling Options ═══[/bold cyan]\n")

    # Transient progress (disappears after completion)
    console.print("[dim]Transient progress (disappears):[/dim]")
    with Progress(transient=True) as progress:
        task = progress.add_task("Loading...", total=50)

        for _i in range(50):
            time.sleep(0.02)
            progress.update(task, advance=1)

    console.print("[green]✓ Progress bar removed after completion[/green]\n")

    # Non-transient progress
    console.print("[dim]Non-transient progress (remains visible):[/dim]")
    with Progress(transient=False) as progress:
        task = progress.add_task("Building project", total=50)

        for _i in range(50):
            time.sleep(0.02)
            progress.update(task, advance=1)

    console.print("[green]✓ Progress bar remains visible[/green]\n")


def demo_use_cases():
    """Common use cases for progress bars."""
    console = get_console()
    console.print("\n[bold cyan]═══ Use Cases ═══[/bold cyan]\n")

    # File processing
    console.print("[dim]File processing:[/dim]")
    files = ["app.py", "config.yaml", "data.json", "utils.py", "tests.py"]

    with Progress() as progress:
        overall = progress.add_task("Processing files", total=len(files))

        for file in files:
            progress.update(overall, description=f"Processing {file}")
            time.sleep(0.3)
            progress.update(overall, advance=1)

    console.print("[green]✓ All files processed[/green]\n")

    # Installation/setup
    console.print("[dim]Installation steps:[/dim]")
    steps = [
        ("Downloading dependencies", 40),
        ("Installing packages", 30),
        ("Configuring application", 20),
        ("Running post-install scripts", 10),
    ]

    with Progress() as progress:
        for step_name, step_work in steps:
            task = progress.add_task(step_name, total=step_work)

            for _ in range(step_work):
                time.sleep(0.02)
                progress.update(task, advance=1)

    console.print("[green]✓ Installation completed[/green]\n")

    # Data transfer simulation
    console.print("[dim]Data transfer:[/dim]")
    with Progress() as progress:
        download = progress.add_task("Downloading data", total=100)

        for i in range(100):
            time.sleep(0.01)
            progress.update(download, advance=1, description=f"Downloading data [{i+1}/100 MB]")

    console.print("[green]✓ Download completed[/green]\n")


def demo_sequential_workflow():
    """Demonstrate a sequential workflow with progress tracking."""
    console = get_console()
    console.print("\n[bold cyan]═══ Sequential Workflow ═══[/bold cyan]\n")

    workflow_steps = [
        ("Validating input", 20),
        ("Connecting to database", 15),
        ("Fetching records", 40),
        ("Processing data", 50),
        ("Generating report", 30),
        ("Saving results", 25),
    ]

    with Progress() as progress:
        for step_name, duration in workflow_steps:
            task = progress.add_task(step_name, total=duration)

            for _ in range(duration):
                time.sleep(0.01)
                progress.update(task, advance=1)

    console.print("[green]✓ Workflow completed successfully[/green]")


def main():
    """Run all Progress demos."""
    console = get_console()

    console.print(
        "\n[bold magenta]╔════════════════════════════════════════════════╗[/bold magenta]"
    )
    console.print("[bold magenta]║   ChalkBox - Progress Component Demo          ║[/bold magenta]")
    console.print("[bold magenta]╚════════════════════════════════════════════════╝[/bold magenta]")

    demo_basic_usage()
    demo_advanced_features()
    demo_styling()
    demo_use_cases()
    demo_sequential_workflow()

    console.print("\n[bold green]✓  Progress demo completed![/bold green]")
    console.print(
        "\n[dim]Progress is perfect for: long-running tasks, file processing, downloads, and multi-step workflows[/dim]\n"
    )


if __name__ == "__main__":
    main()
