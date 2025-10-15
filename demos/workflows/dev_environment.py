import argparse
from datetime import datetime
import random
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


class DevEnvironment:
    """Local development environment manager."""

    def __init__(self):
        self.console = get_console()
        self.logger = setup_logging(level="INFO")
        self.services = {}
        self.env_vars = {}
        self.health_checks_passed = True

    def check_environment_variables(self):
        """Check required environment variables."""
        self.console.print("\n[bold cyan]🔑 Checking Environment Variables[/bold cyan]\n")

        required_vars = {
            "DATABASE_URL": "postgresql://localhost:5432/devdb",
            "REDIS_URL": "redis://localhost:6379",
            "API_KEY": "sk_dev_1234567890abcdef",
            "SECRET_KEY": "super_secret_dev_key_12345",
            "DEBUG": "true",
            "LOG_LEVEL": "INFO",
            "ALLOWED_HOSTS": "localhost,127.0.0.1",
        }

        self.env_vars = required_vars

        with Section("Environment Configuration") as section:
            kv = KeyValue(required_vars)
            section.add(kv)

        # Check for missing vars
        missing_vars = random.sample(list(required_vars.keys()), k=random.randint(0, 1))

        if missing_vars:
            self.console.print(
                Alert.warning(
                    "Some environment variables not set",
                    details=f"Using defaults for: {', '.join(missing_vars)}",
                )
            )
        else:
            self.console.print(Alert.success("All environment variables configured"))

        return True

    def start_docker_containers(self):
        """Start Docker containers via docker-compose."""
        self.console.print("\n[bold cyan]🐳 Starting Docker Containers[/bold cyan]\n")

        # Services to start
        services_config = [
            {
                "name": "postgres",
                "image": "postgres:15-alpine",
                "port": "5432:5432",
                "startup_time": 3,
            },
            {
                "name": "redis",
                "image": "redis:7-alpine",
                "port": "6379:6379",
                "startup_time": 2,
            },
            {
                "name": "api",
                "image": "app/api:dev",
                "port": "8000:8000",
                "startup_time": 4,
            },
            {
                "name": "nginx",
                "image": "nginx:alpine",
                "port": "80:80",
                "startup_time": 2,
            },
        ]

        # Show services table
        with Section("Services Configuration") as section:
            services_table = Table(headers=["Service", "Image", "Ports"])
            for service in services_config:
                services_table.add_row(service["name"], service["image"], service["port"])
            section.add(services_table)

        self.console.print()

        # Start each service
        with Progress() as progress:
            overall_task = progress.add_task("Starting services", total=len(services_config))

            for service in services_config:
                # Pulling image
                pull_task = progress.add_task(f"Pulling {service['image']}", total=100)
                for _ in range(100):
                    time.sleep(0.01)
                    progress.update(pull_task, advance=1)
                progress.remove_task(pull_task)

                # Starting container
                start_task = progress.add_task(f"Starting {service['name']}", total=100)
                for _ in range(100):
                    time.sleep(service["startup_time"] / 100)
                    progress.update(start_task, advance=1)
                progress.remove_task(start_task)

                # Store service info
                self.services[service["name"]] = {
                    "status": "running",
                    "port": service["port"].split(":")[0],
                    "health": "starting",
                }

                progress.update(overall_task, advance=1)

        self.console.print(Alert.success(f"Started {len(services_config)} containers"))

        return True

    def run_health_checks(self):
        """Run health checks on all services."""
        self.console.print("\n[bold cyan]🏥 Running Health Checks[/bold cyan]\n")

        health_results = []

        for service_name, service_info in self.services.items():
            with Spinner(f"Checking {service_name}...") as spinner:
                time.sleep(random.uniform(0.5, 1.5))

                # Simulate health check (90% success rate)
                if random.random() < 0.9:
                    health_status = "healthy"
                    response_time = f"{random.randint(5, 50)}ms"
                    spinner.success(f"{service_name} is healthy")
                else:
                    health_status = "unhealthy"
                    response_time = "timeout"
                    self.health_checks_passed = False
                    spinner.error(f"{service_name} is unhealthy")

                service_info["health"] = health_status

                health_results.append(
                    {
                        "Service": service_name,
                        "Port": service_info["port"],
                        "Status": service_info["status"],
                        "Health": health_status,
                        "Response Time": response_time,
                    }
                )

        # Display health check results
        with Section("Health Check Results") as section:
            # Create table with severity-based row styling
            health_table = Table(
                headers=["Service", "Port", "Status", "Health", "Response Time"],
                row_styles="severity",
            )

            for result in health_results:
                severity = "success" if result["Health"] == "healthy" else "error"
                health_table.add_row(
                    result["Service"],
                    result["Port"],
                    result["Status"],
                    result["Health"],
                    result["Response Time"],
                    severity=severity,
                )

            section.add(health_table)

        if not self.health_checks_passed:
            self.console.print(
                Alert.error(
                    "Some services are unhealthy",
                    details="Check service logs for details",
                )
            )
        else:
            self.console.print(Alert.success("All services are healthy"))

        return self.health_checks_passed

    def show_container_logs(self):
        """Simulate streaming container logs."""
        self.console.print("\n[bold cyan]📋 Recent Container Logs[/bold cyan]\n")

        log_entries = [
            "[postgres] database system is ready to accept connections",
            "[redis] Ready to accept connections",
            "[api] Starting development server at http://0.0.0.0:8000",
            "[api] Watching for file changes with StatReloader",
            "[nginx] nginx/1.25.0",
            "[postgres] checkpoint complete: wrote 150 buffers (0.9%)",
            "[api] GET /health/ HTTP/1.1 200 OK",
            "[redis] DB loaded from disk: 0.001 seconds",
        ]

        with Section("Container Logs", subtitle="Last 10 entries") as section:
            for entry in log_entries:
                # Color code by service
                if "postgres" in entry:
                    style = "blue"
                elif "redis" in entry:
                    style = "red"
                elif "api" in entry:
                    style = "green"
                elif "nginx" in entry:
                    style = "cyan"
                else:
                    style = "white"

                section.add_text(f"  {entry}", style=style)


