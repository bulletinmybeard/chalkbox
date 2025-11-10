import time

from rich.panel import Panel

from chalkbox import DynamicProgress, get_console


def demo_basic_auto_ordering():
    """Demonstrate basic auto-reordering on completion."""
    console = get_console()
    console.print("\n[bold cyan]Auto-Reordering Demo[/bold cyan]\n")

    console.print(
        "[dim]Tasks complete at different speeds and auto-sort by completion time:[/dim]\n"
    )

    with DynamicProgress() as progress:
        # Add 5 tasks with different completion times
        task1 = progress.add_task("Very slow task", total=100)
        task2 = progress.add_task("Fast task", total=100)
        task3 = progress.add_task("Medium task", total=100)
        task4 = progress.add_task("Very fast task", total=100)
        task5 = progress.add_task("Slow task", total=100)

        # Complete tasks with staggered timing
        # Very fast (1s)
        time.sleep(0.01)
        for _ in range(100):
            progress.update(task4, advance=1)
            time.sleep(0.01)

        # Fast (2s from start)
        for _ in range(100):
            progress.update(task2, advance=1)
            time.sleep(0.01)

        # Medium (4s from start)
        for _ in range(100):
            progress.update(task3, advance=1)
            time.sleep(0.02)

        # Slow (5s from start)
        for _ in range(100):
            progress.update(task5, advance=1)
            time.sleep(0.01)

        # Very slow (6s from start)
        for _ in range(100):
            progress.update(task1, advance=1)
            time.sleep(0.01)

    console.print(
        "\n[green]✓ Tasks completed and auto-sorted by completion time (fastest first)[/green]\n"
    )


def demo_millisecond_precision():
    """Demonstrate millisecond precision for tasks finishing in same second."""
    console = get_console()
    console.print("\n[bold cyan]Millisecond Precision Demo[/bold cyan]\n")

    console.print(
        "[dim]Multiple tasks finishing within same second are ordered by milliseconds:[/dim]\n"
    )

    with DynamicProgress() as progress:
        # Add tasks that will finish very close together
        task1 = progress.add_task("Task 1", total=100)
        task2 = progress.add_task("Task 2", total=100)
        task3 = progress.add_task("Task 3", total=100)

        # Complete all within ~100ms but in specific order
        time.sleep(0.03)  # 30ms
        progress.update(task1, completed=100)

        time.sleep(0.02)  # 20ms more (total 50ms)
        progress.update(task2, completed=100)

        time.sleep(0.025)  # 25ms more (total 75ms)
        progress.update(task3, completed=100)

    console.print("\n[green]✓ Tasks ordered correctly using millisecond precision[/green]\n")


def demo_real_world_scraping():
    """Simulate real-world scraping scenario."""
    console = get_console()
    console.print("\n[bold cyan]Web Scraping Simulation[/bold cyan]\n")

    console.print("[dim]Scraping product pages with varying response times:[/dim]\n")

    products = [
        ("Amazon - Laptop", 0.8),
        ("eBay - Headphones", 0.5),
        ("Best Buy - Mouse", 1.2),
        ("Newegg - Keyboard", 0.6),
        ("Walmart - Monitor", 1.5),
    ]

    with DynamicProgress() as progress:
        tasks = {}

        for name, _ in products:
            task_id = progress.add_task(f"Scraping {name}", total=100)
            tasks[name] = task_id

        # Simulate scraping with different response times
        for name, duration in products:
            task_id = tasks[name]

            # Simulate network delay
            for _ in range(100):
                progress.update(task_id, advance=1)
                time.sleep(duration / 100)

    console.print("\n[green]✓ Scraping completed - fastest sites shown first[/green]\n")


def demo_update_description():
    """Demonstrate updating task descriptions."""
    console = get_console()
    console.print("\n[bold cyan]Dynamic Description Updates[/bold cyan]\n")

    console.print("[dim]Task descriptions update as work progresses:[/dim]\n")

    with DynamicProgress() as progress:
        task = progress.add_task("Processing batch", total=5)

        files = ["data1.json", "data2.json", "data3.json", "data4.json", "data5.json"]

        for filename in files:
            # Update description to show current file
            progress.update(task, description=f"Processing {filename}", advance=1)
            time.sleep(0.3)

    console.print("\n[green]✓ Batch processing completed[/green]\n")


def demo_use_case_comparison():
    """Compare standard Progress vs DynamicProgress."""
    console = get_console()
    console.print("\n[bold cyan]Standard vs Dynamic Progress[/bold cyan]\n")

    console.print("[dim]Standard Progress (no reordering):[/dim]")
    from chalkbox import Progress

    with Progress() as progress:
        task1 = progress.add_task("Slow", total=100)
        task2 = progress.add_task("Fast", total=100)

        # Complete fast task first
        for _ in range(100):
            progress.update(task2, advance=1)
            time.sleep(0.005)

        # Then slow task
        for _ in range(100):
            progress.update(task1, advance=1)
            time.sleep(0.005)

    console.print("[yellow]→ Tasks stay in insertion order (Slow, Fast)[/yellow]\n")

    time.sleep(1)

    console.print("[dim]Dynamic Progress (auto-reordering):[/dim]")

    with DynamicProgress() as progress:
        task1 = progress.add_task("Slow", total=100)
        task2 = progress.add_task("Fast", total=100)

        # Complete fast task first
        for _ in range(100):
            progress.update(task2, advance=1)
            time.sleep(0.005)

        # Then slow task
        for _ in range(100):
            progress.update(task1, advance=1)
            time.sleep(0.005)

    console.print("[green]→ Completed tasks sorted by speed (Fast, Slow)[/green]\n")


def main():
    """Run all DynamicProgress demos."""
    console = get_console()

    console.print()
    console.print(
        Panel(
            "[bold]ChalkBox - DynamicProgress Demo[/bold]",
            style="magenta",
            expand=False,
        )
    )

    demo_basic_auto_ordering()
    time.sleep(1)

    demo_millisecond_precision()
    time.sleep(1)

    demo_real_world_scraping()
    time.sleep(1)

    demo_update_description()
    time.sleep(1)

    demo_use_case_comparison()

    console.print("\n[bold green]✓  DynamicProgress demo completed![/bold green]")


if __name__ == "__main__":
    main()
