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


class APITestRunner:
    """API integration test orchestrator."""

    def __init__(self, base_url: str):
        self.console = get_console()
        self.logger = setup_logging(level="INFO")
        self.base_url = base_url
        self.test_results = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
        }
        self.failed_tests = []
        self.performance_metrics = []

    def test_authentication(self):
        """Test authentication endpoints."""
        self.console.print("\n[bold cyan]🔐 Testing Authentication[/bold cyan]\n")

        auth_tests = [
            {"test": "POST /auth/register", "expected": 201},
            {"test": "POST /auth/login (valid)", "expected": 200},
            {"test": "POST /auth/login (invalid)", "expected": 401},
            {"test": "POST /auth/refresh-token", "expected": 200},
            {"test": "POST /auth/logout", "expected": 200},
            {"test": "GET /auth/verify-email", "expected": 200},
        ]

        auth_results = []

        for test in auth_tests:
            with Spinner(f"Running {test['test']}...") as spinner:
                time.sleep(random.uniform(0.3, 0.8))

                # Simulate test execution (90% pass rate)
                if random.random() < 0.9:
                    status = "✓ Passed"
                    actual = test["expected"]
                    response_time = random.randint(50, 300)
                    spinner.success(f"{test['test']} passed")
                    self.test_results["passed"] += 1
                else:
                    status = "✖ Failed"
                    actual = random.choice([400, 500, 503])
                    response_time = random.randint(100, 5000)
                    spinner.error(f"{test['test']} failed")
                    self.test_results["failed"] += 1
                    self.failed_tests.append(test["test"])

                self.test_results["total"] += 1

                auth_results.append(
                    {
                        "Test": test["test"],
                        "Expected": test["expected"],
                        "Actual": actual,
                        "Time (ms)": response_time,
                        "Status": status,
                    }
                )

                self.performance_metrics.append(
                    {
                        "endpoint": test["test"],
                        "response_time": response_time,
                    }
                )

        # Display results
        with Section("Authentication Tests") as section:
            results_table = Table.from_list_of_dicts(auth_results)
            section.add(results_table)

        return True

    def test_crud_operations(self):
        """Test CRUD operations on resources."""
        self.console.print("\n[bold cyan]📝 Testing CRUD Operations[/bold cyan]\n")

        crud_tests = [
            {"test": "GET /api/users", "method": "GET", "expected": 200},
            {"test": "GET /api/users/123", "method": "GET", "expected": 200},
            {"test": "POST /api/users", "method": "POST", "expected": 201},
            {"test": "PUT /api/users/123", "method": "PUT", "expected": 200},
            {"test": "PATCH /api/users/123", "method": "PATCH", "expected": 200},
            {"test": "DELETE /api/users/123", "method": "DELETE", "expected": 204},
            {"test": "GET /api/products", "method": "GET", "expected": 200},
            {"test": "POST /api/products", "method": "POST", "expected": 201},
            {"test": "GET /api/orders", "method": "GET", "expected": 200},
            {"test": "POST /api/orders", "method": "POST", "expected": 201},
        ]

        with Progress() as progress:
            task = progress.add_task("Running CRUD tests", total=len(crud_tests))

            for test in crud_tests:
                time.sleep(random.uniform(0.2, 0.5))

                # Simulate test execution (85% pass rate)
                if random.random() < 0.85:
                    self.test_results["passed"] += 1
                else:
                    self.test_results["failed"] += 1
                    self.failed_tests.append(test["test"])

                self.test_results["total"] += 1

                response_time = random.randint(50, 500)
                self.performance_metrics.append(
                    {
                        "endpoint": test["test"],
                        "response_time": response_time,
                    }
                )

                progress.update(task, advance=1)

        self.console.print(Alert.success(f"Completed {len(crud_tests)} CRUD operation tests"))

        return True

    def test_error_handling(self):
        """Test error handling scenarios."""
        self.console.print("\n[bold cyan]⚠  Testing Error Handling[/bold cyan]\n")

        error_tests = [
            {"test": "400 Bad Request", "endpoint": "/api/users", "error_code": 400},
            {"test": "401 Unauthorized", "endpoint": "/api/admin", "error_code": 401},
            {"test": "403 Forbidden", "endpoint": "/api/users/999", "error_code": 403},
            {"test": "404 Not Found", "endpoint": "/api/invalid", "error_code": 404},
            {"test": "422 Validation Error", "endpoint": "/api/users", "error_code": 422},
            {"test": "429 Rate Limit", "endpoint": "/api/data", "error_code": 429},
            {"test": "500 Server Error", "endpoint": "/api/crash", "error_code": 500},
            {"test": "503 Service Unavailable", "endpoint": "/api/health", "error_code": 503},
        ]

        error_results = []

        with Progress() as progress:
            task = progress.add_task("Testing error scenarios", total=len(error_tests))

            for test in error_tests:
                time.sleep(random.uniform(0.2, 0.5))

                # Check if error code is returned correctly
                actual_code = test["error_code"] if random.random() < 0.95 else 500

                has_error_message = random.random() < 0.98
                has_error_details = random.random() < 0.90

                passed = (
                    actual_code == test["error_code"] and has_error_message and has_error_details
                )

                if passed:
                    status = "✓ Passed"
                    self.test_results["passed"] += 1
                else:
                    status = "✖ Failed"
                    self.test_results["failed"] += 1
                    self.failed_tests.append(test["test"])

                self.test_results["total"] += 1

                error_results.append(
                    {
                        "Test": test["test"],
                        "Expected Code": test["error_code"],
                        "Actual Code": actual_code,
                        "Has Message": "✓" if has_error_message else "✖",
                        "Has Details": "✓" if has_error_details else "✖",
                        "Status": status,
                    }
                )

                progress.update(task, advance=1)

        # Display results
        with Section("Error Handling Tests") as section:
            results_table = Table.from_list_of_dicts(error_results)
            section.add(results_table)

        return True

    def test_response_schemas(self):
        """Test response schema validation."""
        self.console.print("\n[bold cyan]📋 Testing Response Schemas[/bold cyan]\n")

        schema_tests = [
            {"endpoint": "/api/users", "required_fields": ["id", "name", "email"]},
            {"endpoint": "/api/products", "required_fields": ["id", "name", "price"]},
            {"endpoint": "/api/orders", "required_fields": ["id", "user_id", "total"]},
        ]

        schema_results = []

        for test in schema_tests:
            with Spinner(f"Validating {test['endpoint']} schema...") as spinner:
                time.sleep(random.uniform(0.3, 0.7))

                # Check if all required fields are present
                missing_fields = []
                for field in test["required_fields"]:
                    if random.random() < 0.05:  # 5% chance of missing field
                        missing_fields.append(field)

                if missing_fields:
                    status = "✖ Failed"
                    spinner.error(f"Schema validation failed for {test['endpoint']}")
                    self.test_results["failed"] += 1
                    self.failed_tests.append(f"Schema: {test['endpoint']}")
                else:
                    status = "✓ Passed"
                    spinner.success(f"Schema validation passed for {test['endpoint']}")
                    self.test_results["passed"] += 1

                self.test_results["total"] += 1

                schema_results.append(
                    {
                        "Endpoint": test["endpoint"],
                        "Required Fields": ", ".join(test["required_fields"]),
                        "Missing": ", ".join(missing_fields) if missing_fields else "None",
                        "Status": status,
                    }
                )

        # Display results
        with Section("Schema Validation Results") as section:
            results_table = Table.from_list_of_dicts(schema_results)
            section.add(results_table)

        return True

    def test_performance(self):
        """Test API performance metrics."""
        self.console.print("\n[bold cyan]⚡ Testing Performance[/bold cyan]\n")

        # Calculate performance statistics
        if self.performance_metrics:
            avg_response_time = sum(m["response_time"] for m in self.performance_metrics) / len(
                self.performance_metrics
            )

            max_response_time = max(m["response_time"] for m in self.performance_metrics)

            min_response_time = min(m["response_time"] for m in self.performance_metrics)

            # Find slowest endpoints
            sorted_metrics = sorted(
                self.performance_metrics, key=lambda x: x["response_time"], reverse=True
            )

            slowest = sorted_metrics[:5]

            with Section("Performance Metrics") as section:
                perf_stats = {
                    "Total Requests": len(self.performance_metrics),
                    "Average Response Time": f"{avg_response_time:.0f} ms",
                    "Min Response Time": f"{min_response_time} ms",
                    "Max Response Time": f"{max_response_time} ms",
                    "Performance Status": "✓ Good"
                    if avg_response_time < 300
                    else "⚠ Slow"
                    if avg_response_time < 1000
                    else "✖ Poor",
                }

                kv = KeyValue(perf_stats)
                section.add(kv)

                section.add_spacing()
                section.add_text("Slowest Endpoints:", style="bold")

                slowest_table = Table(headers=["Endpoint", "Response Time (ms)"])
                for metric in slowest:
                    severity = (
                        "success"
                        if metric["response_time"] < 300
                        else "warning"
                        if metric["response_time"] < 1000
                        else "error"
                    )
                    slowest_table.add_row(
                        metric["endpoint"],
                        str(metric["response_time"]),
                        severity=severity,
                    )

                section.add(slowest_table)

            # Performance test verdict
            if avg_response_time > 1000:
                self.console.print(
                    Alert.error(
                        "Performance issues detected",
                        details=f"Average response time: {avg_response_time:.0f}ms (threshold: 1000ms)",
                    )
                )
            elif avg_response_time > 300:
                self.console.print(
                    Alert.warning(
                        "Performance could be improved",
                        details=f"Average response time: {avg_response_time:.0f}ms",
                    )
                )
            else:
                self.console.print(
                    Alert.success(f"Good performance: {avg_response_time:.0f}ms average")
                )

        return True


