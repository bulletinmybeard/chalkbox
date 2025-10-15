from chalkbox import Tree, get_console


def demo_basic_usage():
    """Basic usage examples."""
    console = get_console()
    console.print("\n[bold cyan]═══ Basic Tree Usage ═══[/bold cyan]\n")

    # Simple tree
    console.print("[dim]Simple tree:[/dim]")
    tree = Tree("Project")
    tree.add("src/")
    tree.add("tests/")
    tree.add("docs/")
    tree.add("README.md")
    console.print(tree)
    console.print()

    # Tree with branches
    console.print("[dim]Tree with branches:[/dim]")
    tree2 = Tree("Application")
    src = tree2.add("src/")
    src.add("app.py")
    src.add("config.py")
    src.add("utils.py")

    tests = tree2.add("tests/")
    tests.add("test_app.py")
    tests.add("test_utils.py")

    console.print(tree2)


def demo_advanced_features():
    """Advanced features and options."""
    console = get_console()
    console.print("\n\n[bold cyan]═══ Advanced Features ═══[/bold cyan]\n")

    # From dictionary
    console.print("[dim]Tree from nested dictionary:[/dim]")
    data = {
        "name": "MyApp",
        "version": "1.0.0",
        "config": {
            "database": {"host": "localhost", "port": 5432},
            "cache": {"enabled": True, "ttl": 300},
        },
        "features": ["auth", "logging", "metrics"],
    }
    tree_dict = Tree.from_dict(data, root_label="Configuration")
    console.print(tree_dict)
    console.print()

    # Simple helper
    console.print("[dim]Simple list tree:[/dim]")
    items = ["Initialize", "Configure", "Start Server", "Monitor"]
    tree_simple = Tree.simple("Startup Sequence", items)
    console.print(tree_simple)


def demo_styling():
    """Styling and theming options."""
    console = get_console()
    console.print("\n\n[bold cyan]═══ Styling Options ═══[/bold cyan]\n")

    # Styled branches
    console.print("[dim]Styled tree branches:[/dim]")
    tree = Tree("Status")

    success = tree.add("✓ Successful Operations", style="green")
    success.add("Database connection")
    success.add("API health check")
    success.add("Cache warmup")

    warning = tree.add("⚠ Warnings", style="yellow")
    warning.add("High memory usage")
    warning.add("Slow query detected")

    error = tree.add("✖ Errors", style="red")
    error.add("Failed to send email")

    console.print(tree)
    console.print()

    # Custom guide style
    console.print("[dim]Custom guide style:[/dim]")
    tree2 = Tree("Services", guide_style="dim cyan")
    tree2.add("Web Server")
    tree2.add("Database")
    tree2.add("Cache")
    console.print(tree2)


def demo_use_cases():
    """Common use cases for trees."""
    console = get_console()
    console.print("\n\n[bold cyan]═══ Use Cases ═══[/bold cyan]\n")

    # File structure
    console.print("[dim]Project structure:[/dim]")
    project = Tree("my-project/")

    src = project.add("src/")
    src.add("main.py")
    src.add("config.py")

    components = src.add("components/")
    components.add("header.py")
    components.add("footer.py")

    tests = project.add("tests/")
    tests.add("test_main.py")
    tests.add("test_config.py")

    project.add("README.md")
    project.add("pyproject.toml")

    console.print(project)
    console.print()

    # Menu structure
    console.print("[dim]Navigation menu:[/dim]")
    menu = Tree("Main Menu")

    file_menu = menu.add("File")
    file_menu.add("New")
    file_menu.add("Open")
    file_menu.add("Save")
    file_menu.add("Exit")

    edit_menu = menu.add("Edit")
    edit_menu.add("Cut")
    edit_menu.add("Copy")
    edit_menu.add("Paste")

    help_menu = menu.add("Help")
    help_menu.add("Documentation")
    help_menu.add("About")

    console.print(menu)
    console.print()

    # Organization chart
    console.print("[dim]Organization structure:[/dim]")
    org = Tree("Company")

    eng = org.add("Engineering")
    eng_backend = eng.add("Backend Team")
    eng_backend.add("Alice (Lead)")
    eng_backend.add("Bob")
    eng_backend.add("Carol")

    eng_frontend = eng.add("Frontend Team")
    eng_frontend.add("David (Lead)")
    eng_frontend.add("Eve")

    ops = org.add("Operations")
    ops.add("Frank (Manager)")
    ops.add("Grace")

    console.print(org)
    console.print()

    # API structure
    console.print("[dim]API endpoints:[/dim]")
    api = Tree("API v1")

    users = api.add("/users")
    users.add("GET /users")
    users.add("POST /users")
    users.add("GET /users/:id")
    users.add("PUT /users/:id")
    users.add("DELETE /users/:id")

    posts = api.add("/posts")
    posts.add("GET /posts")
    posts.add("POST /posts")
    posts.add("GET /posts/:id")

    console.print(api)
    console.print()

    # Dependency tree
    console.print("[dim]Package dependencies:[/dim]")
    deps = Tree("my-app")

    requests = deps.add("requests==2.31.0")
    requests.add("urllib3==2.0.7")
    requests.add("certifi==2023.11.17")

    _click = deps.add("click==8.1.7")

    rich = deps.add("rich==13.7.0")
    rich.add("markdown-it-py==3.0.0")
    rich.add("pygments==2.17.2")

    console.print(deps)


def main():
    """Run all Tree demos."""
    console = get_console()

    console.print(
        "\n[bold magenta]╔════════════════════════════════════════════════╗[/bold magenta]"
    )
    console.print("[bold magenta]║   ChalkBox - Tree Component Demo              ║[/bold magenta]")
    console.print("[bold magenta]╚════════════════════════════════════════════════╝[/bold magenta]")

    demo_basic_usage()
    demo_advanced_features()
    demo_styling()
    demo_use_cases()

    console.print("\n[bold green]✓  Tree demo completed![/bold green]")
    console.print(
        "\n[dim]Tree is perfect for: file structures, hierarchies, navigation menus, and nested data[/dim]\n"
    )


if __name__ == "__main__":
    main()
