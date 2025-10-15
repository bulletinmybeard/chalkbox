from pathlib import Path
import random
import time

from chalkbox import (
    Alert,
    KeyValue,
    Progress,
    Section,
    Spinner,
    Table,
    get_console,
    setup_logging,
)


class LogAnalyzer:
    """Log file analyzer."""

    def __init__(self, log_directory: str):
        self.console = get_console()
        self.logger = setup_logging(level="INFO")
        self.log_directory = Path(log_directory)
        self.log_files = []
        self.error_counts = {}
        self.warning_counts = {}
        self.critical_issues = []
        self.total_entries = 0

    def scan_log_directory(self):
        """Scan directory for log files."""
        self.console.print("\n[bold cyan]📁 Scanning Log Directory[/bold cyan]\n")

        with Spinner("Scanning for log files...") as spinner:
            time.sleep(1)

            # Simulate finding log files
            self.log_files = [
                {"file": "app.log", "size": "15.3 MB", "lines": 125000},
                {"file": "error.log", "size": "3.2 MB", "lines": 28000},
                {"file": "access.log", "size": "45.8 MB", "lines": 450000},
                {"file": "debug.log", "size": "8.1 MB", "lines": 95000},
                {"file": "database.log", "size": "5.4 MB", "lines": 62000},
            ]

            spinner.success(f"Found {len(self.log_files)} log files")

        # Display log files
        with Section("Log Files Found") as section:
            files_table = Table.from_list_of_dicts(self.log_files)
            section.add(files_table)

            self.total_entries = sum(f["lines"] for f in self.log_files)
            section.add_spacing()
            section.add_text(f"Total log entries: {self.total_entries:,}", style="bold cyan")

        return True

    def parse_log_files(self):
        """Parse log files and extract errors/warnings."""
        self.console.print("\n[bold cyan]🔍 Parsing Log Files[/bold cyan]\n")

        error_types = [
            "ConnectionError",
            "TimeoutError",
            "ValueError",
            "KeyError",
            "DatabaseError",
            "AuthenticationError",
            "FileNotFoundError",
            "PermissionError",
            "MemoryError",
        ]

        warning_types = [
            "DeprecationWarning",
            "ResourceWarning",
            "UserWarning",
            "PerformanceWarning",
            "ConfigWarning",
        ]

        with Progress() as progress:
            overall_task = progress.add_task("Parsing log files", total=len(self.log_files))

            for log_file in self.log_files:
                file_task = progress.add_task(
                    f"Parsing {log_file['file']}", total=log_file["lines"]
                )

                # Simulate parsing with batches
                batch_size = 10000
                processed = 0

                while processed < log_file["lines"]:
                    batch = min(batch_size, log_file["lines"] - processed)

                    # Simulate finding errors/warnings
                    time.sleep(0.1)

                    # Random errors in this batch
                    for _ in range(random.randint(0, 10)):
                        error_type = random.choice(error_types)
                        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1

                    # Random warnings
                    for _ in range(random.randint(0, 5)):
                        warning_type = random.choice(warning_types)
                        self.warning_counts[warning_type] = (
                            self.warning_counts.get(warning_type, 0) + 1
                        )

                    processed += batch
                    progress.update(file_task, advance=batch)

                progress.remove_task(file_task)
                progress.update(overall_task, advance=1)

        total_errors = sum(self.error_counts.values())
        total_warnings = sum(self.warning_counts.values())

        self.console.print(
            Alert.info(
                "Parsing complete",
                details=f"Found {total_errors} errors and {total_warnings} warnings",
            )
        )

        return True

    def analyze_error_patterns(self):
        """Analyze error patterns and frequencies."""
        self.console.print("\n[bold cyan]Analyzing Error Patterns[/bold cyan]\n")

        with Spinner("Analyzing error patterns...") as spinner:
            time.sleep(2)
            spinner.success("Analysis complete")

        # Sort errors by frequency
        sorted_errors = sorted(self.error_counts.items(), key=lambda x: x[1], reverse=True)

        # Display top errors
        with Section("Top Errors by Frequency") as section:
            if sorted_errors:
                error_table = Table(headers=["Error Type", "Count", "Percentage"])

                total_errors = sum(self.error_counts.values())

                for error_type, count in sorted_errors[:10]:
                    percentage = (count / total_errors * 100) if total_errors > 0 else 0

                    # Determine severity based on count
                    if count > 100:
                        severity = "error"
                    elif count > 50:
                        severity = "warning"
                    else:
                        severity = "success"

                    error_table.add_row(
                        error_type,
                        str(count),
                        f"{percentage:.1f}%",
                        severity=severity,
                    )

                section.add(error_table)

                # Mark critical issues
                for error_type, count in sorted_errors:
                    if count > 100:
                        self.critical_issues.append(f"{error_type}: {count} occurrences")
            else:
                section.add_text("No errors found", style="green")

        # Display warnings
        if self.warning_counts:
            self.console.print("\n")
            with Section("Warnings by Type") as section:
                sorted_warnings = sorted(
                    self.warning_counts.items(), key=lambda x: x[1], reverse=True
                )

                warning_table = Table(headers=["Warning Type", "Count"])

                for warning_type, count in sorted_warnings[:5]:
                    warning_table.add_row(warning_type, str(count), severity="warning")

                section.add(warning_table)

        return True

    def generate_health_status(self):
        """Generate system health status based on logs."""
        self.console.print("\n[bold cyan]🏥 Generating Health Status[/bold cyan]\n")

        with Spinner("Calculating health metrics...") as spinner:
            time.sleep(1)
            spinner.success("Health status calculated")

        total_errors = sum(self.error_counts.values())
        total_warnings = sum(self.warning_counts.values())

        # Calculate error rate (errors per 1000 log entries)
        error_rate = (total_errors / self.total_entries * 1000) if self.total_entries > 0 else 0

        # Determine health status
        if total_errors > 500 or error_rate > 5:
            health_status = "✖ Critical"
            _health_color = "red"  # Not used in demo
        elif total_errors > 200 or error_rate > 2:
            health_status = "⚠ Warning"
            _health_color = "yellow"  # Not used in demo
        else:
            health_status = "✓ Healthy"
            _health_color = "green"  # Not used in demo

        with Section("System Health Status") as section:
            health_metrics = {
                "Overall Status": health_status,
                "Total Log Entries": f"{self.total_entries:,}",
                "Total Errors": total_errors,
                "Total Warnings": total_warnings,
                "Error Rate": f"{error_rate:.2f} per 1000 entries",
                "Critical Issues": len(self.critical_issues),
            }

            kv = KeyValue(health_metrics)
            section.add(kv)

            # Show critical issues
            if self.critical_issues:
                section.add_spacing()
                section.add_text("Critical Issues:", style="bold red")
                for issue in self.critical_issues[:5]:
                    section.add_text(f"  • {issue}", style="red")
                if len(self.critical_issues) > 5:
                    section.add_text(
                        f"  ... and {len(self.critical_issues) - 5} more", style="dim red"
                    )

        # Health status alert
        if health_status == "✖ Critical":
            self.console.print(
                Alert.error(
                    "System health is critical",
                    details=f"Error rate: {error_rate:.2f} per 1000 entries",
                )
            )
        elif health_status == "⚠ Warning":
            self.console.print(
                Alert.warning(
                    "System health needs attention",
                    details=f"Found {total_errors} errors and {total_warnings} warnings",
                )
            )
        else:
            self.console.print(Alert.success("System health is good"))

        return health_status, error_rate

    def generate_recommendations(self, health_status: str):
        """Generate recommendations based on analysis."""
        self.console.print("\n[bold cyan]Recommendations[/bold cyan]\n")

        recommendations = []

        # Based on health status
        if health_status == "✖ Critical":
            recommendations.extend(
                [
                    "🔴 Immediate action required",
                    "• Investigate and fix top 5 error types",
                    "• Review recent code changes",
                    "• Check infrastructure status",
                    "• Increase monitoring alerts",
                ]
            )
        elif health_status == "⚠ Warning":
            recommendations.extend(
                [
                    "🟡 Review and monitor closely",
                    "• Address high-frequency errors",
                    "• Update error handling",
                    "• Review recent deployments",
                ]
            )
        else:
            recommendations.extend(
                [
                    "🟢 System is healthy",
                    "• Continue regular monitoring",
                    "• Review logs periodically",
                ]
            )

        # Based on specific error types
        if "DatabaseError" in self.error_counts and self.error_counts["DatabaseError"] > 20:
            recommendations.append("• Check database connection pool settings")

        if "TimeoutError" in self.error_counts and self.error_counts["TimeoutError"] > 20:
            recommendations.append("• Review and optimize slow operations")

        if "MemoryError" in self.error_counts:
            recommendations.append("• Investigate memory leaks and increase memory limits")

        # General recommendations
        recommendations.extend(
            [
                "",
                "General best practices:",
                "• Set up automated log analysis",
                "• Configure alerting for critical errors",
                "• Archive old log files regularly",
                "• Implement log rotation",
            ]
        )

        with Section("Action Items") as section:
            for rec in recommendations:
                if rec.startswith("") or rec.startswith("") or rec.startswith(""):
                    section.add_text(rec, style="bold")
                elif rec.startswith("•"):
                    section.add_text(f"  {rec}", style="cyan")
                elif rec == "":
                    section.add_spacing()
                else:
                    section.add_text(rec, style="bold")


