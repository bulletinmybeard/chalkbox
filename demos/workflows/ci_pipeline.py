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


class CIBuildPipeline:
    """CI/CD build pipeline orchestrator."""

    def __init__(self, branch: str, commit: str):
        self.console = get_console()
        self.logger = setup_logging(level="INFO")
        self.branch = branch
        self.commit = commit
        self.build_artifacts = []
        self.test_results = {}
        self.build_failed = False
        self.build_logs = []

    def checkout_code(self):
        """Checkout code from repository."""
        self.console.print("\n[bold cyan]📥 Checking Out Code[/bold cyan]\n")

        repo_info = {
            "Repository": "github.com/acme/awesome-app",
            "Branch": self.branch,
            "Commit": self.commit,
            "Author": "developer@example.com",
            "Message": "feat: add new feature with tests",
        }

        with Section("Repository Information") as section:
            kv = KeyValue(repo_info)
            section.add(kv)

        self.console.print()

        # Simulate git operations
        with Progress() as progress:
            # Fetching
            fetch_task = progress.add_task("Fetching from origin", total=100)
            for _ in range(100):
                time.sleep(0.01)
                progress.update(fetch_task, advance=1)

            # Checking out
            checkout_task = progress.add_task("Checking out code", total=50)
            for _ in range(50):
                time.sleep(0.01)
                progress.update(checkout_task, advance=1)

        file_count = random.randint(150, 300)
        self.console.print(Alert.success(f"Checked out {file_count} files"))
        self.build_logs.append(f"✓ Checkout complete: {file_count} files")

        return True

    def install_dependencies(self):
        """Install project dependencies."""
        self.console.print("\n[bold cyan]Installing Dependencies[/bold cyan]\n")

        dependencies = [
            "fastapi",
            "uvicorn",
            "sqlalchemy",
            "pydantic",
            "pytest",
            "pytest-cov",
            "ruff",
            "mypy",
            "httpx",
            "redis",
        ]

        with Progress() as progress:
            task = progress.add_task("Installing packages", total=len(dependencies))

            for dep in dependencies:
                self.console.print(f"  [dim]→[/dim] Installing {dep}...")
                time.sleep(random.uniform(0.3, 0.8))
                progress.update(task, advance=1)

        self.console.print(Alert.success(f"Installed {len(dependencies)} packages"))
        self.build_logs.append(f"✓ Dependencies installed: {len(dependencies)} packages")

        return True

    def run_build(self):
        """Run build process."""
        self.console.print("\n[bold cyan]🔨 Building Application[/bold cyan]\n")

        build_steps = [
            "Compiling TypeScript",
            "Bundling JavaScript",
            "Processing CSS",
            "Optimizing images",
            "Generating static assets",
            "Creating build manifest",
        ]

        with Progress() as progress:
            task = progress.add_task("Building application", total=len(build_steps))

            for step in build_steps:
                self.console.print(f"  [dim]→[/dim] {step}...")
                time.sleep(random.uniform(0.5, 1.5))

                # Simulate occasional build warnings
                if random.random() < 0.2:
                    warning_msg = f"Warning in {step.lower()}: optimization skipped"
                    self.console.print(f"    [yellow]⚠[/yellow] {warning_msg}")
                    self.build_logs.append(f"⚠ {warning_msg}")

                progress.update(task, advance=1)

        # Generate build artifacts
        self.build_artifacts = [
            {"artifact": "app.bundle.js", "size": "1.2 MB", "hash": "a3f7b8c"},
            {"artifact": "app.css", "size": "245 KB", "hash": "9e2d1f4"},
            {"artifact": "index.html", "size": "12 KB", "hash": "5c8a3b1"},
            {"artifact": "manifest.json", "size": "2 KB", "hash": "f1e9d7c"},
        ]

        with Section("Build Artifacts") as section:
            artifacts_table = Table.from_list_of_dicts(self.build_artifacts)
            section.add(artifacts_table)

        self.console.print(
            Alert.success(f"Build complete: {len(self.build_artifacts)} artifacts generated")
        )
        self.build_logs.append(f"✓ Build complete: {len(self.build_artifacts)} artifacts")

        return True

    def run_tests(self):
        """Run test suite."""
        self.console.print("\n[bold cyan]🧪 Running Tests[/bold cyan]\n")

        test_suites = [
            {"name": "Unit Tests", "count": 45},
            {"name": "Integration Tests", "count": 22},
            {"name": "E2E Tests", "count": 12},
        ]

        total_tests = sum(suite["count"] for suite in test_suites)
        passed = 0
        failed = 0
        failed_tests = []

        with Progress() as progress:
            overall_task = progress.add_task("Running all tests", total=total_tests)

            for suite in test_suites:
                suite_task = progress.add_task(f"Running {suite['name']}", total=suite["count"])

                for i in range(suite["count"]):
                    time.sleep(random.uniform(0.05, 0.15))

                    # 92% pass rate
                    if random.random() < 0.92:
                        passed += 1
                    else:
                        failed += 1
                        failed_tests.append(f"test_{suite['name'].lower().replace(' ', '_')}_{i}")

                    progress.update(suite_task, advance=1)
                    progress.update(overall_task, advance=1)

                progress.remove_task(suite_task)

        self.test_results = {
            "total": total_tests,
            "passed": passed,
            "failed": failed,
            "pass_rate": passed / total_tests * 100,
        }

        # Display results
        self.console.print("\n")
        with Section("Test Results") as section:
            results_table = Table(headers=["Metric", "Value"])
            results_table.add_row("Total Tests", str(total_tests))
            results_table.add_row("Passed ✓", str(passed), severity="success")
            results_table.add_row(
                "Failed ✖",
                str(failed),
                severity="error" if failed > 0 else "success",
            )
            results_table.add_row(
                "Pass Rate",
                f"{self.test_results['pass_rate']:.1f}%",
            )

            section.add(results_table)

            if failed_tests:
                section.add_spacing()
                section.add_text("Failed Tests:", style="bold red")
                for test in failed_tests[:5]:
                    section.add_text(f"  • {test}", style="red")
                if len(failed_tests) > 5:
                    section.add_text(f"  ... and {len(failed_tests) - 5} more", style="dim red")

        # Check if tests passed threshold
        if failed > 3:
            self.build_failed = True
            self.console.print(
                Alert.error(
                    "Test suite failed",
                    details=f"{failed} tests failed (threshold: 3)",
                )
            )
            self.build_logs.append(f"✖ Tests failed: {failed} failures")
            return False
        elif failed > 0:
            self.console.print(Alert.warning(f"{failed} tests failed but within threshold"))
            self.build_logs.append(f"⚠ Tests passed with {failed} failures")
            return True
        else:
            self.console.print(Alert.success("All tests passed"))
            self.build_logs.append("✓ All tests passed")
            return True

    def deploy_staging(self):
        """Deploy to staging environment."""
        self.console.print("\n[bold cyan]Deploying to Staging[/bold cyan]\n")

        deploy_steps = [
            "Preparing deployment package",
            "Uploading artifacts to S3",
            "Updating infrastructure",
            "Deploying to instances",
            "Running database migrations",
            "Warming up cache",
            "Running smoke tests",
        ]

        with Progress() as progress:
            task = progress.add_task("Deploying to staging", total=len(deploy_steps))

            for step in deploy_steps:
                self.console.print(f"  [dim]→[/dim] {step}...")
                time.sleep(random.uniform(0.5, 1.2))
                progress.update(task, advance=1)

        # Deployment info
        deploy_info = {
            "Environment": "staging",
            "URL": "https://staging.awesome-app.com",
            "Instances": "3",
            "Load Balancer": "staging-lb-1",
            "Health Check": "✓ Passed",
        }

        with Section("Deployment Information") as section:
            kv = KeyValue(deploy_info)
            section.add(kv)

        self.console.print(Alert.success("Deployed to staging successfully"))
        self.build_logs.append("✓ Deployment complete: staging")

        return True


