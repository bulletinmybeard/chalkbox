from pathlib import Path
import random
import time

from chalkbox import (
    Alert,
    KeyValue,
    Progress,
    Section,
    Spinner,
    Stepper,
    Table,
    get_console,
    setup_logging,
)


class ProjectSetup:
    """Automated project setup orchestrator."""

    def __init__(self, repo_url: str, project_name: str):
        self.console = get_console()
        self.logger = setup_logging(level="INFO")
        self.repo_url = repo_url
        self.project_name = project_name
        self.project_path = Path.cwd() / project_name
        self.venv_path = self.project_path / ".venv"
        self.setup_errors = []
        self.setup_warnings = []

    def clone_repository(self):
        """Clone Git repository."""
        self.console.print("\n[bold cyan]📥 Cloning Repository[/bold cyan]\n")

        with Section("Repository Information") as section:
            repo_info = {
                "Repository URL": self.repo_url,
                "Target Directory": str(self.project_path),
                "Branch": "main",
                "Clone Method": "HTTPS",
            }
            kv = KeyValue(repo_info)
            section.add(kv)

        # Simulate git clone with progress
        with Progress() as progress:
            # Counting objects
            objects_task = progress.add_task("Counting objects", total=500)
            for _ in range(500):
                time.sleep(0.001)
                progress.update(objects_task, advance=1)

            # Cloning
            clone_task = progress.add_task("Cloning repository", total=1000)
            for _ in range(1000):
                time.sleep(0.002)
                progress.update(clone_task, advance=1)

            # Resolving deltas
            delta_task = progress.add_task("Resolving deltas", total=250)
            for _ in range(250):
                time.sleep(0.001)
                progress.update(delta_task, advance=1)

        # Show cloned files summary
        file_stats = {
            "Total Files": random.randint(50, 200),
            "Python Files": random.randint(20, 80),
            "Test Files": random.randint(10, 30),
            "Documentation": random.randint(5, 15),
            "Configuration": random.randint(3, 10),
        }

        self.console.print("\n")
        with Section("Cloned Repository Stats") as section:
            kv = KeyValue(file_stats)
            section.add(kv)

        self.logger.info(f"Repository cloned successfully to {self.project_path}")
        return True

    def create_virtual_environment(self):
        """Create Python virtual environment."""
        self.console.print("\n[bold cyan]🐍 Creating Virtual Environment[/bold cyan]\n")

        with Spinner("Creating virtual environment...") as spinner:
            time.sleep(2)

            # Simulate occasional failure
            if random.random() < 0.05:
                spinner.error("Failed to create virtual environment")
                self.setup_errors.append("Virtual environment creation failed")
                return False

            spinner.success("Virtual environment created")

        # Show venv details
        venv_info = {
            "Location": str(self.venv_path),
            "Python Version": f"3.{random.randint(10, 12)}.{random.randint(0, 5)}",
            "Pip Version": f"{random.randint(23, 24)}.{random.randint(0, 3)}",
            "Setuptools": f"{random.randint(68, 70)}.{random.randint(0, 2)}",
        }

        with Section("Virtual Environment Details") as section:
            kv = KeyValue(venv_info)
            section.add(kv)

        self.logger.info(f"Virtual environment created at {self.venv_path}")
        return True

    def install_dependencies(self):
        """Install project dependencies."""
        self.console.print("\n[bold cyan]Installing Dependencies[/bold cyan]\n")

        # Simulate reading requirements.txt
        dependencies = [
            {"name": "requests", "version": "2.31.0", "size": "58 kB"},
            {"name": "click", "version": "8.1.7", "size": "97 kB"},
            {"name": "pydantic", "version": "2.5.0", "size": "420 kB"},
            {"name": "pytest", "version": "7.4.3", "size": "320 kB"},
            {"name": "black", "version": "23.12.1", "size": "390 kB"},
            {"name": "ruff", "version": "0.1.8", "size": "8.2 MB"},
            {"name": "mypy", "version": "1.7.1", "size": "2.5 MB"},
            {"name": "httpx", "version": "0.25.2", "size": "85 kB"},
        ]

        # Show dependencies table
        with Section("Dependencies to Install") as section:
            table = Table.from_list_of_dicts(dependencies[:5], title="Primary Dependencies")
            section.add(table)
            section.add_text(f"... and {len(dependencies) - 5} more packages", style="dim")

        self.console.print()

        # Install with progress
        with Progress() as progress:
            overall_task = progress.add_task("[cyan]Installing packages", total=len(dependencies))

            for dep in dependencies:
                install_task = progress.add_task(f"Installing {dep['name']}", total=100)

                # Simulate installation
                for _ in range(100):
                    time.sleep(random.uniform(0.01, 0.03))
                    progress.update(install_task, advance=1)

                progress.remove_task(install_task)
                progress.update(overall_task, advance=1)

        # Check for dependency conflicts
        if random.random() < 0.15:
            self.setup_warnings.append(
                "Dependency version conflict detected between 'requests' and 'urllib3'"
            )
            self.console.print(
                Alert.warning(
                    "Dependency conflict detected",
                    details="Some packages may require version updates",
                )
            )
        else:
            self.console.print(Alert.success("All dependencies installed successfully"))

        self.logger.info(f"Installed {len(dependencies)} packages")
        return True

    def run_initial_tests(self):
        """Run initial test suite."""
        self.console.print("\n[bold cyan]🧪 Running Initial Tests[/bold cyan]\n")

        # Test categories
        test_suites = [
            {"suite": "Unit Tests", "tests": random.randint(20, 50)},
            {"suite": "Integration Tests", "tests": random.randint(10, 20)},
            {"suite": "API Tests", "tests": random.randint(5, 15)},
        ]

        total_tests = sum(suite["tests"] for suite in test_suites)
        test_results = {
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "failed_tests": [],
        }

        with Progress() as progress:
            for suite in test_suites:
                task = progress.add_task(f"Running {suite['suite']}", total=suite["tests"])

                for i in range(suite["tests"]):
                    time.sleep(random.uniform(0.05, 0.15))

                    # Simulate test results (90% pass rate)
                    result = random.random()
                    if result < 0.9:
                        test_results["passed"] += 1
                    elif result < 0.95:
                        test_results["failed"] += 1
                        test_results["failed_tests"].append(
                            f"test_{suite['suite'].lower().replace(' ', '_')}_{i}"
                        )
                    else:
                        test_results["skipped"] += 1

                    progress.update(task, advance=1)

        # Show test results
        self.console.print("\n")
        with Section("Test Results", subtitle="Summary") as section:
            results_table = Table(headers=["Status", "Count", "Percentage"])
            results_table.add_row(
                "Passed ✓",
                str(test_results["passed"]),
                f"{test_results['passed']/total_tests*100:.1f}%",
                severity="success",
            )
            results_table.add_row(
                "Failed ✖",
                str(test_results["failed"]),
                f"{test_results['failed']/total_tests*100:.1f}%",
                severity="error" if test_results["failed"] > 0 else "success",
            )
            results_table.add_row(
                "Skipped ⊘",
                str(test_results["skipped"]),
                f"{test_results['skipped']/total_tests*100:.1f}%",
            )

            section.add(results_table)

            # Show failed tests if any
            if test_results["failed_tests"]:
                section.add_spacing()
                section.add_text("Failed Tests:", style="bold red")
                for test in test_results["failed_tests"][:5]:
                    section.add_text(f"  • {test}", style="red")
                if len(test_results["failed_tests"]) > 5:
                    section.add_text(
                        f"  ... and {len(test_results['failed_tests']) - 5} more",
                        style="dim red",
                    )

        if test_results["failed"] > 0:
            self.setup_warnings.append(f"{test_results['failed']} tests failed during initial run")

        self.logger.info(
            f"Test run complete: {test_results['passed']} passed, "
            f"{test_results['failed']} failed, {test_results['skipped']} skipped"
        )

        return test_results["failed"] == 0