def start_development_environment():
    """Start the development environment."""
    console = get_console()

    console.print("[bold magenta]═══════════════════════════════════════════════[/bold magenta]")
    console.print("[bold magenta]       Development Environment Startup[/bold magenta]")
    console.print("[bold magenta]═══════════════════════════════════════════════[/bold magenta]\n")

    env = DevEnvironment()

    # Startup steps
    steps = [
        "Check environment variables",
        "Start Docker containers",
        "Run health checks",
        "Display service dashboard",
    ]

    stepper = Stepper.from_list(steps, title="Startup Sequence")
    console.print(stepper)

    # Execute startup
    start_time = time.time()

    # Step 1: Environment variables
    stepper.start(0)
    env.check_environment_variables()
    stepper.complete(0)

    # Step 2: Docker containers
    stepper.start(1)
    env.start_docker_containers()
    stepper.complete(1)

    # Step 3: Health checks
    stepper.start(2)
    health_ok = env.run_health_checks()
    if health_ok:
        stepper.complete(2)
    else:
        stepper.complete(2)  # Complete with issues

    # Step 4: Logs
    stepper.start(3)
    env.show_container_logs()
    stepper.complete(3)

    startup_time = time.time() - start_time

    # Final summary
    console.print("\n")
    console.print(stepper)

    console.print("\n")
    with Section("Environment Summary", subtitle="Ready for Development") as section:
        summary = {
            "Status": "✓ Running" if health_ok else "⚠ Degraded",
            "Startup Time": f"{startup_time:.1f}s",
            "Services": len(env.services),
            "Healthy Services": sum(1 for s in env.services.values() if s["health"] == "healthy"),
        }

        kv = KeyValue(summary)
        section.add(kv)

    # Service URLs
    console.print("\n")
    with Section("Service URLs") as section:
        section.add_text("Your services are accessible at:", style="bold")
        section.add_spacing()

        urls = {
            "API": "http://localhost:8000",
            "API Docs": "http://localhost:8000/docs",
            "Database": "postgresql://localhost:5432/devdb",
            "Redis": "redis://localhost:6379",
            "Web": "http://localhost:80",
        }

        for service, url in urls.items():
            section.add_text(f"  • {service}: [cyan]{url}[/cyan]")

    # Next steps
    console.print("\n")
    with Section("Next Steps") as section:
        section.add_text("1. View logs:", style="bold")
        section.add_text("   docker-compose logs -f", style="dim cyan")
        section.add_spacing()

        section.add_text("2. Stop services:", style="bold")
        section.add_text("   docker-compose down", style="dim cyan")
        section.add_spacing()

        section.add_text("3. Restart a service:", style="bold")
        section.add_text("   docker-compose restart <service>", style="dim cyan")

    # Final status
    console.print("\n")
    if health_ok:
        console.print(
            Alert.success(
                "Development environment ready",
                details="All services started successfully",
            )
        )
    else:
        console.print(
            Alert.warning(
                "Development environment started with issues",
                details="Some services may not be fully operational",
            )
        )