def run_log_analyzer():
    """Execute log analysis workflow."""
    console = get_console()

    console.print("[bold magenta]═══════════════════════════════════════════════[/bold magenta]")
    console.print("[bold magenta]              Log File Analyzer[/bold magenta]")
    console.print("[bold magenta]═══════════════════════════════════════════════[/bold magenta]\n")

    # Analysis configuration
    config = {
        "Log Directory": "/var/log/myapp",
        "Time Range": "Last 24 hours",
        "Analysis Mode": "Full scan",
        "Output Format": "Console + JSON",
    }

    with Section("Analysis Configuration") as section:
        kv = KeyValue(config)
        section.add(kv)

    # Initialize analyzer
    analyzer = LogAnalyzer(config["Log Directory"])

    # Execute analysis
    start_time = time.time()

    # Scan directory
    analyzer.scan_log_directory()

    # Parse logs
    analyzer.parse_log_files()

    # Analyze patterns
    analyzer.analyze_error_patterns()

    # Health status
    health_status, error_rate = analyzer.generate_health_status()

    # Recommendations
    analyzer.generate_recommendations(health_status)

    analysis_time = time.time() - start_time

    # Final summary
    console.print("\n")
    with Section("Analysis Summary", subtitle="Complete") as section:
        summary = {
            "Analysis Time": f"{analysis_time:.1f}s",
            "Files Analyzed": len(analyzer.log_files),
            "Total Entries": f"{analyzer.total_entries:,}",
            "Errors Found": sum(analyzer.error_counts.values()),
            "Warnings Found": sum(analyzer.warning_counts.values()),
            "Health Status": health_status,
        }

        kv = KeyValue(summary)
        section.add(kv)

    # Export options
    console.print("\n")
    with Section("Export Options") as section:
        section.add_text("Analysis results saved to:", style="bold")
        section.add_text("  • JSON: ./reports/log-analysis.json", style="cyan")
        section.add_text("  • CSV: ./reports/error-summary.csv", style="cyan")
        section.add_text("  • HTML: ./reports/log-analysis.html", style="cyan")

    # Final status
    console.print("\n")
    if health_status == "✖ Critical":
        console.print(
            Alert.error(
                "Log analysis complete - action required",
                details="Critical issues detected in logs",
            )
        )
    elif health_status == "⚠ Warning":
        console.print(
            Alert.warning(
                "Log analysis complete - review recommended",
                details="Some issues found in logs",
            )
        )
    else:
        console.print(
            Alert.success(
                "Log analysis complete - system healthy",
                details="No critical issues found",
            )
        )


if __name__ == "__main__":
    run_log_analyzer()
