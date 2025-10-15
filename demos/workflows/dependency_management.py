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


class DependencyManager:
    """Package dependency manager."""

    def __init__(self, project_name: str):
        self.console = get_console()
        self.logger = setup_logging(level="INFO")
        self.project_name = project_name
        self.dependency_tree = {}
        self.installed_packages = []
        self.version_conflicts = []
        self.install_errors = []

    def resolve_dependencies(self, packages: list):
        """Resolve package dependencies with version constraints."""
        self.console.print("\n[bold cyan]🔍 Resolving Dependencies[/bold cyan]\n")

        with Spinner("Analyzing dependency graph...") as spinner:
            time.sleep(2)

            # Build dependency tree
            for pkg in packages:
                pkg_name = pkg["name"]
                self.dependency_tree[pkg_name] = {
                    "version": pkg["version"],
                    "dependencies": [],
                }

                # Simulate finding transitive dependencies
                if pkg_name == "fastapi":
                    self.dependency_tree[pkg_name]["dependencies"] = [
                        "starlette",
                        "pydantic",
                        "typing-extensions",
                    ]
                elif pkg_name == "django":
                    self.dependency_tree[pkg_name]["dependencies"] = [
                        "asgiref",
                        "sqlparse",
                        "pytz",
                    ]
                elif pkg_name == "requests":
                    self.dependency_tree[pkg_name]["dependencies"] = [
                        "urllib3",
                        "certifi",
                        "charset-normalizer",
                    ]
                elif pkg_name == "pytest":
                    self.dependency_tree[pkg_name]["dependencies"] = [
                        "pluggy",
                        "packaging",
                        "iniconfig",
                    ]

            # Calculate total packages (collect package names and their dependencies)
            all_packages = set()
            for pkg in packages:
                pkg_name = pkg["name"]
                all_packages.add(pkg_name)
                for dep in self.dependency_tree[pkg_name]["dependencies"]:
                    all_packages.add(dep)

            spinner.success(f"Resolved {len(all_packages)} total packages")

        # Check for version conflicts
        self.console.print()
        with Spinner("Checking for version conflicts...") as spinner:
            time.sleep(1)

            # Simulate finding conflicts (10% chance)
            if random.random() < 0.1:
                conflict_pkg = random.choice(list(self.dependency_tree.keys()))
                self.version_conflicts.append(
                    f"{conflict_pkg}: required by multiple packages with different versions"
                )
                spinner.warning("Version conflicts detected")
            else:
                spinner.success("No version conflicts")

        # Display dependency tree
        with Section("Dependency Resolution") as section:
            section.add_text("Dependency tree:", style="bold")
            section.add_spacing()

            for pkg_name, pkg_info in self.dependency_tree.items():
                section.add_text(f"📦 {pkg_name} @ {pkg_info['version']}", style="bold cyan")

                if pkg_info["dependencies"]:
                    for dep in pkg_info["dependencies"]:
                        section.add_text(f"  └─ {dep}", style="dim")
                else:
                    section.add_text("  └─ (no dependencies)", style="dim")

                section.add_spacing()

            # Version conflicts warning
            if self.version_conflicts:
                section.add_text("⚠ Version Conflicts:", style="bold yellow")
                for conflict in self.version_conflicts:
                    section.add_text(f"  • {conflict}", style="yellow")

        return list(all_packages)

    def download_packages(self, packages: list):
        """Download packages from registry."""
        self.console.print("\n[bold cyan]Downloading Packages[/bold cyan]\n")

        # Simulate package metadata
        package_metadata = {}
        for pkg in packages:
            pkg_name = pkg["name"] if isinstance(pkg, dict) else pkg

            package_metadata[pkg_name] = {
                "size": random.randint(100, 5000),  # KB
                "version": "1.0.0" if not isinstance(pkg, dict) else pkg["version"],
            }

        with Progress() as progress:
            overall_task = progress.add_task("[cyan]Downloading packages", total=len(packages))

            for pkg in packages:
                pkg_name = pkg["name"] if isinstance(pkg, dict) else pkg

                metadata = package_metadata[pkg_name]
                size_kb = metadata["size"]

                download_task = progress.add_task(f"Downloading {pkg_name}", total=size_kb * 1024)

                # Simulate download
                downloaded = 0
                while downloaded < size_kb * 1024:
                    chunk = min(50000, size_kb * 1024 - downloaded)
                    time.sleep(0.01)
                    downloaded += chunk
                    progress.update(download_task, advance=chunk)

                progress.remove_task(download_task)
                progress.update(overall_task, advance=1)

        total_size_mb = sum(m["size"] for m in package_metadata.values()) / 1024

        self.console.print(
            Alert.success(
                f"Downloaded {len(packages)} packages",
                details=f"Total size: {total_size_mb:.1f} MB",
            )
        )

        return True

    def install_packages(self, packages: list):
        """Install packages with pre/post-install scripts."""
        self.console.print("\n[bold cyan]📥 Installing Packages[/bold cyan]\n")

        install_results = []

        for pkg in packages:
            if isinstance(pkg, dict):
                pkg_name = pkg["name"]
                pkg_version = pkg["version"]
            else:
                pkg_name = pkg
                pkg_version = "1.0.0"

            self.console.print(f"\n[bold]Installing {pkg_name}@{pkg_version}[/bold]")

            # Installation steps
            steps = [
                "Running pre-install scripts",
                "Extracting package files",
                "Installing dependencies",
                "Copying files to node_modules",
                "Running post-install scripts",
                "Updating package registry",
            ]

            with Progress() as progress:
                task = progress.add_task(f"Installing {pkg_name}", total=len(steps))

                for _step in steps:
                    time.sleep(random.uniform(0.1, 0.3))
                    progress.update(task, advance=1)

            # Simulate occasional installation failures (5% chance)
            if random.random() < 0.05:
                status = "Failed"
                self.install_errors.append(pkg_name)
                self.console.print(f"  [red]✖[/red] Failed to install {pkg_name}")
            else:
                status = "Installed"
                self.installed_packages.append(
                    {
                        "Package": pkg_name,
                        "Version": pkg_version,
                        "Status": "✓ Installed",
                    }
                )
                self.console.print(f"  [green]✓[/green] Installed {pkg_name}")

            install_results.append(
                {
                    "Package": pkg_name,
                    "Version": pkg_version,
                    "Status": status,
                }
            )

        # Display installation summary
        self.console.print("\n")
        with Section("Installation Summary") as section:
            results_table = Table.from_list_of_dicts(install_results)
            section.add(results_table)

        return len(self.install_errors) == 0

    def verify_installation(self):
        """Verify installed packages."""
        self.console.print("\n[bold cyan]✓ Verifying Installation[/bold cyan]\n")

        with Progress() as progress:
            task = progress.add_task("Verifying packages", total=len(self.installed_packages))

            for _pkg in self.installed_packages:
                time.sleep(0.1)
                progress.update(task, advance=1)

        self.console.print(Alert.success(f"Verified {len(self.installed_packages)} packages"))

        return True

    def generate_lockfile(self):
        """Generate dependency lockfile."""
        self.console.print("\n[bold cyan]🔒 Generating Lock File[/bold cyan]\n")

        with Spinner("Generating package-lock.json...") as spinner:
            time.sleep(1)
            spinner.success("Lock file generated")

        lockfile_info = {
            "Packages": len(self.installed_packages),
            "Lockfile Version": "3.0",
            "Node Version": ">=18.0.0",
            "Location": "./package-lock.json",
        }

        with Section("Lock File Information") as section:
            kv = KeyValue(lockfile_info)
            section.add(kv)

        return True