def start_live_dashboard():
    """Start live monitoring dashboard."""
    console = get_console()

    console.print("[bold magenta]═══════════════════════════════════════════════[/bold magenta]")
    console.print("[bold magenta]       Live Service Dashboard[/bold magenta]")
    console.print("[bold magenta]═══════════════════════════════════════════════[/bold magenta]\n")

    console.print("[dim]Starting live dashboard. Resize terminal to see responsive layout.[/dim]")
    console.print("[yellow]Press Ctrl+C to stop[/yellow]\n")

    time.sleep(2)

    # Initialize services state
    services_state = {
        "postgres": {"status": "running", "health": "healthy", "requests": 0},
        "redis": {"status": "running", "health": "healthy", "requests": 0},
        "api": {"status": "running", "health": "healthy", "requests": 0},
        "nginx": {"status": "running", "health": "healthy", "requests": 0},
    }

    # Create dashboard
    dashboard = Dashboard.create("sidebar_left")

    # Header
    def update_header():
        return Panel(
            f"[bold cyan]Development Services Dashboard[/bold cyan] - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            border_style="cyan",
        )

    dashboard.set_header(Text(""), update_fn=update_header)

    # Sidebar with quick stats
    def update_sidebar():
        running = sum(1 for s in services_state.values() if s["status"] == "running")
        healthy = sum(1 for s in services_state.values() if s["health"] == "healthy")
        total_requests = sum(s["requests"] for s in services_state.values())

        kv = KeyValue(title="Quick Stats")
        kv.add("Total Services", str(len(services_state)))
        kv.add("Running", str(running))
        kv.add("Healthy", str(healthy))
        kv.add("Total Requests", str(total_requests))

        return Panel(kv, border_style="green")

    dashboard.set_sidebar(Text(""), update_fn=update_sidebar)

    # Main content with service table
    def update_main():
        # Simulate some activity
        for service in services_state.values():
            service["requests"] += random.randint(0, 10)
            # Occasional health changes
            if random.random() < 0.05:
                service["health"] = random.choice(["healthy", "healthy", "healthy", "degraded"])

        table = Table(
            headers=["Service", "Status", "Health", "Port", "Requests"],
            show_lines=True,
        )

        service_ports = {"postgres": "5432", "redis": "6379", "api": "8000", "nginx": "80"}

        for service_name, service_data in services_state.items():
            severity = "success" if service_data["health"] == "healthy" else "warning"

            table.add_row(
                service_name,
                service_data["status"],
                service_data["health"],
                service_ports[service_name],
                str(service_data["requests"]),
                severity=severity,
            )

        return Panel(table, title="Service Status", border_style="green")

    dashboard.set_main(update_fn=update_main)

    # Footer
    def update_footer():
        all_healthy = all(s["health"] == "healthy" for s in services_state.values())
        status = (
            "[green]All systems operational[/green]"
            if all_healthy
            else "[yellow]Some services degraded[/yellow]"
        )

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
        description="Development Environment Startup - Start local dev services or monitor live",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s              Start development environment (default)
  %(prog)s --live       Start live monitoring dashboard

The live mode shows real-time service metrics with automatic terminal resize support.
        """,
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Start live monitoring dashboard (responsive to terminal resize)",
    )

    args = parser.parse_args()

    if args.live:
        start_live_dashboard()
    else:
        start_development_environment()
