from chalkbox import JsonView, get_console


def demo_basic_usage():
    """Basic usage examples."""
    console = get_console()
    console.print("\n[bold cyan]═══ Basic JsonView Usage ═══[/bold cyan]\n")

    # Simple dictionary
    console.print("[dim]Simple dictionary:[/dim]")
    data = {"name": "John Doe", "age": 30, "email": "john@example.com"}
    json_view = JsonView.from_dict(data)
    console.print(json_view)
    console.print()

    # List of items
    console.print("[dim]List of items:[/dim]")
    items = ["apple", "banana", "cherry", "date"]
    json_view_list = JsonView.from_list(items)
    console.print(json_view_list)
    console.print()

    # Nested structure
    console.print("[dim]Nested structure:[/dim]")
    nested = {
        "user": {"name": "Alice", "role": "admin", "permissions": ["read", "write", "delete"]},
        "active": True,
    }
    console.print(JsonView.from_dict(nested))


def demo_advanced_features():
    """Advanced features and options."""
    console = get_console()
    console.print("\n[bold cyan]═══ Advanced Features ═══[/bold cyan]\n")

    # Complex nested data
    console.print("[dim]Complex API response:[/dim]")
    api_response = {
        "status": "success",
        "data": {
            "users": [
                {"id": 1, "name": "Alice", "active": True},
                {"id": 2, "name": "Bob", "active": False},
                {"id": 3, "name": "Charlie", "active": True},
            ],
            "meta": {"total": 3, "page": 1, "per_page": 10},
        },
        "timestamp": "2024-01-01T12:00:00Z",
    }
    console.print(JsonView(api_response))
    console.print()

    # Database configuration
    console.print("[dim]Database config:[/dim]")
    db_config = {
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "myapp_db",
            "credentials": {"username": "admin", "password": "secret123"},
            "pool": {"min": 2, "max": 10, "idle_timeout": 30000},
        }
    }
    console.print(JsonView.from_dict(db_config))


def demo_styling():
    """Styling and theming options."""
    console = get_console()
    console.print("\n[bold cyan]═══ Styling Options ═══[/bold cyan]\n")

    data = {
        "service": "api",
        "version": "2.0.0",
        "endpoints": ["/users", "/posts", "/comments"],
        "features": {"auth": True, "cache": True, "logging": True},
    }

    # Pretty printed (default)
    console.print("[dim]Pretty printed (indent=4):[/dim]")
    console.print(JsonView.pretty(data))
    console.print()

    # Compact format
    console.print("[dim]Compact format:[/dim]")
    console.print(JsonView.compact(data))
    console.print()

    # Sorted keys
    console.print("[dim]Sorted keys:[/dim]")
    console.print(JsonView(data, sort_keys=True))
    console.print()

    # Custom indentation
    console.print("[dim]Custom indentation (6 spaces):[/dim]")
    console.print(JsonView(data, indent=6))


def demo_use_cases():
    """Common use cases for JSON views."""
    console = get_console()
    console.print("\n[bold cyan]═══ Use Cases ═══[/bold cyan]\n")

    # Configuration display
    console.print("[dim]Application config:[/dim]")
    app_config = {
        "app_name": "MyApp",
        "environment": "production",
        "debug": False,
        "server": {"host": "0.0.0.0", "port": 8000, "workers": 4},  # noqa: S104  # Demo config example
        "logging": {"level": "INFO", "format": "json", "outputs": ["stdout", "file"]},
    }
    console.print(JsonView.from_dict(app_config))
    console.print()

    # API request/response
    console.print("[dim]API request payload:[/dim]")
    request = {
        "method": "POST",
        "endpoint": "/api/users",
        "headers": {"Content-Type": "application/json", "Authorization": "Bearer token123"},
        "body": {"name": "New User", "email": "newuser@example.com", "role": "user"},
    }
    console.print(JsonView(request))
    console.print()

    # From JSON string
    console.print("[dim]Parse JSON string:[/dim]")
    json_string = '{"message": "Hello", "code": 200, "success": true}'
    console.print(JsonView.from_string(json_string))


def main():
    """Run all JsonView demos."""
    console = get_console()

    console.print(
        "\n[bold magenta]╔════════════════════════════════════════════════╗[/bold magenta]"
    )
    console.print("[bold magenta]║   ChalkBox - JsonView Component Demo          ║[/bold magenta]")
    console.print("[bold magenta]╚════════════════════════════════════════════════╝[/bold magenta]")

    demo_basic_usage()
    demo_advanced_features()
    demo_styling()
    demo_use_cases()

    console.print("\n[bold green]✓  JsonView demo completed![/bold green]")
    console.print(
        "\n[dim]JsonView is perfect for: API responses, config files, debugging, and data inspection[/dim]\n"
    )


if __name__ == "__main__":
    main()
