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
)


class PackageInstaller:
    """Simulated package installer."""

    def __init__(self):
        self.console = get_console()
        self.installed_packages = []
        self.failed_packages = []

    @staticmethod
    def check_system_requirements():
        """Check system requirements."""
        requirements = {
            "OS": "macOS 12.0+",
            "Python": "3.8+",
            "Disk Space": "500 MB",
            "Memory": "2 GB",
            "Network": "Active",
        }

        with Section("System Requirements Check") as section:
            checks = []

            with Spinner("Checking system compatibility...") as spinner:
                for req, expected in requirements.items():
                    time.sleep(0.3)

                    # Simulate checks
                    if req == "OS":
                        actual = "macOS 14.5"
                        passed = True
                    elif req == "Python":
                        actual = "3.12.11"
                        passed = True
                    elif req == "Disk Space":
                        actual = "12.3 GB"
                        passed = True
                    elif req == "Memory":
                        actual = "16 GB"
                        passed = True
                    elif req == "Network":
                        actual = "Connected"
                        passed = random.random() < 0.95

                    checks.append(
                        {
                            "Requirement": req,
                            "Expected": expected,
                            "Actual": actual,
                            "Status": "✓ " if passed else "✖",
                        }
                    )

                all_passed = all(c["Status"] == "✓ " for c in checks)

                if all_passed:
                    spinner.success("All requirements met")
                else:
                    spinner.error("Some requirements not met")

            table = Table.from_list_of_dicts(checks)
            section.add(table)

        return all_passed

    def resolve_dependencies(self, packages):
        """Resolve package dependencies."""
        self.console.print("\n[bold cyan]Resolving Dependencies[/bold cyan]\n")

        dependency_tree = {}

        with Spinner("Analyzing package dependencies...") as spinner:
            for pkg in packages:
                time.sleep(0.5)

                # Simulate dependency resolution
                deps = []
                if pkg["name"] == "web-framework":
                    deps = ["http-client", "template-engine", "router"]
                elif pkg["name"] == "database-orm":
                    deps = ["connection-pool", "query-builder"]
                elif pkg["name"] == "api-server":
                    deps = ["web-framework", "auth-lib", "validator"]

                dependency_tree[pkg["name"]] = deps

            # Calculate total packages
            all_packages = set()
            for pkg in packages:
                all_packages.add(pkg["name"])
                all_packages.update(dependency_tree.get(pkg["name"], []))

            spinner.success(f"Resolved {len(all_packages)} total packages")

        # Show dependency tree
        with Section("Dependency Tree") as section:
            for pkg, deps in dependency_tree.items():
                if deps:
                    section.add_text(f"{pkg}", style="bold")
                    for dep in deps:
                        section.add_text(f"  └─ {dep}", style="dim")
                else:
                    section.add_text(f"{pkg} (no dependencies)", style="bold")

        return list(all_packages)

    def download_packages(self, package_list):
        """Download packages with progress tracking."""
        self.console.print("\n[bold cyan]Downloading Packages[/bold cyan]\n")

        download_stats = {"total_size": 0, "downloaded": 0, "speed": 0}

        with Progress() as progress:
            overall_task = progress.add_task("[cyan]Overall Progress", total=len(package_list))

            for pkg_name in package_list:
                # Simulate package size
                pkg_size = random.randint(1, 50) * 1024 * 1024  # 1-50 MB

                dl_task = progress.add_task(f"Downloading {pkg_name}", total=pkg_size)

                downloaded = 0
                while downloaded < pkg_size:
                    # Simulate download with variable speed
                    chunk_size = random.randint(100000, 500000)
                    chunk_size = min(chunk_size, pkg_size - downloaded)

                    time.sleep(0.01)
                    downloaded += chunk_size
                    download_stats["downloaded"] += chunk_size

                    progress.update(dl_task, advance=chunk_size)

                download_stats["total_size"] += pkg_size
                progress.update(overall_task, advance=1)
                progress.remove_task(dl_task)

        self.console.print(
            Alert.info(
                f"Downloaded {len(package_list)} packages",
                details=f"Total size: {download_stats['total_size'] / 1024 / 1024:.1f} MB",
            )
        )

        return True

    def install_package(self, pkg_name, stepper, step_idx):
        """Install a single package."""
        stepper.start(step_idx)

        with Spinner(f"Installing {pkg_name}...") as spinner:
            # Simulate installation steps
            steps = [
                "Extracting files",
                "Running pre-install scripts",
                "Copying files",
                "Running post-install scripts",
                "Updating registry",
            ]

            for step in steps:
                spinner.update(f"Installing {pkg_name}: {step}...")
                time.sleep(random.uniform(0.2, 0.5))

            # Simulate occasional failures
            if random.random() < 0.1:
                spinner.error(f"Failed to install {pkg_name}")
                stepper.fail(step_idx, "Installation script error")
                self.failed_packages.append(pkg_name)
                return False
            else:
                spinner.success(f"Installed {pkg_name}")
                stepper.complete(step_idx)
                self.installed_packages.append(pkg_name)
                return True

    def configure_packages(self):
        """Configure installed packages."""
        self.console.print("\n[bold cyan] Configuring Packages[/bold cyan]\n")

        configs = {}

        with Progress() as progress:
            task = progress.add_task("Applying configurations", total=len(self.installed_packages))

            for pkg in self.installed_packages:
                time.sleep(0.3)

                # Generate mock configuration
                configs[pkg] = {
                    "enabled": True,
                    "auto_start": random.choice([True, False]),
                    "log_level": random.choice(["info", "warning", "debug"]),
                    "port": random.randint(3000, 9000) if "server" in pkg else None,
                }

                progress.update(task, advance=1)

        # Show configuration summary
        with Section("Configuration Summary") as section:
            for pkg, config in list(configs.items())[:3]:  # Show first 3
                section.add_text(f"[bold]{pkg}[/bold]")

                # Filter out None values
                clean_config = {k: v for k, v in config.items() if v is not None}
                kv = KeyValue(clean_config)
                section.add(kv)
                section.add_spacing()

            if len(configs) > 3:
                section.add_text(
                    f"... and {len(configs) - 3} more packages configured", style="dim"
                )

        return configs


