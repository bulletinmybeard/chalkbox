import argparse
from datetime import datetime
import platform
import random
import sys
import time

from rich.panel import Panel
from rich.text import Text

from chalkbox import (
    Alert,
    Dashboard,
    KeyValue,
    Progress,
    Section,
    Spinner,
    Stepper,
    Table,
    get_console,
    setup_logging,
)


class ReleaseOrchestrator:
    """Application release orchestrator."""

    def __init__(self, version: str, branch: str, commit: str):
        self.console = get_console()
        self.logger = setup_logging(level="INFO")
        self.version = version
        self.branch = branch
        self.commit = commit
        self.start_time = None
        self.release_failed = False
        self.warnings = []
        self.deployment_targets = []
        self.test_results = {}
        self.health_checks = []

    def check_environment(self):
        """Check release environment prerequisites."""
        self.console.print("\n[bold cyan]🔍 Environment Check[/bold cyan]\n")

        env_checks = []

        # Check Python version
        with Spinner("Checking Python version...") as spinner:
            time.sleep(0.5)
            python_version = platform.python_version()
            major, minor, _ = python_version.split(".")

            if int(major) >= 3 and int(minor) >= 10:
                spinner.success(f"Python {python_version} ✓")
                env_checks.append(
                    {
                        "Check": "Python",
                        "Required": "3.10+",
                        "Actual": python_version,
                        "Status": "✓",
                    }
                )
            else:
                spinner.warning(f"Python {python_version} is outdated")
                env_checks.append(
                    {
                        "Check": "Python",
                        "Required": "3.10+",
                        "Actual": python_version,
                        "Status": "⚠",
                    }
                )
                self.warnings.append(f"Python {python_version} is below recommended 3.10+")

        # Check Docker
        with Spinner("Checking Docker...") as spinner:
            time.sleep(0.5)
            docker_available = random.random() < 0.95

            if docker_available:
                spinner.success("Docker available ✓")
                env_checks.append(
                    {"Check": "Docker", "Required": "20.0+", "Actual": "24.0.6", "Status": "✓"}
                )
            else:
                spinner.error("Docker not available")
                env_checks.append(
                    {"Check": "Docker", "Required": "20.0+", "Actual": "Not found", "Status": "✖"}
                )
                self.release_failed = True

        # Check disk space
        with Spinner("Checking disk space...") as spinner:
            time.sleep(0.5)
            available_gb = random.randint(15, 100)

            if available_gb >= 10:
                spinner.success(f"{available_gb} GB available ✓")
                env_checks.append(
                    {
                        "Check": "Disk Space",
                        "Required": "10 GB",
                        "Actual": f"{available_gb} GB",
                        "Status": "✓",
                    }
                )
            else:
                spinner.error(f"Only {available_gb} GB available")
                env_checks.append(
                    {
                        "Check": "Disk Space",
                        "Required": "10 GB",
                        "Actual": f"{available_gb} GB",
                        "Status": "✖",
                    }
                )
                self.release_failed = True

        # Check network
        with Spinner("Checking network connectivity...") as spinner:
            time.sleep(0.5)
            network_ok = random.random() < 0.98

            if network_ok:
                spinner.success("Network connectivity ✓")
                env_checks.append(
                    {"Check": "Network", "Required": "Active", "Actual": "Connected", "Status": "✓"}
                )
            else:
                spinner.error("Network connectivity failed")
                env_checks.append(
                    {
                        "Check": "Network",
                        "Required": "Active",
                        "Actual": "Disconnected",
                        "Status": "✖",
                    }
                )
                self.release_failed = True

        # Display environment checks
        with Section("Environment Prerequisites") as section:
            checks_table = Table.from_list_of_dicts(env_checks)
            section.add(checks_table)

        if self.release_failed:
            self.console.print(
                Alert.error(
                    "Environment check failed", details="Fix critical issues before proceeding"
                )
            )
            return False
        elif self.warnings:
            self.console.print(
                Alert.warning(
                    "Environment check passed with warnings",
                    details=f"{len(self.warnings)} warnings",
                )
            )
        else:
            self.console.print(Alert.success("Environment check passed"))

        return True

    def fetch_artifact(self):
        """Download and extract release artifact."""
        self.console.print("\n[bold cyan]📥 Fetching Release Artifact[/bold cyan]\n")

        # Artifact metadata
        artifact_info = {
            "Version": self.version,
            "Branch": self.branch,
            "Commit": self.commit,
            "Size": "120 MB",
            "Format": "tar.gz",
            "Registry": "https://artifacts.company.com",
        }

        with Section("Artifact Information") as section:
            kv = KeyValue(artifact_info)
            section.add(kv)

        self.console.print()

        # Download artifact
        size_mb = 120
        size_bytes = size_mb * 1024 * 1024

        with Progress() as progress:
            download_task = progress.add_task(
                f"[cyan]Downloading release-{self.version}.tar.gz", total=size_bytes
            )

            downloaded = 0
            while downloaded < size_bytes:
                chunk = random.randint(500000, 2000000)
                chunk = min(chunk, size_bytes - downloaded)
                time.sleep(0.01)
                downloaded += chunk
                progress.update(download_task, advance=chunk)

        self.console.print(
            Alert.success(f"Downloaded release-{self.version}.tar.gz ({size_mb} MB)")
        )

        # Extract artifact
        with Spinner("Extracting archive...") as spinner:
            time.sleep(2)

            if random.random() < 0.98:  # 98% success
                spinner.success("Archive extracted successfully")
                return True
            else:
                spinner.error("Archive extraction failed")
                self.release_failed = True
                return False

    def build_application(self):
        """Build application with dependencies."""
        self.console.print("\n[bold cyan]🔨 Building Application[/bold cyan]\n")

        build_steps = [
            ("Installing dependencies", 15),
            ("Compiling backend code", 10),
            ("Bundling frontend assets", 12),
            ("Optimizing images", 5),
            ("Generating static files", 8),
        ]

        with Progress() as progress:
            overall_task = progress.add_task("[cyan]Overall build progress", total=len(build_steps))

            for step_name, duration in build_steps:
                step_task = progress.add_task(f"{step_name}", total=100)

                for _i in range(100):
                    time.sleep(duration / 100)
                    progress.update(step_task, advance=1)

                # Simulate occasional build warnings
                if random.random() < 0.15:
                    warning = f"{step_name}: optimization skipped for performance"
                    self.warnings.append(warning)
                    self.console.print(f"  [yellow]⚠[/yellow] {warning}")

                # Simulate build failure (5% chance)
                if random.random() < 0.05:
                    self.console.print(f"  [red]✖[/red] {step_name} failed")
                    self.release_failed = True
                    progress.remove_task(step_task)
                    self.console.print(
                        Alert.error(
                            "Build failed", details=f"Error in {step_name}: dependency conflict"
                        )
                    )
                    return False

                progress.remove_task(step_task)
                progress.update(overall_task, advance=1)

        # Build artifacts
        build_artifacts = [
            {"Artifact": "backend.whl", "Size": "15 MB", "Type": "Python Package"},
            {"Artifact": "frontend.bundle.js", "Size": "2.3 MB", "Type": "JavaScript"},
            {"Artifact": "frontend.bundle.css", "Size": "450 KB", "Type": "Stylesheet"},
            {"Artifact": "assets.tar.gz", "Size": "8.2 MB", "Type": "Static Assets"},
        ]

        with Section("Build Artifacts") as section:
            artifacts_table = Table.from_list_of_dicts(build_artifacts)
            section.add(artifacts_table)

        self.console.print(Alert.success("Build completed successfully"))
        return True

    def run_tests(self):
        """Execute test suite."""
        self.console.print("\n[bold cyan]🧪 Running Tests[/bold cyan]\n")

        test_suites = [
            {"name": "Unit Tests", "count": 65},
            {"name": "Integration Tests", "count": 28},
            {"name": "API Tests", "count": 15},
            {"name": "E2E Tests", "count": 12},
        ]

        total_tests = sum(suite["count"] for suite in test_suites)
        passed = 0
        failed = 0
        skipped = 0
        failed_tests = []

        with Progress() as progress:
            overall_task = progress.add_task("[cyan]Running all tests", total=total_tests)

            for suite in test_suites:
                suite_task = progress.add_task(f"Running {suite['name']}", total=suite["count"])

                for i in range(suite["count"]):
                    time.sleep(random.uniform(0.03, 0.1))

                    # Test results (92% pass rate)
                    result = random.random()
                    if result < 0.92:
                        passed += 1
                    elif result < 0.97:
                        failed += 1
                        failed_tests.append(f"test_{suite['name'].lower().replace(' ', '_')}_{i}")
                    else:
                        skipped += 1

                    progress.update(suite_task, advance=1)
                    progress.update(overall_task, advance=1)

                progress.remove_task(suite_task)

        self.test_results = {
            "total": total_tests,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "pass_rate": (passed / total_tests * 100) if total_tests > 0 else 0,
        }

        # Display test results
        with Section("Test Results", subtitle="Summary") as section:
            results_table = Table(headers=["Metric", "Count", "Percentage"])
            results_table.add_row(
                "Passed ✓", str(passed), f"{passed/total_tests*100:.1f}%", severity="success"
            )
            results_table.add_row(
                "Failed ✖",
                str(failed),
                f"{failed/total_tests*100:.1f}%",
                severity="error" if failed > 0 else "success",
            )
            results_table.add_row("Skipped ⊘", str(skipped), f"{skipped/total_tests*100:.1f}%")

            section.add(results_table)

            # Show failed tests
            if failed_tests:
                section.add_spacing()
                section.add_text("Failed Tests:", style="bold red")
                for test in failed_tests[:5]:
                    section.add_text(f"  • {test}", style="red")
                if len(failed_tests) > 5:
                    section.add_text(f"  ... and {len(failed_tests) - 5} more", style="dim red")

        # Check if tests meet threshold
        pass_threshold = 95
        if self.test_results["pass_rate"] < pass_threshold:
            self.console.print(
                Alert.error(
                    "Tests failed",
                    details=f"Pass rate {self.test_results['pass_rate']:.1f}% is below {pass_threshold}% threshold",
                )
            )
            self.release_failed = True
            return False
        elif failed > 0:
            self.console.print(
                Alert.warning(
                    f"Tests passed with {failed} failures",
                    details=f"Pass rate: {self.test_results['pass_rate']:.1f}%",
                )
            )
            self.warnings.append(f"{failed} tests failed but within acceptable threshold")
        else:
            self.console.print(Alert.success("All tests passed"))

        return True

    def deploy_to_targets(self):
        """Deploy application to target servers."""
        self.console.print("\n[bold cyan]Deploying to Targets[/bold cyan]\n")

        # Deployment targets
        targets = [
            {"name": "web-01.prod", "type": "Web Server", "region": "us-east-1"},
            {"name": "web-02.prod", "type": "Web Server", "region": "us-east-1"},
            {"name": "web-03.prod", "type": "Web Server", "region": "us-west-2"},
            {"name": "api-01.prod", "type": "API Server", "region": "us-east-1"},
            {"name": "api-02.prod", "type": "API Server", "region": "us-west-2"},
            {"name": "worker-01.prod", "type": "Worker", "region": "us-east-1"},
        ]

        # Show deployment plan
        with Section("Deployment Plan") as section:
            targets_table = Table.from_list_of_dicts(targets)
            section.add(targets_table)

        self.console.print()

        # Deploy to each target
        for target in targets:
            self.console.print(f"\n[bold]Deploying to {target['name']}[/bold]")

            deployment_steps = [
                "Stopping old version",
                "Uploading new artifacts",
                "Starting new version",
                "Running health checks",
            ]

            with Progress() as progress:
                task = progress.add_task(
                    f"Deploying to {target['name']}", total=len(deployment_steps)
                )

                for _step in deployment_steps:
                    time.sleep(random.uniform(0.5, 1.5))
                    progress.update(task, advance=1)

            # Simulate deployment failure (8% chance)
            if random.random() < 0.08:
                status = "Failed"
                health = "Unhealthy"
                self.console.print(f"  [red]✖[/red] Deployment failed on {target['name']}")
                self.release_failed = True
            else:
                status = "Deployed"
                health = "Healthy"
                self.console.print(f"  [green]✓[/green] Successfully deployed to {target['name']}")

            self.deployment_targets.append(
                {
                    "Target": target["name"],
                    "Type": target["type"],
                    "Region": target["region"],
                    "Status": status,
                    "Health": health,
                }
            )

        # Deployment summary
        self.console.print("\n")
        with Section("Deployment Summary") as section:
            deployment_table = Table.from_list_of_dicts(self.deployment_targets)
            section.add(deployment_table)

        successful = sum(1 for t in self.deployment_targets if t["Status"] == "Deployed")
        failed = len(self.deployment_targets) - successful

        if failed > 0:
            self.console.print(
                Alert.error(
                    f"{failed} deployments failed", details="Review failed targets and retry"
                )
            )
            return False
        else:
            self.console.print(
                Alert.success(f"Successfully deployed to all {len(targets)} targets")
            )
            return True

    def verify_health(self):
        """Verify application health after deployment."""
        self.console.print("\n[bold cyan]🏥 Verifying Health[/bold cyan]\n")

        # Health check endpoints
        endpoints = [
            {"endpoint": "/health", "type": "Health Check", "timeout": "5s"},
            {"endpoint": "/api/status", "type": "API Status", "timeout": "10s"},
            {"endpoint": "/auth/verify", "type": "Auth Service", "timeout": "10s"},
            {"endpoint": "/static/app.js", "type": "Static Assets", "timeout": "5s"},
        ]

        # Service checks
        services = [
            {"service": "PostgreSQL", "port": 5432},
            {"service": "Redis Cache", "port": 6379},
            {"service": "Message Queue", "port": 5672},
        ]

        health_results = []

        # Check endpoints
        self.console.print("[bold]Checking Endpoints[/bold]")
        with Progress() as progress:
            task = progress.add_task("Checking endpoints", total=len(endpoints))

            for endpoint_info in endpoints:
                time.sleep(random.uniform(0.3, 0.8))

                # Simulate health check (95% success)
                if random.random() < 0.95:
                    status_code = 200
                    response_time = random.randint(10, 150)
                    health_status = "✓ Healthy"
                    severity = "success"
                else:
                    status_code = random.choice([500, 503, 504])
                    response_time = random.randint(1000, 5000)
                    health_status = "✖ Unhealthy"
                    severity = "error"
                    self.release_failed = True

                health_results.append(
                    {
                        "Endpoint": endpoint_info["endpoint"],
                        "Type": endpoint_info["type"],
                        "Status": status_code,
                        "Response Time": f"{response_time}ms",
                        "Health": health_status,
                        "Severity": severity,
                    }
                )

                progress.update(task, advance=1)

        # Check services
        self.console.print("\n[bold]Checking Services[/bold]")
        with Progress() as progress:
            task = progress.add_task("Checking services", total=len(services))

            for service_info in services:
                time.sleep(random.uniform(0.3, 0.8))

                # Simulate service check (98% success)
                if random.random() < 0.98:
                    health_status = "✓ Running"
                    severity = "success"
                else:
                    health_status = "✖ Down"
                    severity = "error"
                    self.release_failed = True

                health_results.append(
                    {
                        "Endpoint": service_info["service"],
                        "Type": "Service",
                        "Status": service_info["port"],
                        "Response Time": "N/A",
                        "Health": health_status,
                        "Severity": severity,
                    }
                )

                progress.update(task, advance=1)

        self.health_checks = health_results

        # Display health check results
        self.console.print("\n")
        with Section("Health Check Results") as section:
            health_table = Table(
                headers=["Endpoint/Service", "Type", "Status", "Response Time", "Health"]
            )

            for result in health_results:
                health_table.add_row(
                    result["Endpoint"],
                    result["Type"],
                    str(result["Status"]),
                    result["Response Time"],
                    result["Health"],
                    severity=result["Severity"],
                )

            section.add(health_table)

        unhealthy = sum(1 for r in health_results if "✖" in r["Health"])

        if unhealthy > 0:
            self.console.print(
                Alert.error(
                    f"{unhealthy} health checks failed",
                    details="Application may not be fully operational",
                )
            )
            return False
        else:
            self.console.print(Alert.success("All health checks passed"))
            return True

    def generate_release_summary(self):
        """Generate final release summary."""
        self.console.print("\n[bold cyan]📋 Release Summary[/bold cyan]\n")

        build_duration = time.time() - self.start_time

        # Release metadata
        release_metadata = {
            "Version": self.version,
            "Branch": self.branch,
            "Commit": self.commit[:7],
            "Released By": "release-bot",
            "Release Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Build Duration": f"{build_duration:.1f}s",
            "Status": "✓ Success" if not self.release_failed else "✖ Failed",
        }

        with Section("Release Metadata") as section:
            kv = KeyValue(release_metadata)
            section.add(kv)

        # Release statistics
        self.console.print()
        with Section("Release Statistics") as section:
            stats = {
                "Tests Executed": self.test_results.get("total", 0),
                "Test Pass Rate": f"{self.test_results.get('pass_rate', 0):.1f}%",
                "Deployment Targets": len(self.deployment_targets),
                "Successful Deployments": sum(
                    1 for t in self.deployment_targets if t["Status"] == "Deployed"
                ),
                "Health Checks": len(self.health_checks),
                "Warnings": len(self.warnings),
            }

            kv = KeyValue(stats)
            section.add(kv)

            # Show warnings
            if self.warnings:
                section.add_spacing()
                section.add_text("Warnings:", style="bold yellow")
                for warning in self.warnings[:5]:
                    section.add_text(f"  • {warning}", style="yellow")
                if len(self.warnings) > 5:
                    section.add_text(f"  ... and {len(self.warnings) - 5} more", style="dim")

        return not self.release_failed