def run_ci_build():
    """Execute CI/CD build pipeline."""
    console = get_console()

    console.print("[bold magenta]═══════════════════════════════════════════════[/bold magenta]")
    console.print("[bold magenta]           CI/CD Build Pipeline[/bold magenta]")
    console.print("[bold magenta]═══════════════════════════════════════════════[/bold magenta]\n")

    # Build configuration
    build_config = {
        "Build Number": "#" + str(random.randint(1000, 9999)),
        "Branch": "main",
        "Commit": "abc123f",
        "Triggered By": "push event",
        "Runner": "ubuntu-latest",
        "Started": "2024-01-15 10:30:00 UTC",
    }

    with Section("Build Configuration") as section:
        kv = KeyValue(build_config)
        section.add(kv)

    # Initialize pipeline
    pipeline = CIBuildPipeline(branch=build_config["Branch"], commit=build_config["Commit"])

    # Pipeline steps
    steps = [
        "Checkout code",
        "Install dependencies",
        "Build application",
        "Run tests",
        "Deploy to staging",
        "Generate report",
    ]

    console.print("\n")
    stepper = Stepper.from_list(steps, title="Pipeline Steps")
    console.print(stepper)

    # Execute pipeline
    start_time = time.time()

    # Step 1: Checkout
    stepper.start(0)
    if pipeline.checkout_code():
        stepper.complete(0)
    else:
        stepper.fail(0, "Checkout failed")
        return

    # Step 2: Dependencies
    stepper.start(1)
    if pipeline.install_dependencies():
        stepper.complete(1)
    else:
        stepper.fail(1, "Dependency installation failed")
        return

    # Step 3: Build
    stepper.start(2)
    if pipeline.run_build():
        stepper.complete(2)
    else:
        stepper.fail(2, "Build failed")
        console.print("\n")
        console.print(stepper)
        return

    # Step 4: Tests
    stepper.start(3)
    tests_passed = pipeline.run_tests()
    if tests_passed:
        stepper.complete(3)
    else:
        stepper.fail(3, "Tests failed")
        console.print("\n")
        console.print(stepper)
        return

    # Step 5: Deploy
    stepper.start(4)
    if pipeline.deploy_staging():
        stepper.complete(4)
    else:
        stepper.fail(4, "Deployment failed")
        console.print("\n")
        console.print(stepper)
        return

    # Step 6: Report
    stepper.start(5)
    with Spinner("Generating build report...") as spinner:
        time.sleep(1)
        spinner.success("Report generated")
    stepper.complete(5)

    build_time = time.time() - start_time

    # Final summary
    console.print("\n")
    console.print(stepper)

    console.print("\n")
    with Section("Build Summary", subtitle="Pipeline Complete") as section:
        summary = {
            "Build Status": "✓ Success" if not pipeline.build_failed else "✖ Failed",
            "Build Time": f"{build_time:.1f}s",
            "Total Tests": pipeline.test_results.get("total", 0),
            "Test Pass Rate": f"{pipeline.test_results.get('pass_rate', 0):.1f}%",
            "Artifacts": len(pipeline.build_artifacts),
            "Deployment": "staging",
        }

        kv = KeyValue(summary)
        section.add(kv)

    # Build logs summary
    console.print("\n")
    with Section("Build Logs", subtitle="Summary") as section:
        for log in pipeline.build_logs[-10:]:
            if "✓" in log:
                style = "green"
            elif "✖" in log:
                style = "red"
            elif "⚠" in log:
                style = "yellow"
            else:
                style = "white"

            section.add_text(f"  {log}", style=style)

    # Artifacts
    if pipeline.build_artifacts:
        console.print("\n")
        with Section("Build Artifacts") as section:
            section.add_text("Available at:", style="bold")
            section.add_text(
                "  https://artifacts.ci.awesome-app.com/builds/" + build_config["Build Number"],
                style="cyan",
            )

    # Next steps
    console.print("\n")
    with Section("Next Steps") as section:
        if not pipeline.build_failed:
            section.add_text("✓ Build successful!", style="bold green")
            section.add_spacing()
            section.add_text("To promote to production:", style="bold")
            section.add_text("  1. Review staging deployment", style="dim")
            section.add_text("  2. Run manual tests", style="dim")
            section.add_text("  3. Trigger production deployment", style="dim")
        else:
            section.add_text("✖ Build failed", style="bold red")
            section.add_spacing()
            section.add_text("To fix:", style="bold")
            section.add_text("  1. Review failed tests", style="dim")
            section.add_text("  2. Fix issues in code", style="dim")
            section.add_text("  3. Push fixes and retry", style="dim")

    # Final status
    console.print("\n")
    if not pipeline.build_failed:
        console.print(
            Alert.success(
                "Build pipeline completed successfully",
                details=f"Build {build_config['Build Number']} deployed to staging",
            )
        )
    else:
        console.print(
            Alert.error(
                "Build pipeline failed",
                details="Fix the issues above and retry the build",
            )
        )


if __name__ == "__main__":
    run_ci_build()
