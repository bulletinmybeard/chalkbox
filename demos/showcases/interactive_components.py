from pathlib import Path

from chalkbox import (
    Alert,
    Divider,
    Section,
    Table,
    Tree,
    get_console,
)


def demo_prompts():
    """Demonstrate prompt components (simulated interaction)."""
    console = get_console()

    console.print("\n[bold cyan]═══ Prompt Components Demo ═══[/bold cyan]\n")
    console.print(
        "[dim]Note: This demo shows simulated interaction to allow batch execution[/dim]\n"
    )

    # Divider
    Divider.section("User Input Examples").print()

    # Basic text input (simulated)
    console.print("[cyan]?[/cyan] What is your name? [dim](default: Guest)[/dim]")
    name = "Alice Johnson"  # Simulated input
    console.print(f"[cyan]>[/cyan] {name}")
    console.print(f"[green]✓[/green] Hello, {name}!\n")

    # Input with choices (simulated)
    console.print("[cyan]?[/cyan] Choose your favorite language")
    console.print("[dim]  Choices: Python, JavaScript, Rust, Go (default: Python)[/dim]")
    language = "Rust"  # Simulated selection
    console.print(f"[cyan]>[/cyan] {language}")
    console.print(f"[green]✓[/green] Great choice: {language}!\n")

    # Integer input (simulated)
    console.print("[cyan]?[/cyan] Enter your age [dim](default: 25, range: 0-120)[/dim]")
    age = 32  # Simulated input
    console.print(f"[cyan]>[/cyan] {age}")
    console.print(f"[green]✓[/green] You are {age} years old\n")

    # Float input (simulated)
    console.print(
        "[cyan]?[/cyan] Enter temperature (°C) [dim](default: 20.0, range: -50.0 to 50.0)[/dim]"
    )
    temperature = 23.5  # Simulated input
    console.print(f"[cyan]>[/cyan] {temperature}")
    console.print(f"[green]✓[/green] Temperature: {temperature}°C\n")

    # Confirmation (simulated)
    console.print("[cyan]?[/cyan] Continue to next demo? [dim](Y/n, default: Yes)[/dim]")
    should_continue = True  # Simulated confirmation
    console.print(f"[cyan]>[/cyan] {'Yes' if should_continue else 'No'}")

    if should_continue:
        console.print("[green]✓[/green] Moving on!\n")
    else:
        console.print("[yellow]⚠[/yellow] Demo stopped\n")
        return False

    return True


def demo_dividers():
    """Demonstrate divider components."""
    console = get_console()

    console.print("\n[bold cyan]═══ Divider Components Demo ═══[/bold cyan]\n")

    # Different divider styles
    Divider.section("Section with Title").print()
    console.print("Content under section divider\n")

    Divider.separator().print()
    console.print("Content after plain separator\n")

    Divider.double("Double Line Divider").print()
    console.print("Content with double-line divider\n")

    Divider.heavy("Heavy Divider").print()
    console.print("Content with heavy divider\n")

    Divider.dotted("Dotted Divider").print()
    console.print("Content with dotted divider\n")

    Divider.dashed("Dashed Divider").print()
    console.print("Content with dashed divider\n")


def demo_tree():
    """Demonstrate tree component."""
    console = get_console()

    console.print("\n[bold cyan]═══ Tree Component Demo ═══[/bold cyan]\n")

    # Simple tree
    Divider.section("Simple Tree").print()
    simple = Tree.simple("Programming Languages", ["Python", "JavaScript", "Rust", "Go"])
    simple.print()
    console.print()

    # Nested tree
    Divider.section("Nested Tree Structure").print()
    tech_tree = Tree("Tech Stack")
    frontend = tech_tree.add("Frontend")
    frontend.add("React")
    frontend.add("Vue")
    frontend.add("Svelte")

    backend = tech_tree.add("Backend")
    backend.add("Django")
    backend.add("FastAPI")
    backend.add("Express")

    database = tech_tree.add("Database")
    database.add("PostgreSQL")
    database.add("MongoDB")
    database.add("Redis")

    tech_tree.print()
    console.print()

    # Tree from dict
    Divider.section("Tree from Dictionary").print()
    config_data = {
        "server": {
            "host": "localhost",
            "port": 8080,
            "ssl": {"enabled": True, "cert": "/path/to/cert.pem"},
        },
        "database": {
            "host": "db.example.com",
            "port": 5432,
            "name": "myapp",
        },
        "features": ["auth", "api", "websockets"],
    }

    config_tree = Tree.from_dict(config_data, root_label="Configuration")
    config_tree.print()
    console.print()

    # Tree from filesystem (current directory, limited depth)
    Divider.section("Filesystem Tree (examples directory)").print()
    examples_path = Path(__file__).parent
    fs_tree = Tree.from_filesystem(str(examples_path), max_depth=2, show_hidden=False)
    fs_tree.print()
    console.print()


def demo_combined():
    """Demonstrate combining new components with existing ones (simulated interaction)."""
    console = get_console()

    console.print("\n[bold cyan]═══ Combined Components Demo ═══[/bold cyan]\n")

    Divider.section("Project Setup Wizard").print()

    # Get project details (simulated)
    console.print("[cyan]?[/cyan] Project name [dim](default: my-awesome-project)[/dim]")
    project_name = "chalkbox-cli-tool"  # Simulated input
    console.print(f"[cyan]>[/cyan] {project_name}\n")

    console.print("[cyan]?[/cyan] Project type")
    console.print("[dim]  Choices: Web App, CLI Tool, Library, API (default: Web App)[/dim]")
    project_type = "CLI Tool"  # Simulated selection
    console.print(f"[cyan]>[/cyan] {project_type}\n")

    # Show collected info in a section
    with Section("Project Configuration") as section:
        config_table = Table(headers=["Setting", "Value"])
        config_table.add_row("Name", project_name)
        config_table.add_row("Type", project_type)
        section.add(config_table)

    console.print()

    # Show project structure
    Divider.section("Recommended Project Structure").print()
    structure = Tree(project_name)
    structure.add("📄 README.md")
    structure.add("📄 pyproject.toml")

    src = structure.add("📁 src")
    src.add("📄 __init__.py")
    src.add("📄 main.py")

    tests = structure.add("📁 tests")
    tests.add("📄 __init__.py")
    tests.add("📄 test_main.py")

    structure.add("📁 docs")
    structure.print()

    console.print()

    # Confirmation (simulated)
    console.print(f"[cyan]?[/cyan] Create project '{project_name}'? [dim](Y/n, default: Yes)[/dim]")
    proceed = True  # Simulated confirmation
    console.print(f"[cyan]>[/cyan] {'Yes' if proceed else 'No'}\n")

    if proceed:
        console.print(Alert.success(f"Project '{project_name}' created successfully!"))
    else:
        console.print(Alert.warning("Project creation cancelled"))


def main():
    """Run all demos with simulated interaction."""
    console = get_console()

    console.print(
        "\n[bold magenta]╔════════════════════════════════════════════════╗[/bold magenta]"
    )
    console.print("[bold magenta]║   ChalkBox - Interactive Components Demo      ║[/bold magenta]")
    console.print(
        "[bold magenta]╚════════════════════════════════════════════════╝[/bold magenta]\n"
    )

    console.print("[bold yellow]Running all demos with simulated interaction...[/bold yellow]")
    console.print(
        "[dim]Interactive components shown with mock user input for batch execution[/dim]\n"
    )

    # Run demos
    demo_prompts()
    demo_dividers()
    demo_tree()
    demo_combined()

    console.print("\n[bold green]✓  All demos completed![/bold green]\n")


if __name__ == "__main__":
    main()