def run_release(version: str, branch: str, commit: str):
    """Execute release orchestration."""
    console = get_console()

    console.print("[bold magenta]" + "═" * 60 + "[/bold magenta]")
    console.print(
        "[bold magenta]" + " " * 15 + "APP RELEASE ORCHESTRATOR" + " " * 15 + "[/bold magenta]"
    )
    console.print("[bold magenta]" + "═" * 60 + "[/bold magenta]\n")

    # Release information
    release_info = {
        "Version": version,
        "Branch": branch,
        "Commit": commit,
        "Environment": "production",
        "Strategy": "Rolling deployment",
    }

    with Section("Release Information") as section:
        kv = KeyValue(release_info)
        section.add(kv)

    # Initialize orchestrator
    orchestrator = ReleaseOrchestrator(version, branch, commit)
    orchestrator.start_time = time.time()

    # Release pipeline steps
    steps = [
        "Check environment",
        "Fetch release artifact",
        "Build application",
        "Run tests",
        "Deploy to targets",
        "Verify health",
        "Generate summary",
    ]

    console.print("\n")
    stepper = Stepper.from_list(steps, title="Release Pipeline")
    console.print(stepper)

    # Execute release pipeline
    try:
        # Step 1: Environment check
        stepper.start(0)
        if orchestrator.check_environment():
            stepper.complete(0)
        else:
            stepper.fail(0, "Environment prerequisites not met")
            console.print("\n")
            console.print(stepper)
            return False

        # Step 2: Fetch artifact
        stepper.start(1)
        if orchestrator.fetch_artifact():
            stepper.complete(1)
        else:
            stepper.fail(1, "Artifact download/extraction failed")
            console.print("\n")
            console.print(stepper)
            return False

        # Step 3: Build
        stepper.start(2)
        if orchestrator.build_application():
            stepper.complete(2)
        else:
            stepper.fail(2, "Build failed")
            console.print("\n")
            console.print(stepper)
            return False

        # Step 4: Tests
        stepper.start(3)
        if orchestrator.run_tests():
            stepper.complete(3)
        else:
            stepper.fail(3, "Tests failed")
            console.print("\n")
            console.print(stepper)
            return False

        # Step 5: Deploy
        stepper.start(4)
        if orchestrator.deploy_to_targets():
            stepper.complete(4)
        else:
            stepper.fail(4, "Deployment failed")
            console.print("\n")
            console.print(stepper)
            return False

        # Step 6: Health checks
        stepper.start(5)
        if orchestrator.verify_health():
            stepper.complete(5)
        else:
            stepper.fail(5, "Health checks failed")
            console.print("\n")
            console.print(stepper)
            return False

        # Step 7: Summary
        stepper.start(6)
        success = orchestrator.generate_release_summary()
        stepper.complete(6)

        # Final pipeline status
        console.print("\n")
        console.print(stepper)

        # Release notes
        console.print("\n")
        with Section("Release Notes") as section:
            section.add_text("📝 Changes in this release:", style="bold")
            section.add_text("  • Added new user dashboard", style="dim")
            section.add_text("  • Fixed authentication bug #1234", style="dim")
            section.add_text("  • Improved API response times by 20%", style="dim")
            section.add_text("  • Updated dependencies to latest versions", style="dim")

        # Final status
        console.print("\n")
        if success:
            console.print(
                Alert.success(
                    f"Release {version} completed successfully",
                    details="Application is live in production",
                )
            )
            return True
        else:
            console.print(
                Alert.error(
                    f"Release {version} failed", details="Review errors and retry deployment"
                )
            )
            return False

    except KeyboardInterrupt:
        console.print("\n")
        console.print(Alert.warning("Release interrupted by user"))
        return False


