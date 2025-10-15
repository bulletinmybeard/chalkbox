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


class CodeQualityPipeline:
    """Automated code quality check orchestrator."""

    def __init__(self):
        self.console = get_console()
        self.logger = setup_logging(level="INFO")
        self.lint_issues = []
        self.failed_tests = []
        self.coverage_data = {}
        self.quality_gates_passed = True

    def run_linting(self):
        """Run linting checks on codebase."""
        self.console.print("\n[bold cyan]🔍 Running Linting Checks[/bold cyan]\n")

        # Linting tools to run
        linters = [
            {"name": "ruff", "description": "Fast Python linter", "files": 45},
            {"name": "flake8", "description": "Style guide enforcement", "files": 45},
            {"name": "mypy", "description": "Static type checking", "files": 45},
            {"name": "black", "description": "Code formatting check", "files": 45},
        ]

        all_issues = []

        for linter in linters:
            self.console.print(f"[bold]Running {linter['name']}...[/bold]")

            with Progress() as progress:
                task = progress.add_task(
                    f"Checking files with {linter['name']}", total=linter["files"]
                )

                for i in range(linter["files"]):
                    time.sleep(random.uniform(0.02, 0.05))

                    # Simulate finding issues (20% chance per file)
                    if random.random() < 0.2:
                        issue_types = [
                            "line too long",
                            "unused import",
                            "missing type annotation",
                            "undefined variable",
                            "inconsistent formatting",
                        ]

                        all_issues.append(
                            {
                                "Tool": linter["name"],
                                "File": f"src/module_{i % 10}.py",
                                "Line": random.randint(1, 500),
                                "Issue": random.choice(issue_types),
                                "Severity": random.choice(["error", "warning", "info"]),
                            }
                        )

                    progress.update(task, advance=1)

            self.console.print()

        # Categorize issues
        errors = [i for i in all_issues if i["Severity"] == "error"]
        warnings = [i for i in all_issues if i["Severity"] == "warning"]
        info = [i for i in all_issues if i["Severity"] == "info"]

        self.lint_issues = all_issues

        # Display results
        with Section("Linting Results Summary") as section:
            summary = {
                "Total Files Checked": sum(linter["files"] for linter in linters),
                "Total Issues": len(all_issues),
                "Errors": len(errors),
                "Warnings": len(warnings),
                "Info": len(info),
            }

            kv = KeyValue(summary)
            section.add(kv)

            # Show top issues
            if all_issues:
                section.add_spacing()
                section.add_text("Top Issues:", style="bold")

                issues_table = Table(headers=["Tool", "File", "Line", "Issue", "Severity"])

                for issue in all_issues[:10]:
                    severity_map = {
                        "error": "error",
                        "warning": "warning",
                        "info": "success",
                    }
                    issues_table.add_row(
                        issue["Tool"],
                        issue["File"],
                        str(issue["Line"]),
                        issue["Issue"],
                        issue["Severity"].upper(),
                        severity=severity_map[issue["Severity"]],
                    )

                section.add(issues_table)

                if len(all_issues) > 10:
                    section.add_text(f"... and {len(all_issues) - 10} more issues", style="dim")

        # Quality gate check
        if len(errors) > 0:
            self.quality_gates_passed = False
            self.console.print(
                Alert.error(
                    "Linting failed",
                    details=f"Found {len(errors)} errors that must be fixed",
                )
            )
        elif len(warnings) > 5:
            self.console.print(
                Alert.warning(
                    "Linting passed with warnings",
                    details=f"Found {len(warnings)} warnings to review",
                )
            )
        else:
            self.console.print(Alert.success("Linting passed"))

        self.logger.info(f"Linting complete: {len(errors)} errors, {len(warnings)} warnings")

        return len(errors) == 0

    def run_tests(self):
        """Run unit test suite."""
        self.console.print("\n[bold cyan]🧪 Running Test Suite[/bold cyan]\n")

        # Test suites
        test_suites = [
            {"name": "Unit Tests", "path": "tests/unit", "count": 35},
            {"name": "Integration Tests", "path": "tests/integration", "count": 18},
            {"name": "API Tests", "path": "tests/api", "count": 12},
            {"name": "Database Tests", "path": "tests/database", "count": 8},
        ]

        total_tests = sum(suite["count"] for suite in test_suites)
        test_results = {
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "xfailed": 0,
        }

        with Progress() as progress:
            overall_task = progress.add_task("Running all tests", total=total_tests)

            for suite in test_suites:
                suite_task = progress.add_task(f"Running {suite['name']}", total=suite["count"])

                for i in range(suite["count"]):
                    time.sleep(random.uniform(0.05, 0.15))

                    # Simulate test results (85% pass rate)
                    result = random.random()

                    if result < 0.85:
                        test_results["passed"] += 1
                    elif result < 0.92:
                        test_results["failed"] += 1
                        self.failed_tests.append(
                            {
                                "Suite": suite["name"],
                                "Test": f"test_{suite['path'].split('/')[-1]}_{i}",
                                "Reason": random.choice(
                                    [
                                        "AssertionError: expected 200, got 404",
                                        "ValueError: invalid input data",
                                        "TimeoutError: operation exceeded 30s",
                                        "TypeError: expected str, got int",
                                    ]
                                ),
                                "Duration": f"{random.uniform(0.1, 5):.2f}s",
                            }
                        )
                    elif result < 0.97:
                        test_results["skipped"] += 1
                    else:
                        test_results["xfailed"] += 1

                    progress.update(suite_task, advance=1)
                    progress.update(overall_task, advance=1)

                progress.remove_task(suite_task)

        # Display results
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

            results_table.add_row(
                "Expected Fail ⚠",
                str(test_results["xfailed"]),
                f"{test_results['xfailed']/total_tests*100:.1f}%",
                severity="warning",
            )

            section.add(results_table)

            # Show failed tests
            if self.failed_tests:
                section.add_spacing()
                section.add_text("Failed Tests:", style="bold red")

                failed_table = Table(
                    headers=["Suite", "Test", "Reason", "Duration"],
                    show_lines=True,
                )

                for test in self.failed_tests[:5]:
                    failed_table.add_row(
                        test["Suite"],
                        test["Test"],
                        test["Reason"],
                        test["Duration"],
                        severity="error",
                    )

                section.add(failed_table)

                if len(self.failed_tests) > 5:
                    section.add_text(
                        f"... and {len(self.failed_tests) - 5} more failures",
                        style="dim red",
                    )

        # Quality gate check
        fail_threshold = 3
        if test_results["failed"] > fail_threshold:
            self.quality_gates_passed = False
            self.console.print(
                Alert.error(
                    "Test suite failed",
                    details=f"{test_results['failed']} tests failed (threshold: {fail_threshold})",
                )
            )
        elif test_results["failed"] > 0:
            self.console.print(
                Alert.warning(
                    "Test suite passed with failures",
                    details=f"{test_results['failed']} tests failed but within threshold",
                )
            )
        else:
            self.console.print(Alert.success("All tests passed"))

        self.logger.info(
            f"Tests complete: {test_results['passed']} passed, " f"{test_results['failed']} failed"
        )

        return test_results["failed"] <= fail_threshold

    def generate_coverage_report(self):
        """Generate code coverage report."""
        self.console.print("\n[bold cyan]Generating Coverage Report[/bold cyan]\n")

        with Spinner("Analyzing code coverage...") as spinner:
            time.sleep(2)
            spinner.success("Coverage analysis complete")

        # Simulate coverage data
        modules = [
            {"Module": "src/core/engine.py", "Lines": 245, "Covered": random.randint(180, 240)},
            {"Module": "src/api/routes.py", "Lines": 180, "Covered": random.randint(150, 180)},
            {"Module": "src/utils/helpers.py", "Lines": 120, "Covered": random.randint(90, 120)},
            {"Module": "src/db/models.py", "Lines": 310, "Covered": random.randint(250, 310)},
            {"Module": "src/services/auth.py", "Lines": 95, "Covered": random.randint(70, 95)},
            {"Module": "src/services/cache.py", "Lines": 75, "Covered": random.randint(50, 75)},
        ]

        for module in modules:
            module["Coverage"] = f"{module['Covered']/module['Lines']*100:.1f}%"
            module["Missing"] = module["Lines"] - module["Covered"]

        total_lines = sum(m["Lines"] for m in modules)
        total_covered = sum(m["Covered"] for m in modules)
        overall_coverage = total_covered / total_lines * 100

        self.coverage_data = {
            "total_lines": total_lines,
            "covered_lines": total_covered,
            "coverage_percent": overall_coverage,
        }

        # Display coverage report
        with Section("Coverage Report", subtitle="By Module") as section:
            coverage_table = Table(headers=["Module", "Lines", "Covered", "Missing", "Coverage"])

            for module in modules:
                coverage_pct = float(module["Coverage"].rstrip("%"))
                severity = (
                    "success"
                    if coverage_pct >= 80
                    else "warning"
                    if coverage_pct >= 60
                    else "error"
                )

                coverage_table.add_row(
                    module["Module"],
                    str(module["Lines"]),
                    str(module["Covered"]),
                    str(module["Missing"]),
                    module["Coverage"],
                    severity=severity,
                )

            section.add(coverage_table)

            section.add_spacing()

            # Overall stats
            overall_stats = {
                "Total Lines": total_lines,
                "Covered Lines": total_covered,
                "Coverage": f"{overall_coverage:.1f}%",
                "Status": "✓ Passed"
                if overall_coverage >= 80
                else "⚠ Warning"
                if overall_coverage >= 60
                else "✖ Failed",
            }

            kv = KeyValue(overall_stats)
            section.add(kv)

        # Quality gate check
        coverage_threshold = 80
        if overall_coverage < coverage_threshold:
            self.quality_gates_passed = False
            self.console.print(
                Alert.error(
                    "Coverage below threshold",
                    details=f"Coverage is {overall_coverage:.1f}% (threshold: {coverage_threshold}%)",
                )
            )
        elif overall_coverage < 85:
            self.console.print(
                Alert.warning(
                    "Coverage passed but could be improved",
                    details=f"Coverage is {overall_coverage:.1f}%",
                )
            )
        else:
            self.console.print(Alert.success(f"Excellent coverage: {overall_coverage:.1f}%"))

        self.logger.info(f"Coverage: {overall_coverage:.1f}%")

        return overall_coverage >= coverage_threshold