def run_project_setup():
    """Execute project setup workflow."""
    console = get_console()

    console.print("[bold magenta]═══════════════════════════════════════════════[/bold magenta]")
    console.print("[bold magenta]       Project Setup Automation[/bold magenta]")
    console.print("[bold magenta]═══════════════════════════════════════════════[/bold magenta]\n")

    # Project configuration
    project_config = {
        "Repository": "https://github.com/acme/awesome-project",
        "Project Name": "awesome-project",
        "Language": "Python 3.12",
        "Package Manager": "pip",
        "Test Framework": "pytest",
    }

    with Section("Project Configuration") as section:
        kv = KeyValue(project_config)
        section.add(kv)

    # Initialize setup manager
    setup = ProjectSetup(
        repo_url=project_config["Repository"],
        project_name=project_config["Project Name"],
    )

    # Setup steps
    steps = [
        "Clone Git repository",
        "Create virtual environment",
        "Install dependencies",
        "Run initial tests",
        "Finalize setup",
    ]

    console.print("\n")
    stepper = Stepper.from_list(steps, title="Setup Progress")
    console.print(stepper)

    # Execute setup steps
    start_time = time.time()

    # Step 1: Clone repository
    stepper.start(0)
    if setup.clone_repository():
        stepper.complete(0)
    else:
        stepper.fail(0, "Clone failed")
        return

    # Step 2: Create virtual environment
    stepper.start(1)
    if setup.create_virtual_environment():
        stepper.complete(1)
    else:
        stepper.fail(1, "Failed to create venv")
        console.print("\n")
        console.print(stepper)
        return

    # Step 3: Install dependencies
    stepper.start(2)
    if setup.install_dependencies():
        stepper.complete(2)
    else:
        stepper.fail(2, "Dependency installation failed")
        console.print("\n")
        console.print(stepper)
        return

    # Step 4: Run tests
    stepper.start(3)
    tests_passed = setup.run_initial_tests()
    if tests_passed:
        stepper.complete(3)
    else:
        stepper.complete(3)  # Complete with warnings

    # Step 5: Finalize
    stepper.start(4)
    with Spinner("Creating configuration files...") as spinner:
        time.sleep(1)
        spinner.success("Configuration complete")
    stepper.complete(4)

    # Calculate setup time
    setup_time = time.time() - start_time

    # Final summary
    console.print("\n")
    console.print(stepper)

    console.print("\n")
    with Section("Setup Summary", subtitle="Project Ready") as section:
        summary = {
            "Status": "✓ Ready" if not setup.setup_errors else "⚠ Needs Attention",
            "Setup Time": f"{setup_time:.1f}s",
            "Project Path": str(setup.project_path),
            "Virtual Environment": str(setup.venv_path),
            "Errors": len(setup.setup_errors),
            "Warnings": len(setup.setup_warnings),
        }

        kv = KeyValue(summary)
        section.add(kv)

        # Show errors/warnings if any
        if setup.setup_errors:
            section.add_spacing()
            section.add_text("Errors:", style="bold red")
            for error in setup.setup_errors:
                section.add_text(f"  • {error}", style="red")

        if setup.setup_warnings:
            section.add_spacing()
            section.add_text("Warnings:", style="bold yellow")
            for warning in setup.setup_warnings:
                section.add_text(f"  • {warning}", style="yellow")

    # Next steps
    console.print("\n")
    with Section("Next Steps") as section:
        section.add_text("1. Activate virtual environment:", style="bold")
        section.add_text(f"   source {setup.venv_path}/bin/activate", style="dim cyan")
        section.add_spacing()

        section.add_text("2. Start development server:", style="bold")
        section.add_text("   python manage.py runserver", style="dim cyan")
        section.add_spacing()

        section.add_text("3. Run tests:", style="bold")
        section.add_text("   pytest tests/", style="dim cyan")

    # Final status alert
    console.print("\n")
    if setup.setup_errors:
        console.print(
            Alert.error(
                "Setup completed with errors",
                details=f"Found {len(setup.setup_errors)} critical issues",
            )
        )
    elif setup.setup_warnings:
        console.print(
            Alert.warning(
                "Setup completed with warnings",
                details=f"Found {len(setup.setup_warnings)} warnings to review",
            )
        )
    else:
        console.print(
            Alert.success(
                "Project setup completed successfully",
                details="Your development environment is ready!",
            )
        )


if __name__ == "__main__":
    run_project_setup()
