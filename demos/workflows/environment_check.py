import platform
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


class EnvironmentDoctor:
    """Development environment health checker."""

    def __init__(self):
        self.console = get_console()
        self.logger = setup_logging(level="INFO")
        self.checks_passed = []
        self.checks_failed = []
        self.warnings = []
        self.recommendations = []

    def check_system_info(self):
        """Check system information."""
        self.console.print("\n[bold cyan]💻 System Information[/bold cyan]\n")

        with Spinner("Gathering system information...") as spinner:
            time.sleep(1)

            system_info = {
                "OS": platform.system(),
                "OS Version": platform.version(),
                "Architecture": platform.machine(),
                "Hostname": platform.node(),
                "Processor": platform.processor() or "Unknown",
            }

            spinner.success("System information collected")

        with Section("System Details") as section:
            kv = KeyValue(system_info)
            section.add(kv)

        # Verify OS is supported
        if platform.system() in ["Darwin", "Linux", "Windows"]:
            self.checks_passed.append("Operating system is supported")
            self.console.print(Alert.success("Operating system check passed"))
        else:
            self.checks_failed.append("Unsupported operating system")
            self.console.print(Alert.error("Operating system not supported"))

        return True

    def check_python_installation(self):
        """Check Python installation."""
        self.console.print("\n[bold cyan]🐍 Python Installation[/bold cyan]\n")

        python_checks = []

        with Spinner("Checking Python installation...") as spinner:
            time.sleep(1)

            python_version = platform.python_version()
            python_impl = platform.python_implementation()

            spinner.success("Python installation found")

        python_info = {
            "Python Version": python_version,
            "Implementation": python_impl,
            "Compiler": platform.python_compiler(),
            "Build": " ".join(platform.python_build()),
        }

        with Section("Python Details") as section:
            kv = KeyValue(python_info)
            section.add(kv)

        # Check Python version (require 3.8+)
        major, minor, _ = python_version.split(".")
        if int(major) >= 3 and int(minor) >= 8:
            python_checks.append(
                {
                    "Check": "Python version >= 3.8",
                    "Result": "✓ Passed",
                    "Details": python_version,
                }
            )
            self.checks_passed.append(f"Python {python_version} installed")
        else:
            python_checks.append(
                {
                    "Check": "Python version >= 3.8",
                    "Result": "✖ Failed",
                    "Details": python_version,
                }
            )
            self.checks_failed.append(f"Python version {python_version} is too old")
            self.recommendations.append("Upgrade Python to version 3.8 or higher")

        # Check pip
        with Spinner("Checking pip...") as spinner:
            time.sleep(0.5)
            pip_available = random.random() < 0.98

            if pip_available:
                spinner.success("pip is available")
                python_checks.append(
                    {
                        "Check": "pip package manager",
                        "Result": "✓ Passed",
                        "Details": "pip 23.3.1",
                    }
                )
                self.checks_passed.append("pip is installed")
            else:
                spinner.error("pip not found")
                python_checks.append(
                    {
                        "Check": "pip package manager",
                        "Result": "✖ Failed",
                        "Details": "Not found",
                    }
                )
                self.checks_failed.append("pip is not installed")
                self.recommendations.append("Install pip: python -m ensurepip")

        # Display checks
        checks_table = Table.from_list_of_dicts(python_checks)
        self.console.print(checks_table)

        return True

    def check_disk_space(self):
        """Check available disk space."""
        self.console.print("\n[bold cyan]💾 Disk Space[/bold cyan]\n")

        with Spinner("Checking disk space...") as spinner:
            time.sleep(1)

            # Simulate disk space check
            total_gb = random.randint(100, 1000)
            used_gb = random.randint(50, int(total_gb * 0.85))
            available_gb = total_gb - used_gb
            used_percent = (used_gb / total_gb) * 100

            spinner.success("Disk space checked")

        disk_info = {
            "Total Space": f"{total_gb} GB",
            "Used Space": f"{used_gb} GB ({used_percent:.1f}%)",
            "Available Space": f"{available_gb} GB",
            "Mount Point": "/",
        }

        with Section("Disk Space Details") as section:
            kv = KeyValue(disk_info)
            section.add(kv)

        # Check if sufficient space (require 10GB available)
        if available_gb >= 10:
            self.checks_passed.append(f"Sufficient disk space: {available_gb} GB available")
            self.console.print(Alert.success(f"Sufficient disk space available: {available_gb} GB"))
        elif available_gb >= 5:
            self.warnings.append(f"Low disk space: only {available_gb} GB available")
            self.recommendations.append("Free up disk space - recommend at least 10 GB")
            self.console.print(
                Alert.warning(
                    "Low disk space",
                    details=f"Only {available_gb} GB available, recommend 10+ GB",
                )
            )
        else:
            self.checks_failed.append(f"Insufficient disk space: only {available_gb} GB")
            self.recommendations.append("Critical: Free up disk space immediately")
            self.console.print(
                Alert.error(
                    "Insufficient disk space",
                    details=f"Only {available_gb} GB available, need at least 10 GB",
                )
            )

        return True

    def check_development_tools(self):
        """Check required development tools."""
        self.console.print("\n[bold cyan]Development Tools[/bold cyan]\n")

        tools = [
            {"name": "git", "required": True, "min_version": "2.0.0"},
            {"name": "docker", "required": True, "min_version": "20.0.0"},
            {"name": "poetry", "required": False, "min_version": "1.0.0"},
            {"name": "node", "required": False, "min_version": "18.0.0"},
            {"name": "npm", "required": False, "min_version": "9.0.0"},
            {"name": "make", "required": False, "min_version": "4.0"},
        ]

        tool_results = []

        with Progress() as progress:
            task = progress.add_task("Checking tools", total=len(tools))

            for tool in tools:
                time.sleep(0.5)

                # Simulate tool check (90% installed)
                is_installed = random.random() < 0.9

                if is_installed:
                    # Simulate version
                    major = random.randint(2, 5)
                    minor = random.randint(0, 20)
                    patch = random.randint(0, 10)
                    version = f"{major}.{minor}.{patch}"
                    status = "✓ Installed"
                    severity = "success"

                    self.checks_passed.append(f"{tool['name']} is installed")
                else:
                    version = "Not found"
                    status = "✖ Missing"
                    severity = "error" if tool["required"] else "warning"

                    if tool["required"]:
                        self.checks_failed.append(f"{tool['name']} is not installed")
                        self.recommendations.append(
                            f"Install {tool['name']} - it is required for development"
                        )
                    else:
                        self.warnings.append(f"{tool['name']} is not installed")
                        self.recommendations.append(
                            f"Install {tool['name']} (optional but recommended)"
                        )

                tool_results.append(
                    {
                        "Tool": tool["name"],
                        "Required": "Yes" if tool["required"] else "No",
                        "Version": version,
                        "Status": status,
                        "Severity": severity,
                    }
                )

                progress.update(task, advance=1)

        # Display tool check results
        with Section("Tool Check Results") as section:
            tools_table = Table(headers=["Tool", "Required", "Version", "Status"])

            for result in tool_results:
                tools_table.add_row(
                    result["Tool"],
                    result["Required"],
                    result["Version"],
                    result["Status"],
                    severity=result["Severity"],
                )

            section.add(tools_table)

        return True

    def generate_diagnostic_report(self):
        """Generate diagnostic report."""
        self.console.print("\n[bold cyan]📋 Diagnostic Report[/bold cyan]\n")

        with Spinner("Generating diagnostic report...") as spinner:
            time.sleep(1)
            spinner.success("Report generated")

        # Calculate health score
        total_checks = len(self.checks_passed) + len(self.checks_failed)
        health_score = (len(self.checks_passed) / total_checks * 100) if total_checks > 0 else 0

        # Determine health status
        if health_score >= 90:
            health_status = "✓ Excellent"
            _health_color = "green"  # Not used in demo
        elif health_score >= 75:
            health_status = "⚠ Good"
            _health_color = "yellow"  # Not used in demo
        elif health_score >= 50:
            health_status = "⚠ Fair"
            _health_color = "yellow"  # Not used in demo
        else:
            health_status = "✖ Poor"
            _health_color = "red"  # Not used in demo

        with Section("Health Summary") as section:
            health_metrics = {
                "Overall Health": health_status,
                "Health Score": f"{health_score:.0f}%",
                "Checks Passed": len(self.checks_passed),
                "Checks Failed": len(self.checks_failed),
                "Warnings": len(self.warnings),
                "Recommendations": len(self.recommendations),
            }

            kv = KeyValue(health_metrics)
            section.add(kv)

            # Show failed checks
            if self.checks_failed:
                section.add_spacing()
                section.add_text("Failed Checks:", style="bold red")
                for check in self.checks_failed:
                    section.add_text(f"  ✖ {check}", style="red")

            # Show warnings
            if self.warnings:
                section.add_spacing()
                section.add_text("Warnings:", style="bold yellow")
                for warning in self.warnings[:5]:
                    section.add_text(f"  ⚠ {warning}", style="yellow")

        return health_status, health_score


