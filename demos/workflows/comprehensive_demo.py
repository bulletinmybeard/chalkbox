import random
import time

from chalkbox import (
    Alert,
    Divider,
    KeyValue,
    Progress,
    Section,
    Spinner,
    Stepper,
    Table,
    get_console,
    setup_logging,
)


def simulate_database_migration():
    """Simulate a database migration workflow."""
    console = get_console()

    console.print("[bold cyan]Database Migration Tool v1.0[/bold cyan]\n")

    # Show configuration
    config = {
        "source_db": "production_v1",
        "target_db": "production_v2",
        "host": "db.example.com",
        "port": 5432,
        "user": "migrator",
        "password": "secret_key_123",
        "batch_size": 1000,
        "parallel_workers": 4,
    }

    with Section("Migration Configuration") as section:
        kv = KeyValue(config)
        section.add(kv)

    # Confirmation
    console.print(
        Alert.warning(
            "This will migrate all data from production_v1 to production_v2",
            details="Ensure you have a backup before proceeding",
        )
    )

    # Migration steps
    steps = [
        ("Validate source database", "Check schema and data integrity"),
        ("Create target schema", "Set up tables and indexes"),
        ("Migrate user data", "Transfer user accounts and profiles"),
        ("Migrate transactions", "Transfer transaction history"),
        ("Verify data integrity", "Compare checksums and counts"),
        ("Update sequences", "Sync primary key sequences"),
        ("Run validation tests", "Execute test suite on new database"),
        ("Switch traffic", "Update load balancer configuration"),
    ]

    console.print("\n")

    with Stepper(title="Migration Steps", live=True) as stepper:
        for name, desc in steps:
            stepper.add_step(name, desc)

        for i in range(len(steps)):
            step_name = steps[i][0]

            # Start the step
            stepper.start(i)

            # Simulate work (can't use nested Live displays)
            if "Migrate" in step_name:
                # Simulate migration with delay
                time.sleep(2)
                console.print(f"    [green]✓[/green] {step_name} completed")
            else:
                # Simulate other tasks
                time.sleep(random.uniform(0.5, 2))
                console.print(f"    [green]✓[/green] {step_name} completed")

            # Random success/failure for demo
            if i == 6:  # Fail validation tests
                stepper.fail(i, "5 tests failed: auth_test, profile_test")
            elif i == 7:  # Skip traffic switch due to failure
                stepper.skip(i)
            else:
                stepper.complete(i)

    # Show results
    console.print("\n")

    with Section("Migration Summary", subtitle="Completed with errors") as section:
        section.add(
            Alert.error(
                "Migration completed with failures",
                details="Manual intervention required for test failures",
            )
        )

        section.add_spacing()

        stats = Table(title="Statistics", headers=["Metric", "Value"])
        stats.add_row("Total Records", "1,234,567")
        stats.add_row("Migration Time", "12m 34s")
        stats.add_row("Success Rate", "87.5%")
        stats.add_row("Failed Steps", "1")
        stats.add_row("Skipped Steps", "1")

        section.add(stats)


def simulate_deployment_pipeline():
    """Simulate a deployment pipeline."""
    console = get_console()

    console.print("\n[bold cyan]Deployment Pipeline[/bold cyan]\n")

    # Setup logging for this operation
    logger = setup_logging(level="INFO")

    logger.info("Starting deployment pipeline")

    # Show deployment targets
    targets = [
        {"name": "web-01", "region": "us-east-1", "type": "t3.large", "status": "ready"},
        {"name": "web-02", "region": "us-east-1", "type": "t3.large", "status": "ready"},
        {"name": "web-03", "region": "us-west-2", "type": "t3.large", "status": "ready"},
        {"name": "worker-01", "region": "us-east-1", "type": "t3.medium", "status": "maintenance"},
    ]

    table = Table.from_list_of_dicts(targets, title="Deployment Targets")
    console.print(table)

    console.print("\n")

    # Deployment progress
    with Progress() as progress:
        build_task = progress.add_task("Building application", total=100)
        test_task = progress.add_task("Running tests", total=50)
        deploy_task = progress.add_task("Deploying to servers", total=3)

        # Build
        for _i in range(100):
            progress.update(build_task, advance=1)
            time.sleep(0.01)

        logger.info("Build completed successfully")

        # Test
        for _i in range(50):
            progress.update(test_task, advance=1)
            time.sleep(0.02)

        logger.info("All tests passed")

        # Deploy
        for _i, target in enumerate([t for t in targets if t["status"] == "ready"]):
            logger.info(f"Deploying to {target['name']}")
            progress.update(deploy_task, advance=1)
            time.sleep(1)

    console.print("\n")
    console.print(Alert.success("Deployment completed successfully!"))


def simulate_system_health_check():
    """Simulate a system health check."""
    console = get_console()

    console.print("\n[bold cyan]System Health Check[/bold cyan]\n")

    with Spinner("Running system diagnostics...") as spinner:
        time.sleep(2)
        spinner.success("Diagnostics complete")

    # Health metrics
    health_data = {
        "CPU Usage": "45%",
        "Memory Usage": "67%",
        "Disk Usage": "72%",
        "Network Latency": "12ms",
        "Database Connections": "42/100",
        "Cache Hit Rate": "94%",
        "API Response Time": "145ms",
        "Error Rate": "0.02%",
    }

    with Section("System Metrics") as section:
        # Create a table with severity-based coloring
        table = Table(headers=["Metric", "Value", "Status"], row_styles="severity")

        for metric, value in health_data.items():
            # Determine status based on metric
            if metric == "Disk Usage":
                status = "⚠ Warning"
                severity = "warning"
            elif metric == "Error Rate":
                if float(value.rstrip("%")) > 1:
                    status = "✖ Critical"
                    severity = "error"
                else:
                    status = "✓  Healthy"
                    severity = "success"
            else:
                status = "✓  Healthy"
                severity = "success"

            table.add_row(metric, value, status, severity=severity)

        section.add(table)

    # Show alerts for any issues
    console.print("\n")
    console.print(
        Alert.warning(
            "Disk usage is above 70%", details="Consider cleaning up old logs and temporary files"
        )
    )


def main():
    """Run the full demo."""
    console = get_console()

    console.print(
        "[bold magenta]═══════════════════════════════════════════════════[/bold magenta]"
    )
    console.print("[bold magenta]     🎨 ChalkBox - Full Application Demo[/bold magenta]")
    console.print(
        "[bold magenta]═══════════════════════════════════════════════════[/bold magenta]\n"
    )

    # Run different scenarios
    scenarios = [
        ("Database Migration", simulate_database_migration),
        ("Deployment Pipeline", simulate_deployment_pipeline),
        ("System Health Check", simulate_system_health_check),
    ]

    stepper = Stepper.from_list([name for name, _ in scenarios], title="Demo Scenarios")
    console.print(stepper)
    console.print("\n")

    for i, (name, scenario_func) in enumerate(scenarios):
        console.print()
        console.print(Divider(style="dim", character="═"))
        console.print(f"[bold yellow]Scenario {i+1}: {name}[/bold yellow]")
        console.print(Divider(style="dim", character="═"))
        console.print()

        scenario_func()

        time.sleep(1)

    console.print()
    console.print(Divider(style="dim", character="═"))
    console.print("\n[bold green]✓  Demo completed successfully![/bold green]")
    console.print("\nChalkBox provides consistent, beautiful CLI components")
    console.print("for building professional command-line applications.\n")


if __name__ == "__main__":
    main()
