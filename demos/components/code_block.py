from chalkbox import CodeBlock, Divider, get_console


def demo_basic_usage():
    """Basic usage examples."""
    console = get_console()
    console.print("\n[bold cyan]═══ Basic CodeBlock Usage ═══[/bold cyan]\n")

    # Python code
    python_code = '''def fibonacci(n):
    """Calculate fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = fibonacci(10)
print(f"Result: {result}")'''

    Divider.section("Python Example").print()
    console.print(CodeBlock(python_code, language="python"))

    # JavaScript code
    js_code = """const fetchData = async (url) => {
  try {
    const response = await fetch(url);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Failed to fetch:', error);
  }
};"""

    Divider.section("JavaScript Example").print()
    console.print(CodeBlock(js_code, language="javascript"))


def demo_advanced_features():
    """Advanced features and options."""
    console = get_console()
    console.print("\n[bold cyan]═══ Advanced Features ═══[/bold cyan]\n")

    # Line numbers
    code = """class DatabaseConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        self.connection = create_connection(
            host=self.host,
            port=self.port
        )"""

    Divider.section("With Line Numbers").print()
    console.print(CodeBlock(code, language="python", line_numbers=True))

    # Different languages
    bash_code = """#!/bin/bash
for file in *.txt; do
    echo "Processing: $file"
    wc -l "$file"
done"""
    Divider.section("Bash Script").print()
    console.print(CodeBlock(bash_code, language="bash"))

    sql_code = """SELECT users.name, COUNT(orders.id) as count
FROM users
LEFT JOIN orders ON users.id = orders.user_id
WHERE users.created_at > '2024-01-01'
GROUP BY users.id
LIMIT 10;"""
    Divider.section("SQL Query").print()
    console.print(CodeBlock(sql_code, language="sql"))


def demo_styling():
    """Styling and theming options."""
    console = get_console()
    console.print("\n[bold cyan]═══ Styling Options ═══[/bold cyan]\n")

    code = """def greet(name):
    return f"Hello, {name}!"

print(greet("World"))"""

    # Different themes
    themes = ["monokai", "github-dark", "one-dark"]

    for theme in themes:
        Divider.section(f"Theme: {theme}").print()
        console.print(CodeBlock(code, language="python", theme=theme))
        console.print()

    # Inline snippets
    Divider.section("Install Command").print()
    console.print(CodeBlock("pip install chalkbox", language="bash"))

    Divider.section("Hello World").print()
    console.print(CodeBlock('print("Hello!")', language="python"))


def main():
    """Run all CodeBlock demos."""
    console = get_console()

    console.print(
        "\n[bold magenta]╔════════════════════════════════════════════════╗[/bold magenta]"
    )
    console.print("[bold magenta]║   ChalkBox - CodeBlock Component Demo         ║[/bold magenta]")
    console.print("[bold magenta]╚════════════════════════════════════════════════╝[/bold magenta]")

    demo_basic_usage()
    demo_advanced_features()
    demo_styling()

    console.print("\n[bold green]✓  CodeBlock demo completed![/bold green]")
    console.print(
        "\n[dim]CodeBlocks are perfect for: syntax highlighting, documentation, and code snippets[/dim]\n"
    )


if __name__ == "__main__":
    main()