def run_installer():
    """Run the package installer."""
    console = get_console()

    console.print("[bold magenta]╔══════════════════════════════════════════╗[/bold magenta]")
    console.print("[bold magenta]║      Package Manager Installation        ║[/bold magenta]")
    console.print("[bold magenta]╚══════════════════════════════════════════╝[/bold magenta]\n")

    installer = PackageInstaller()

    # Packages to install
    packages = [
        {"name": "web-framework", "version": "2.1.0", "size": "12 MB"},
        {"name": "database-orm", "version": "1.5.3", "size": "8 MB"},
        {"name": "api-server", "version": "3.0.1", "size": "15 MB"},
        {"name": "cache-lib", "version": "1.2.0", "size": "3 MB"},
        {"name": "monitoring-agent", "version": "2.0.0", "size": "5 MB"},
    ]

    # Show packages to install
    with Section("Packages to Install") as section:
        table = Table.from_list_of_dicts(packages)
        section.add(table)

    # Check system requirements
    console.print("\n")
    if not installer.check_system_requirements():
        console.print(
            Alert.error(
                "System requirements not met",
                details="Please resolve the issues above and try again",
            )
        )
        return

    # Resolve dependencies
    all_packages = installer.resolve_dependencies(packages)

    # User confirmation
    console.print("\n")
    console.print(
        Alert.warning(
            f"This will install {len(all_packages)} packages", details="Including all dependencies"
        )
    )

    # Download packages
    if not installer.download_packages(all_packages):
        console.print(Alert.error("Download failed"))
        return

    # Install packages
    console.print("\n[bold cyan]📥 Installing Packages[/bold cyan]\n")

    # Create stepper for installation
    install_steps = [(pkg, f"Install {pkg}") for pkg in all_packages]
    stepper = Stepper(title="Installation Progress")

    for pkg, desc in install_steps:
        stepper.add_step(pkg, desc)

    console.print(stepper)

    # Install each package
    for idx, pkg in enumerate(all_packages):
        success = installer.install_package(pkg, stepper, idx)

        if not success and pkg in [p["name"] for p in packages]:
            # Critical package failed
            console.print("\n")
            console.print(
                Alert.error(
                    f"Critical package '{pkg}' failed to install", details="Starting rollback..."
                )
            )

            # Simulate rollback
            with Spinner("Rolling back installation...") as spinner:
                time.sleep(2)
                spinner.success("Rollback complete")

            return

    # Configure packages
    if installer.installed_packages:
        _configs = (
            installer.configure_packages()
        )  # Result not used - method called for side effects

    # Final summary
    console.print("\n")
    console.print(stepper)

    console.print("\n")
    with Section("Installation Complete", subtitle="Summary") as section:
        summary = {
            "Packages Installed": len(installer.installed_packages),
            "Packages Failed": len(installer.failed_packages),
            "Total Disk Used": f"{random.randint(100, 200)} MB",
            "Installation Time": f"{random.randint(2, 5)}m {random.randint(10, 59)}s",
        }

        kv = KeyValue(summary)
        section.add(kv)

        if installer.failed_packages:
            section.add_spacing()
            section.add_text("Failed packages:", style="bold red")
            for pkg in installer.failed_packages:
                section.add_text(f"  • {pkg}", style="red")

    # Final status
    if installer.failed_packages:
        console.print(
            Alert.warning(
                "Installation completed with warnings",
                details=f"{len(installer.failed_packages)} packages failed to install",
            )
        )
    else:
        console.print(
            Alert.success("All packages installed successfully", details="System is ready to use")
        )

    # Post-install recommendations
    console.print("\n")
    with Section("Next Steps") as section:
        section.add_text("1. Review configuration files in /etc/packages/", style="dim")
        section.add_text("2. Start services with 'systemctl start <service>'", style="dim")
        section.add_text("3. Check logs in /var/log/packages/", style="dim")


if __name__ == "__main__":
    run_installer()