def run_dependency_manager():
    """Execute dependency management workflow."""
    console = get_console()

    console.print("[bold magenta]═══════════════════════════════════════════════[/bold magenta]")
    console.print("[bold magenta]          Package Dependency Manager[/bold magenta]")
    console.print("[bold magenta]═══════════════════════════════════════════════[/bold magenta]\n")

    # Project configuration
    project_config = {
        "Project": "my-awesome-app",
        "Package Manager": "npm",
        "Registry": "https://registry.npmjs.org",
        "Install Mode": "production",
    }

    with Section("Project Configuration") as section:
        kv = KeyValue(project_config)
        section.add(kv)

    # Initialize manager
    manager = DependencyManager(project_config["Project"])

    # Packages to install
    packages = [
        {"name": "fastapi", "version": "0.104.1"},
        {"name": "django", "version": "4.2.7"},
        {"name": "requests", "version": "2.31.0"},
        {"name": "pytest", "version": "7.4.3"},
        {"name": "sqlalchemy", "version": "2.0.23"},
    ]

    # Show requested packages
    console.print("\n[bold cyan]📋 Requested Packages[/bold cyan]\n")
    requested_table = Table(headers=["Package", "Version"])
    for pkg in packages:
        requested_table.add_row(pkg["name"], pkg["version"])
    console.print(requested_table)

    # Installation steps
    steps = [
        "Resolve dependencies",
        "Download packages",
        "Install packages",
        "Verify installation",
        "Generate lock file",
    ]

    console.print("\n")
    stepper = Stepper.from_list(steps, title="Installation Steps")
    console.print(stepper)

    # Execute installation
    start_time = time.time()

    # Step 1: Resolve dependencies
    stepper.start(0)
    all_packages = manager.resolve_dependencies(packages)
    if manager.version_conflicts:
        stepper.complete(0)  # Complete with warnings
    else:
        stepper.complete(0)

    # Step 2: Download
    stepper.start(1)
    if manager.download_packages(all_packages):
        stepper.complete(1)
    else:
        stepper.fail(1, "Download failed")
        return

    # Step 3: Install
    stepper.start(2)
    install_ok = manager.install_packages(all_packages)
    if install_ok:
        stepper.complete(2)
    else:
        stepper.complete(2)  # Complete with errors

    # Step 4: Verify
    stepper.start(3)
    if manager.verify_installation():
        stepper.complete(3)
    else:
        stepper.fail(3, "Verification failed")

    # Step 5: Lock file
    stepper.start(4)
    if manager.generate_lockfile():
        stepper.complete(4)
    else:
        stepper.fail(4, "Lock file generation failed")

    install_time = time.time() - start_time

    # Final summary
    console.print("\n")
    console.print(stepper)

    console.print("\n")
    with Section("Installation Complete", subtitle="Summary") as section:
        summary = {
            "Installation Time": f"{install_time:.1f}s",
            "Requested Packages": len(packages),
            "Total Packages": len(all_packages),
            "Installed": len(manager.installed_packages),
            "Failed": len(manager.install_errors),
            "Version Conflicts": len(manager.version_conflicts),
        }

        kv = KeyValue(summary)
        section.add(kv)

        # Show errors if any
        if manager.install_errors:
            section.add_spacing()
            section.add_text("Failed Packages:", style="bold red")
            for pkg in manager.install_errors:
                section.add_text(f"  • {pkg}", style="red")

        # Show conflicts if any
        if manager.version_conflicts:
            section.add_spacing()
            section.add_text("Version Conflicts:", style="bold yellow")
            for conflict in manager.version_conflicts:
                section.add_text(f"  • {conflict}", style="yellow")

    # Installed packages
    if manager.installed_packages:
        console.print("\n")
        with Section("Installed Packages") as section:
            installed_table = Table.from_list_of_dicts(manager.installed_packages[:10])
            section.add(installed_table)

            if len(manager.installed_packages) > 10:
                section.add_text(
                    f"... and {len(manager.installed_packages) - 10} more packages",
                    style="dim",
                )

    # Next steps
    console.print("\n")
    with Section("Next Steps") as section:
        section.add_text("1. Review installed packages:", style="bold")
        section.add_text("   npm list", style="dim cyan")
        section.add_spacing()

        section.add_text("2. Update packages:", style="bold")
        section.add_text("   npm update", style="dim cyan")
        section.add_spacing()

        section.add_text("3. Audit for vulnerabilities:", style="bold")
        section.add_text("   npm audit", style="dim cyan")

    # Final status
    console.print("\n")
    if manager.install_errors:
        console.print(
            Alert.error(
                "Installation completed with errors",
                details=f"{len(manager.install_errors)} packages failed to install",
            )
        )
    elif manager.version_conflicts:
        console.print(
            Alert.warning(
                "Installation completed with warnings",
                details=f"{len(manager.version_conflicts)} version conflicts detected",
            )
        )
    else:
        console.print(
            Alert.success(
                "All packages installed successfully",
                details=f"Installed {len(manager.installed_packages)} packages",
            )
        )


if __name__ == "__main__":
    run_dependency_manager()