def run_environment_doctor():
    """Execute environment health checks."""
    console = get_console()

    console.print("[bold magenta]═══════════════════════════════════════════════[/bold magenta]")
    console.print("[bold magenta]        Development Environment Doctor[/bold magenta]")
    console.print("[bold magenta]═══════════════════════════════════════════════[/bold magenta]\n")

    doctor = EnvironmentDoctor()

    # Diagnostic steps
    steps = [
        "Check system information",
        "Check Python installation",
        "Check disk space",
        "Check development tools",
        "Generate diagnostic report",
    ]

    stepper = Stepper.from_list(steps, title="Diagnostic Process")
    console.print(stepper)

    # Execute diagnostics
    start_time = time.time()

    # Step 1: System info
    stepper.start(0)
    doctor.check_system_info()
    stepper.complete(0)

    # Step 2: Python
    stepper.start(1)
    doctor.check_python_installation()
    stepper.complete(1)

    # Step 3: Disk space
    stepper.start(2)
    doctor.check_disk_space()
    stepper.complete(2)

    # Step 4: Development tools
    stepper.start(3)
    doctor.check_development_tools()
    stepper.complete(3)

    # Step 5: Report
    stepper.start(4)
    health_status, health_score = doctor.generate_diagnostic_report()
    stepper.complete(4)

    _diagnostic_time = time.time() - start_time  # Not displayed in demo

    # Final summary
    console.print("\n")
    console.print(stepper)

    # Recommendations
    if doctor.recommendations:
        console.print("\n")
        with Section("Recommendations") as section:
            section.add_text("Follow these steps to improve your environment:", style="bold")
            section.add_spacing()

            for i, rec in enumerate(doctor.recommendations, 1):
                section.add_text(f"{i}. {rec}", style="cyan")

    # Export diagnostic report
    console.print("\n")
    with Section("Diagnostic Report") as section:
        section.add_text("Full diagnostic report saved to:", style="bold")
        section.add_text("  • JSON: ./diagnostics/env-check.json", style="cyan")
        section.add_text("  • HTML: ./diagnostics/env-check.html", style="cyan")
        section.add_text("  • Text: ./diagnostics/env-check.txt", style="cyan")

    # Final status
    console.print("\n")
    if health_score >= 90:
        console.print(
            Alert.success(
                "Environment is healthy",
                details="Your development environment meets all requirements",
            )
        )
    elif health_score >= 50:
        console.print(
            Alert.warning(
                "Environment needs attention",
                details=f"Health score: {health_score:.0f}% - review recommendations",
            )
        )
    else:
        console.print(
            Alert.error(
                "Environment has critical issues",
                details=f"Health score: {health_score:.0f}% - fix failed checks",
            )
        )


if __name__ == "__main__":
    run_environment_doctor()