def run_live_release_dashboard(version: str):
    """Run live release monitoring dashboard."""
    console = get_console()

    console.print("[bold magenta]" + "═" * 60 + "[/bold magenta]")
    console.print(
        "[bold magenta]" + " " * 12 + "LIVE RELEASE DASHBOARD" + " " * 12 + "[/bold magenta]"
    )
    console.print("[bold magenta]" + "═" * 60 + "[/bold magenta]\n")

    console.print(f"[bold cyan]Monitoring release {version} deployment...[/bold cyan]")
    console.print("[dim]Live dashboard. Resize terminal to see responsive layout.[/dim]")
    console.print("[yellow]Press Ctrl+C to stop monitoring[/yellow]\n")

    time.sleep(2)

    # Simulate deployment state
    deployment_state = {
        "web-01": {"status": "deploying", "progress": 0, "health": "pending"},
        "web-02": {"status": "deploying", "progress": 0, "health": "pending"},
        "web-03": {"status": "pending", "progress": 0, "health": "pending"},
        "api-01": {"status": "pending", "progress": 0, "health": "pending"},
        "api-02": {"status": "pending", "progress": 0, "health": "pending"},
        "worker-01": {"status": "pending", "progress": 0, "health": "pending"},
    }

    # Create dashboard
    dashboard = Dashboard.create("sidebar_left")

    # Header
    def update_header():
        return Panel(
            f"[bold cyan]Release {version} Deployment Dashboard[/bold cyan] - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            border_style="cyan",
        )

    dashboard.set_header(Text(""), update_fn=update_header)

    # Sidebar with quick stats
    def update_sidebar():
        deploying = sum(1 for s in deployment_state.values() if s["status"] == "deploying")
        completed = sum(1 for s in deployment_state.values() if s["status"] == "completed")
        healthy = sum(1 for s in deployment_state.values() if s["health"] == "healthy")

        kv = KeyValue(title="Deployment Stats")
        kv.add("Total Targets", str(len(deployment_state)))
        kv.add("Deploying", str(deploying))
        kv.add("Completed", str(completed))
        kv.add("Healthy", str(healthy))
        kv.add("Version", version)

        return Panel(kv, border_style="green")

    dashboard.set_sidebar(Text(""), update_fn=update_sidebar)

    # Main content with deployment table
    def update_main():
        # Simulate deployment progress
        for _, state in deployment_state.items():
            if state["status"] == "deploying":
                state["progress"] = min(100, state["progress"] + random.randint(5, 15))
                if state["progress"] >= 100:
                    state["status"] = "completed"
                    state["health"] = "healthy" if random.random() < 0.95 else "unhealthy"
            elif state["status"] == "pending":
                # Start next pending deployment
                if random.random() < 0.3:
                    state["status"] = "deploying"

        table = Table(
            headers=["Target", "Status", "Progress", "Health"],
            show_lines=True,
        )

        for target, state in deployment_state.items():
            status_emoji = {
                "pending": "",
                "deploying": "",
                "completed": "✓",
                "failed": "✖",
            }

            progress_str = (
                f"{state['progress']}%"
                if state["status"] == "deploying"
                else ("100%" if state["status"] == "completed" else "-")
            )

            severity = (
                "success"
                if state["status"] == "completed" and state["health"] == "healthy"
                else "warning"
                if state["status"] == "deploying"
                else "error"
                if state["health"] == "unhealthy"
                else None
            )

            table.add_row(
                target,
                f"{status_emoji.get(state['status'], '?')} {state['status']}",
                progress_str,
                state["health"],
                severity=severity,
            )

        return Panel(table, title="Deployment Status", border_style="green")

    dashboard.set_main(update_fn=update_main)

    # Footer
    def update_footer():
        all_completed = all(s["status"] == "completed" for s in deployment_state.values())
        all_healthy = all(
            s["health"] == "healthy"
            for s in deployment_state.values()
            if s["status"] == "completed"
        )

        if all_completed and all_healthy:
            status = "[green]All deployments completed successfully[/green]"
        elif all_completed:
            status = "[yellow]Deployments completed with issues[/yellow]"
        else:
            status = "[cyan]Deployment in progress...[/cyan]"

        return Panel(
            f"[dim]Status: {status} | Last updated: {datetime.now().strftime('%H:%M:%S')} | Press Ctrl+C to exit[/dim]",
            border_style="blue",
        )

    dashboard.set_footer(Text(""), update_fn=update_footer)

    # Run the dashboard
    try:
        dashboard.run(refresh_per_second=2)
    except KeyboardInterrupt:
        console.print("\n[green]✓[/green] Dashboard stopped\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="App Release Orchestrator - Complete release workflow automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                               Run complete release workflow (default)
  %(prog)s --live                        Monitor release with live dashboard
  %(prog)s --version 2.5.0               Release specific version
  %(prog)s --branch hotfix --commit abc  Release from hotfix branch

The live mode shows real-time deployment progress across all targets.
        """,
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Monitor release with live dashboard (responsive to terminal resize)",
    )
    parser.add_argument(
        "--version",
        default="2.4.0",
        help="Version to release (default: 2.4.0)",
    )
    parser.add_argument(
        "--branch",
        default="main",
        help="Branch to release from (default: main)",
    )
    parser.add_argument(
        "--commit",
        default="a7f9c2d1e3b",
        help="Commit hash (default: a7f9c2d1e3b)",
    )

    args = parser.parse_args()

    if args.live:
        run_live_release_dashboard(args.version)
    else:
        success = run_release(args.version, args.branch, args.commit)
        sys.exit(0 if success else 1)
