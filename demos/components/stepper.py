import time

from chalkbox import Stepper, get_console


def demo_basic_usage():
    """Basic usage examples."""
    console = get_console()
    console.print("\n[bold cyan]═══ Basic Stepper Usage ═══[/bold cyan]\n")

    # Simple step list (static)
    console.print("[dim]Static step list:[/dim]")
    steps = ["Initialize project", "Install dependencies", "Configure settings"]
    stepper = Stepper.from_list(steps, title="Setup Process")

    # Mark steps as complete
    stepper.start(0)
    stepper.complete(0)
    stepper.start(1)
    stepper.complete(1)
    stepper.start(2)

    console.print(stepper)
    console.print()


def demo_advanced_features():
    """Advanced features and options."""
    console = get_console()
    console.print("\n[bold cyan]═══ Advanced Features ═══[/bold cyan]\n")

    # Live updating stepper
    console.print("[dim]Live stepper with real-time updates:[/dim]")
    steps = [
        "Download packages",
        "Verify signatures",
        "Extract files",
        "Install components",
        "Configure system",
    ]

    with Stepper.from_list(steps, title="Installation", live=True) as stepper:
        for i in range(len(steps)):
            stepper.start(i)
            time.sleep(0.8)
            stepper.complete(i)

    console.print()

    # Steps with failures
    console.print("[dim]Stepper with failures:[/dim]")
    steps = [
        "Validate input",
        "Connect to database",
        "Run migration",
        "Update schema",
        "Verify results",
    ]

    stepper = Stepper.from_list(steps, title="Database Migration")
    stepper.start(0)
    stepper.complete(0)
    stepper.start(1)
    stepper.complete(1)
    stepper.start(2)
    stepper.fail(2, "Migration script error: column already exists")
    stepper.skip(3)
    stepper.skip(4)

    console.print(stepper)


def demo_styling():
    """Styling and theming options."""
    console = get_console()
    console.print("\n\n[bold cyan]═══ Styling Options ═══[/bold cyan]\n")

    # Without numbers
    console.print("[dim]Without step numbers:[/dim]")
    steps = ["Build", "Test", "Deploy"]
    stepper = Stepper.from_list(steps, title="Pipeline", show_numbers=False)
    stepper.complete(0)
    stepper.complete(1)
    stepper.start(2)
    console.print(stepper)
    console.print()

    # With descriptions
    console.print("[dim]With descriptions:[/dim]")
    stepper_desc = Stepper(title="Deployment", show_description=True)
    stepper_desc.add_step("Build", "Compile source code and assets")
    stepper_desc.add_step("Test", "Run unit and integration tests")
    stepper_desc.add_step("Deploy", "Push to production environment")

    stepper_desc.complete(0)
    stepper_desc.complete(1)
    stepper_desc.start(2)

    console.print(stepper_desc)


def demo_use_cases():
    """Common use cases for steppers."""
    console = get_console()
    console.print("\n\n[bold cyan]═══ Use Cases ═══[/bold cyan]\n")

    # CI/CD Pipeline
    console.print("[dim]CI/CD Pipeline:[/dim]")
    pipeline_steps = [
        "Checkout code",
        "Install dependencies",
        "Run linters",
        "Run tests",
        "Build artifacts",
        "Deploy to staging",
        "Run smoke tests",
        "Deploy to production",
    ]

    with Stepper.from_list(pipeline_steps, title="CI/CD Pipeline", live=True) as stepper:
        for i in range(len(pipeline_steps)):
            stepper.start(i)
            time.sleep(0.5)

            # Simulate some failures
            if i == 3:
                stepper.fail(i, "2 tests failed")
                break
            else:
                stepper.complete(i)

    console.print()

    # Setup wizard
    console.print("[dim]Setup Wizard:[/dim]")
    wizard_steps = [
        "Welcome",
        "Choose installation directory",
        "Select components",
        "Configure database",
        "Create admin account",
        "Finalize setup",
    ]

    stepper = Stepper.from_list(wizard_steps, title="Setup Wizard")
    stepper.complete(0)
    stepper.complete(1)
    stepper.complete(2)
    stepper.start(3)

    console.print(stepper)
    console.print()

    # Data processing workflow
    console.print("[dim]Data Processing:[/dim]")
    processing_steps = [
        "Load data",
        "Clean data",
        "Transform data",
        "Validate data",
        "Export results",
    ]

    with Stepper.from_list(processing_steps, title="Data Pipeline", live=True) as stepper:
        for i in range(len(processing_steps)):
            stepper.start(i)
            time.sleep(0.6)
            stepper.complete(i)


def demo_complex_workflow():
    """Demonstrate a complex workflow with mixed outcomes."""
    console = get_console()
    console.print("\n\n[bold cyan]═══ Complex Workflow ═══[/bold cyan]\n")

    workflow_steps = [
        "Initialize workspace",
        "Download dependencies",
        "Build application",
        "Run unit tests",
        "Run integration tests",
        "Generate documentation",
        "Package artifacts",
        "Upload to registry",
        "Notify team",
    ]

    with Stepper.from_list(workflow_steps, title="Build & Deploy", live=True) as stepper:
        # Step 0: Success
        stepper.start(0)
        time.sleep(0.5)
        stepper.complete(0)

        # Step 1: Success
        stepper.start(1)
        time.sleep(0.7)
        stepper.complete(1)

        # Step 2: Success
        stepper.start(2)
        time.sleep(0.8)
        stepper.complete(2)

        # Step 3: Success
        stepper.start(3)
        time.sleep(0.6)
        stepper.complete(3)

        # Step 4: Failure
        stepper.start(4)
        time.sleep(0.7)
        stepper.fail(4, "Integration tests failed: API timeout")

        # Step 5: Skipped due to failure
        stepper.skip(5)

        # Step 6: Skipped
        stepper.skip(6)

        # Step 7: Skipped
        stepper.skip(7)

        # Step 8: Skipped
        stepper.skip(8)


def main():
    """Run all Stepper demos."""
    console = get_console()

    console.print(
        "\n[bold magenta]╔════════════════════════════════════════════════╗[/bold magenta]"
    )
    console.print("[bold magenta]║   ChalkBox - Stepper Component Demo           ║[/bold magenta]")
    console.print("[bold magenta]╚════════════════════════════════════════════════╝[/bold magenta]")

    demo_basic_usage()
    demo_advanced_features()
    demo_styling()
    demo_use_cases()
    demo_complex_workflow()

    console.print("\n[bold green]✓  Stepper demo completed![/bold green]")
    console.print(
        "\n[dim]Stepper is perfect for: multi-step workflows, wizards, pipelines, and progress tracking[/dim]\n"
    )


if __name__ == "__main__":
    main()