def run_api_tests():
    """Execute API integration tests."""
    console = get_console()

    console.print("[bold magenta]═══════════════════════════════════════════════[/bold magenta]")
    console.print("[bold magenta]         API Integration Test Suite[/bold magenta]")
    console.print("[bold magenta]═══════════════════════════════════════════════[/bold magenta]\n")

    # Test configuration
    test_config = {
        "API Base URL": "https://api.example.com",
        "Environment": "staging",
        "Test Framework": "pytest + httpx",
        "Authentication": "Bearer Token",
        "Timeout": "30 seconds",
    }

    with Section("Test Configuration") as section:
        kv = KeyValue(test_config)
        section.add(kv)

    # Initialize test runner
    runner = APITestRunner(test_config["API Base URL"])

    # Test steps
    steps = [
        "Test authentication flows",
        "Test CRUD operations",
        "Test error handling",
        "Test response schemas",
        "Test performance",
        "Generate test report",
    ]

    console.print("\n")
    stepper = Stepper.from_list(steps, title="Test Execution")
    console.print(stepper)

    # Execute tests
    start_time = time.time()

    # Step 1: Authentication
    stepper.start(0)
    runner.test_authentication()
    stepper.complete(0)

    # Step 2: CRUD
    stepper.start(1)
    runner.test_crud_operations()
    stepper.complete(1)

    # Step 3: Error handling
    stepper.start(2)
    runner.test_error_handling()
    stepper.complete(2)

    # Step 4: Schema validation
    stepper.start(3)
    runner.test_response_schemas()
    stepper.complete(3)

    # Step 5: Performance
    stepper.start(4)
    runner.test_performance()
    stepper.complete(4)

    # Step 6: Report
    stepper.start(5)
    with Spinner("Generating test report...") as spinner:
        time.sleep(1)
        spinner.success("Test report generated")
    stepper.complete(5)

    test_time = time.time() - start_time

    # Final summary
    console.print("\n")
    console.print(stepper)

    console.print("\n")
    with Section("Test Summary", subtitle="Complete") as section:
        pass_rate = (
            runner.test_results["passed"] / runner.test_results["total"] * 100
            if runner.test_results["total"] > 0
            else 0
        )

        summary = {
            "Total Tests": runner.test_results["total"],
            "Passed ✓": runner.test_results["passed"],
            "Failed ✖": runner.test_results["failed"],
            "Skipped": runner.test_results["skipped"],
            "Pass Rate": f"{pass_rate:.1f}%",
            "Execution Time": f"{test_time:.1f}s",
            "Status": "✓ Passed" if pass_rate >= 90 else "✖ Failed",
        }

        kv = KeyValue(summary)
        section.add(kv)

        # Show failed tests
        if runner.failed_tests:
            section.add_spacing()
            section.add_text("Failed Tests:", style="bold red")
            for test in runner.failed_tests[:10]:
                section.add_text(f"  • {test}", style="red")
            if len(runner.failed_tests) > 10:
                section.add_text(f"  ... and {len(runner.failed_tests) - 10} more", style="dim red")

    # Test report location
    console.print("\n")
    with Section("Test Report") as section:
        section.add_text("Full report available at:", style="bold")
        section.add_text("  • HTML: ./test-reports/api-tests.html", style="cyan")
        section.add_text("  • JSON: ./test-reports/api-tests.json", style="cyan")
        section.add_text("  • JUnit: ./test-reports/api-tests.xml", style="cyan")

    # Final status
    console.print("\n")
    if pass_rate >= 95:
        console.print(
            Alert.success(
                "API tests passed",
                details=f"All critical tests passed with {pass_rate:.1f}% success rate",
            )
        )
    elif pass_rate >= 90:
        console.print(
            Alert.warning(
                "API tests passed with warnings",
                details=f"Pass rate: {pass_rate:.1f}% - some tests failed",
            )
        )
    else:
        console.print(
            Alert.error(
                "API tests failed",
                details=f"Pass rate: {pass_rate:.1f}% - too many failures",
            )
        )


if __name__ == "__main__":
    run_api_tests()