def run_quality_pipeline():
    """Execute code quality pipeline."""
    console = get_console()

    console.print("[bold magenta]═══════════════════════════════════════════════[/bold magenta]")
    console.print("[bold magenta]       Code Quality & Testing Pipeline[/bold magenta]")
    console.print("[bold magenta]═══════════════════════════════════════════════[/bold magenta]\n")

    pipeline = CodeQualityPipeline()

    # Pipeline configuration
    config = {
        "Repository": "main branch",
        "Commit": "abc123f",
        "Author": "developer@example.com",
        "Linters": "ruff, flake8, mypy, black",
        "Test Framework": "pytest",
        "Coverage Tool": "coverage.py",
    }

    with Section("Pipeline Configuration") as section:
        kv = KeyValue(config)
        section.add(kv)

    # Quality gates
    console.print("\n[bold cyan]Quality Gates[/bold cyan]\n")

    quality_gates = [
        {"Gate": "No linting errors", "Threshold": "0 errors", "Status": "Pending"},
        {"Gate": "Test pass rate", "Threshold": "> 95%", "Status": "Pending"},
        {"Gate": "Code coverage", "Threshold": "> 80%", "Status": "Pending"},
    ]

    gates_table = Table.from_list_of_dicts(quality_gates)
    console.print(gates_table)

    # Pipeline steps
    steps = [
        "Run linting checks",
        "Execute test suite",
        "Generate coverage report",
        "Evaluate quality gates",
        "Generate report",
    ]

    console.print("\n")
    stepper = Stepper.from_list(steps, title="Pipeline Steps")
    console.print(stepper)

    # Execute pipeline
    start_time = time.time()

    # Step 1: Linting
    stepper.start(0)
    lint_passed = pipeline.run_linting()
    if lint_passed:
        stepper.complete(0)
    else:
        stepper.complete(0)  # Complete with issues

    # Step 2: Tests
    stepper.start(1)
    tests_passed = pipeline.run_tests()
    if tests_passed:
        stepper.complete(1)
    else:
        stepper.complete(1)  # Complete with failures

    # Step 3: Coverage
    stepper.start(2)
    coverage_passed = pipeline.generate_coverage_report()
    if coverage_passed:
        stepper.complete(2)
    else:
        stepper.complete(2)  # Complete with low coverage

    # Step 4: Evaluate gates
    stepper.start(3)
    with Spinner("Evaluating quality gates...") as spinner:
        time.sleep(1)

        if pipeline.quality_gates_passed:
            spinner.success("All quality gates passed")
            stepper.complete(3)
        else:
            spinner.error("Some quality gates failed")
            stepper.fail(3, "Quality standards not met")

    # Step 5: Report
    stepper.start(4)
    with Spinner("Generating final report...") as spinner:
        time.sleep(1)
        spinner.success("Report generated")
    stepper.complete(4)

    pipeline_time = time.time() - start_time

    # Final summary
    console.print("\n")
    console.print(stepper)

    console.print("\n")
    with Section("Pipeline Summary", subtitle="Complete") as section:
        summary = {
            "Execution Time": f"{pipeline_time:.1f}s",
            "Linting Issues": len(pipeline.lint_issues),
            "Failed Tests": len(pipeline.failed_tests),
            "Code Coverage": f"{pipeline.coverage_data.get('coverage_percent', 0):.1f}%",
            "Quality Gates": "✓ Passed" if pipeline.quality_gates_passed else "✖ Failed",
            "Merge Ready": "Yes" if pipeline.quality_gates_passed else "No - Fix Required",
        }

        kv = KeyValue(summary)
        section.add(kv)

    # Recommendations
    if not pipeline.quality_gates_passed:
        console.print("\n")
        with Section("Required Actions") as section:
            section.add_text("Fix the following issues before merging:", style="bold red")

            if any(i["Severity"] == "error" for i in pipeline.lint_issues):
                section.add_text("  • Fix linting errors", style="red")

            if len(pipeline.failed_tests) > 3:
                section.add_text(f"  • Fix {len(pipeline.failed_tests)} failed tests", style="red")

            if pipeline.coverage_data.get("coverage_percent", 100) < 80:
                section.add_text("  • Increase code coverage to 80%+", style="red")

    # Final status
    console.print("\n")
    if pipeline.quality_gates_passed:
        console.print(
            Alert.success(
                "✓ Ready to merge",
                details="All quality gates passed - code meets standards",
            )
        )
    else:
        console.print(
            Alert.error(
                "✖ Not ready to merge",
                details="Quality gates failed - fix issues before merging",
            )
        )


if __name__ == "__main__":
    run_quality_pipeline()
