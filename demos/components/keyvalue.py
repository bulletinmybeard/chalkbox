from chalkbox import KeyValue, get_console


def demo_basic_usage():
    """Basic usage examples."""
    console = get_console()
    console.print("\n[bold cyan]═══ Basic KeyValue Usage ═══[/bold cyan]\n")

    # Simple configuration
    console.print("[dim]Simple config:[/dim]")
    config = {"host": "localhost", "port": 5432, "database": "myapp", "timeout": 30}
    kv = KeyValue(config, title="Database Configuration")
    console.print(kv)
    console.print()

    # System information
    console.print("[dim]System info:[/dim]")
    system_info = {
        "OS": "Linux",
        "Python": "3.12.0",
        "CPU": "Intel i7",
        "Memory": "16 GB",
        "Disk": "512 GB SSD",
    }
    kv_system = KeyValue(system_info, title="System Information")
    console.print(kv_system)


def demo_advanced_features():
    """Advanced features and options."""
    console = get_console()
    console.print("\n[bold cyan]═══ Advanced Features ═══[/bold cyan]\n")

    # Secret masking (default behavior)
    console.print("[dim]Automatic secret masking:[/dim]")
    credentials = {
        "username": "admin",
        "password": "super_secret_password_123",
        "api_key": "sk-1234567890abcdefghijklmnop",
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        "database": "myapp",
        "host": "localhost",
    }
    kv_masked = KeyValue(credentials, title="Credentials (Masked)")
    console.print(kv_masked)
    console.print()

    # Reveal secrets
    console.print("[dim]Secrets revealed:[/dim]")
    kv_revealed = KeyValue(credentials, title="Credentials (Revealed)", reveal=True)
    console.print(kv_revealed)
    console.print()

    # Different value types
    console.print("[dim]Various value types:[/dim]")
    mixed_types = {
        "string": "text value",
        "number": 42,
        "boolean": True,
        "none_value": None,
        "list": ["item1", "item2", "item3"],
        "long_list": list(range(20)),
        "dict": {"nested": "data"},
    }
    kv_types = KeyValue(mixed_types, title="Mixed Types")
    console.print(kv_types)


def demo_styling():
    """Styling and theming options."""
    console = get_console()
    console.print("\n[bold cyan]═══ Styling Options ═══[/bold cyan]\n")

    config = {"service": "web", "version": "2.0.0", "port": 8000, "debug": False}

    # Custom separator
    console.print("[dim]Custom separator (=):[/dim]")
    kv_sep = KeyValue(config, title="Config", separator=" =")
    console.print(kv_sep)
    console.print()

    # Custom styles
    console.print("[dim]Custom key/value styles:[/dim]")
    kv_styled = KeyValue(config, title="Styled Config", key_style="bold cyan", value_style="yellow")
    console.print(kv_styled)
    console.print()

    # No alignment
    console.print("[dim]Without alignment:[/dim]")
    kv_no_align = KeyValue(config, title="No Align", align=False)
    console.print(kv_no_align)


def demo_use_cases():
    """Common use cases for key-value lists."""
    console = get_console()
    console.print("\n[bold cyan]═══ Use Cases ═══[/bold cyan]\n")

    # Application settings
    console.print("[dim]Application settings:[/dim]")
    app_settings = {
        "app_name": "MyApp",
        "environment": "production",
        "debug_mode": False,
        "log_level": "INFO",
        "max_workers": 4,
        "cache_enabled": True,
    }
    kv_app = KeyValue.from_config(app_settings)
    console.print(kv_app)
    console.print()

    # Build information
    console.print("[dim]Build info:[/dim]")
    build_info = {
        "version": "1.2.3",
        "build_number": "456",
        "commit_hash": "abc123def",
        "build_date": "2024-01-15",
        "build_time": "14:30:00",
    }
    kv_build = KeyValue(build_info, title="Build Information")
    console.print(kv_build)
    console.print()

    # Server status
    console.print("[dim]Server status:[/dim]")
    server_status = {
        "status": "running",
        "uptime": "14 days, 3 hours",
        "requests_served": 1234567,
        "active_connections": 42,
        "cpu_usage": "45%",
        "memory_usage": "2.1 GB / 16 GB",
    }
    kv_status = KeyValue(server_status, title="Server Status")
    console.print(kv_status)
    console.print()

    # Adding items dynamically
    console.print("[dim]Dynamic key-value list:[/dim]")
    kv_dynamic = KeyValue(title="Test Results")
    kv_dynamic.add("Total Tests", 150)
    kv_dynamic.add("Passed", 145)
    kv_dynamic.add("Failed", 5)
    kv_dynamic.add("Skipped", 0)
    kv_dynamic.add("Duration", "12.3s")
    console.print(kv_dynamic)


def main():
    """Run all KeyValue demos."""
    console = get_console()

    console.print(
        "\n[bold magenta]╔════════════════════════════════════════════════╗[/bold magenta]"
    )
    console.print("[bold magenta]║   ChalkBox - KeyValue Component Demo          ║[/bold magenta]")
    console.print("[bold magenta]╚════════════════════════════════════════════════╝[/bold magenta]")

    demo_basic_usage()
    demo_advanced_features()
    demo_styling()
    demo_use_cases()

    console.print("\n[bold green]✓  KeyValue demo completed![/bold green]")
    console.print(
        "\n[dim]KeyValue is perfect for: configs, credentials (auto-masked), stats, and settings display[/dim]\n"
    )


if __name__ == "__main__":
    main()
