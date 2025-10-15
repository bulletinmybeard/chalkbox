from chalkbox import Divider, get_console


def demo_basic_usage():
    """Basic usage examples."""
    console = get_console()
    console.print("\n[bold cyan]═══ Basic Divider Usage ═══[/bold cyan]\n")

    # Simple separator
    console.print(Divider.separator())
    console.print()

    # Section divider with title
    console.print(Divider.section("Configuration"))
    console.print("host: localhost")
    console.print("port: 5432")
    console.print()

    # Centered title
    console.print(Divider("Application Settings", align="center"))
    console.print()

    # Right-aligned title
    console.print(Divider("End of Section", align="right"))


def demo_advanced_features():
    """Advanced features and options."""
    console = get_console()
    console.print("\n[bold cyan]═══ Advanced Features ═══[/bold cyan]\n")

    # Different character styles
    console.print("[dim]Double line:[/dim]")
    console.print(Divider.double("Important Section"))
    console.print()

    console.print("[dim]Heavy line:[/dim]")
    console.print(Divider.heavy("Critical Information"))
    console.print()

    console.print("[dim]Light line:[/dim]")
    console.print(Divider.light("Subsection"))
    console.print()

    console.print("[dim]Dotted line:[/dim]")
    console.print(Divider.dotted("Optional Content"))
    console.print()

    console.print("[dim]Dashed line:[/dim]")
    console.print(Divider.dashed("Work in Progress"))


def demo_styling():
    """Styling and theming options."""
    console = get_console()
    console.print("\n[bold cyan]═══ Styling Options ═══[/bold cyan]\n")

    # Colored dividers
    console.print("[dim]Green divider:[/dim]")
    console.print(Divider("Success Section", style="bold green"))
    console.print()

    console.print("[dim]Yellow divider:[/dim]")
    console.print(Divider("Warning Section", style="bold yellow"))
    console.print()

    console.print("[dim]Red divider:[/dim]")
    console.print(Divider("Error Section", style="bold red"))
    console.print()

    console.print("[dim]Blue divider:[/dim]")
    console.print(Divider("Information", style="bold blue"))
    console.print()

    # Custom characters
    console.print("[dim]Custom characters:[/dim]")
    console.print(Divider("Stars", characters="*"))
    console.print(Divider("Equals", characters="="))
    console.print(Divider("Tilde", characters="~"))


def demo_use_cases():
    """Common use cases for dividers."""
    console = get_console()
    console.print("\n[bold cyan]═══ Use Cases ═══[/bold cyan]\n")

    # Document structure
    console.print(Divider.section("1. Introduction"))
    console.print("This is the introduction section of the document.")
    console.print()

    console.print(Divider.section("2. Installation"))
    console.print("Run: pip install chalkbox")
    console.print()

    console.print(Divider.section("3. Usage"))
    console.print("Import and use components as needed.")
    console.print()

    # Log output separation
    console.print(Divider.double("Build Process", align="center"))
    console.print("Building application...")
    console.print("Compiling...")
    console.print("Tests passed!")
    console.print(Divider.separator())
    console.print()

    # Status sections
    console.print(Divider("System Status", style="green", align="center"))
    console.print("All services operational")
    console.print(Divider.separator())


def main():
    """Run all Divider demos."""
    console = get_console()

    console.print(
        "\n[bold magenta]╔════════════════════════════════════════════════╗[/bold magenta]"
    )
    console.print("[bold magenta]║   ChalkBox - Divider Component Demo           ║[/bold magenta]")
    console.print("[bold magenta]╚════════════════════════════════════════════════╝[/bold magenta]")

    demo_basic_usage()
    demo_advanced_features()
    demo_styling()
    demo_use_cases()

    console.print("\n[bold green]✓  Divider demo completed![/bold green]")
    console.print(
        "\n[dim]Dividers are perfect for: section separation, document structure, and visual organization[/dim]\n"
    )


if __name__ == "__main__":
    main()
