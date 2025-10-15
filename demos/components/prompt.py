from rich.syntax import Syntax

from chalkbox import get_console


def demo_basic_usage():
    """Basic usage examples."""
    console = get_console()
    console.print("\n[bold cyan]═══ Basic Prompt Usage ═══[/bold cyan]\n")

    # Input examples
    console.print("[bold]Input Component[/bold]\n")

    code1 = """from chalkbox import Input

# Simple text input
name = Input.ask_once("What is your name?", default="User")
print(f"Hello, {name}!")

# With choices
env = Input.ask_once(
    "Select environment",
    choices=["dev", "staging", "production"],
    default="dev"
)"""
    console.print(Syntax(code1, "python", theme="monokai"))
    console.print()

    # Confirm examples
    console.print("[bold]Confirm Component[/bold]\n")

    code2 = """from chalkbox import Confirm

# Yes/no confirmation
proceed = Confirm.ask_once("Continue with deployment?", default=False)

if proceed:
    print("Deploying...")
else:
    print("Cancelled")"""
    console.print(Syntax(code2, "python", theme="monokai"))
    console.print()

    # Select examples
    console.print("[bold]Select Component[/bold]\n")

    code3 = """from chalkbox import Select

# Multiple choice selection
action = Select.ask_once(
    "Choose an action",
    choices=["start", "stop", "restart", "status"],
    default="status"
)"""
    console.print(Syntax(code3, "python", theme="monokai"))


def demo_advanced_features():
    """Advanced features and options."""
    console = get_console()
    console.print("\n[bold cyan]═══ Advanced Features ═══[/bold cyan]\n")

    # Number input
    console.print("[bold]IntInput and FloatInput[/bold]\n")

    code1 = """from chalkbox import IntInput, FloatInput

# Integer input with validation
port = IntInput.ask_once(
    "Enter port number",
    default=8000,
    min_value=1024,
    max_value=65535
)

# Float input with range
cpu_limit = FloatInput.ask_once(
    "CPU limit (cores)",
    default=2.0,
    min_value=0.1,
    max_value=8.0
)"""
    console.print(Syntax(code1, "python", theme="monokai"))
    console.print()

    # Password input
    console.print("[bold]Password Input[/bold]\n")

    code2 = """from chalkbox import Input

# Masked password input
password = Input("Enter password", password=True).ask()
api_key = Input("Enter API key", password=True).ask()"""
    console.print(Syntax(code2, "python", theme="monokai"))
    console.print()

    # Reusable prompts
    console.print("[bold]Reusable Prompt Objects[/bold]\n")

    code3 = """from chalkbox import Input, Select

# Create reusable prompts
env_prompt = Select(
    "Select environment",
    choices=["dev", "staging", "production"],
    default="dev"
)

# Use multiple times
env1 = env_prompt.ask()
env2 = env_prompt.ask()"""
    console.print(Syntax(code3, "python", theme="monokai"))


def demo_styling():
    """Styling and theming options."""
    console = get_console()
    console.print("\n[bold cyan]═══ Styling Options ═══[/bold cyan]\n")

    console.print("[bold]Prompts use ChalkBox theming automatically[/bold]\n")

    code = """from chalkbox import Input, Confirm, Select

# All prompts automatically use ChalkBox theme colors
# - Primary color for prompt text
# - Warning color for confirmations
# - Muted color for defaults

# Input with custom styling via theme
username = Input("Username").ask()

# Confirm with themed warning color
confirm = Confirm("Delete all files?").ask()

# Select with themed choices display
option = Select("Choose", ["one", "two", "three"]).ask()"""
    console.print(Syntax(code, "python", theme="monokai"))


def demo_use_cases():
    """Common use cases for prompts."""
    console = get_console()
    console.print("\n[bold cyan]═══ Use Cases ═══[/bold cyan]\n")

    # Configuration wizard
    console.print("[bold]Configuration Wizard[/bold]\n")

    code1 = '''from chalkbox import Input, IntInput, Confirm, Select

def setup_wizard():
    """Interactive configuration wizard."""
    config = {}

    config["app_name"] = Input.ask_once("Application name", default="myapp")
    config["port"] = IntInput.ask_once("Port", default=8000, min_value=1024)
    config["env"] = Select.ask_once(
        "Environment",
        choices=["development", "production"],
        default="development"
    )
    config["debug"] = Confirm.ask_once("Enable debug mode?", default=True)

    return config

config = setup_wizard()'''
    console.print(Syntax(code1, "python", theme="monokai"))
    console.print()

    # Deployment confirmation
    console.print("[bold]Deployment Confirmation[/bold]\n")

    code2 = '''from chalkbox import Confirm, Alert

def deploy(environment):
    """Deploy with confirmation."""
    Alert.warning(f"You are about to deploy to {environment}")

    if Confirm.ask_once(f"Deploy to {environment}?", default=False):
        print("Deploying...")
        return True
    else:
        Alert.info("Deployment cancelled")
        return False'''
    console.print(Syntax(code2, "python", theme="monokai"))
    console.print()

    # Multi-step workflow
    console.print("[bold]Multi-step Workflow[/bold]\n")

    code3 = '''from chalkbox import Input, Select, IntInput

def create_project():
    """Multi-step project creation."""
    name = Input.ask_once("Project name")
    template = Select.ask_once(
        "Template",
        choices=["basic", "advanced", "custom"]
    )
    workers = IntInput.ask_once(
        "Worker processes",
        default=4,
        min_value=1,
        max_value=16
    )

    print(f"Creating {name} with {template} template...")
    return {"name": name, "template": template, "workers": workers}'''
    console.print(Syntax(code3, "python", theme="monokai"))


def main():
    """Run all Prompt demos."""
    console = get_console()

    console.print(
        "\n[bold magenta]╔════════════════════════════════════════════════╗[/bold magenta]"
    )
    console.print("[bold magenta]║   ChalkBox - Prompt Components Demo           ║[/bold magenta]")
    console.print("[bold magenta]╚════════════════════════════════════════════════╝[/bold magenta]")

    console.print(
        "\n[bold yellow]Note:[/bold yellow] This demo shows code examples. "
        "For interactive prompts, use these components in your own scripts.\n"
    )

    demo_basic_usage()
    demo_advanced_features()
    demo_styling()
    demo_use_cases()

    console.print("\n[bold green]✓  Prompt demo completed![/bold green]")
    console.print(
        "\n[dim]Prompts are perfect for: user input, configuration wizards, confirmations, and interactive CLIs[/dim]\n"
    )


if __name__ == "__main__":
    main()
