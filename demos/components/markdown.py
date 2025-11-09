from rich.panel import Panel

from chalkbox import (
    Divider,
    Markdown,
    get_console,
)


def demo_basic_usage():
    """Basic usage examples."""
    console = get_console()
    console.print()
    console.print(Divider(title="Basic Markdown Usage", style="bold cyan"))
    console.print()

    # Simple heading
    console.print("[dim]Heading:[/dim]")
    console.print(Markdown.heading("Welcome to ChalkBox", level=1))
    console.print()

    # Paragraph
    console.print("[dim]Paragraph with formatting:[/dim]")
    md_text = """
This is a **bold** word and this is *italic*.
You can also use `inline code` for technical terms.
    """
    console.print(Markdown(md_text.strip()))
    console.print()

    # Unordered list
    console.print("[dim]Unordered list:[/dim]")
    items = ["Install ChalkBox", "Import components", "Build beautiful CLIs"]
    console.print(Markdown.from_list(items))
    console.print()

    # Ordered list
    console.print("[dim]Ordered list:[/dim]")
    steps = ["Clone repository", "Install dependencies", "Run examples"]
    console.print(Markdown.from_list(steps, ordered=True))


def demo_advanced_features():
    """Advanced features and options."""
    console = get_console()
    console.print()
    console.print(Divider(title="Advanced Features", style="bold cyan"))
    console.print()

    # Code block
    console.print("[dim]Code block:[/dim]")
    code = """from chalkbox import Alert, get_console

console = get_console()
console.print(Alert.success("Hello, World!"))"""
    console.print(Markdown.code_block(code, language="python"))
    console.print()

    # Blockquote
    console.print("[dim]Blockquote:[/dim]")
    quote_text = "The best way to predict the future is to invent it."
    console.print(Markdown.quote(quote_text))
    console.print()

    # Table
    console.print("[dim]Markdown table:[/dim]")
    headers = ["Component", "Purpose", "Status"]
    rows = [
        ["Alert", "Notifications", "✓"],
        ["Table", "Data display", "✓"],
        ["Progress", "Task tracking", "✓"],
    ]
    console.print(Markdown.table(headers, rows))
    console.print()

    # Complex markdown
    console.print("[dim]Complex document:[/dim]")
    complex_md = """
# Project Documentation

## Overview

This project provides a **comprehensive** CLI toolkit with the following features:

- Themed components
- Easy integration
- Rich formatting

## Installation

```bash
pip install chalkbox
```

## Quick Start

1. Import the library
2. Create components
3. Display in terminal

> Note: All components are fail-safe and work in non-TTY environments.
    """
    console.print(Markdown(complex_md.strip()))


def demo_styling():
    """Styling and theming options."""
    console = get_console()
    console.print()
    console.print(Divider(title="Styling Options", style="bold cyan"))
    console.print()

    # Different heading levels
    console.print("[dim]Heading levels:[/dim]")
    for level in range(1, 4):
        console.print(Markdown.heading(f"Heading Level {level}", level=level))
    console.print()

    # Code with different languages
    console.print("[dim]JavaScript code:[/dim]")
    js_code = """const message = "Hello";
console.log(message);"""
    console.print(Markdown.code_block(js_code, language="javascript"))
    console.print()

    console.print("[dim]Bash script:[/dim]")
    bash_code = """#!/bin/bash
echo "Starting deployment..."
npm run build"""
    console.print(Markdown.code_block(bash_code, language="bash"))
    console.print()

    # Combined styles
    console.print("[dim]Rich formatting:[/dim]")
    rich_md = """
**Bold text**, *italic text*, and `inline code`.

You can combine ***bold and italic***.

Links: [ChalkBox](https://github.com/example/chalkbox)
    """
    console.print(Markdown(rich_md.strip()))


def demo_use_cases():
    """Common use cases for markdown rendering."""
    console = get_console()
    console.print()
    console.print(Divider(title="Use Cases", style="bold cyan"))
    console.print()

    # Release notes
    console.print("[dim]Release notes:[/dim]")
    release_notes = """
# Release v2.0.0

## New Features

- Added **JsonView** component for JSON visualization
- Improved **Table** performance by 40%
- New **Markdown** rendering support

## Bug Fixes

- Fixed spinner animation in non-TTY environments
- Corrected color rendering on Windows terminals

## Breaking Changes

> The `old_method()` has been deprecated. Use `new_method()` instead.
    """
    console.print(Markdown(release_notes.strip()))
    console.print()

    # Help documentation
    console.print("[dim]Command help:[/dim]")
    help_text = """
## deploy command

Deploy your application to production.

### Usage

```bash
myapp deploy [options]
```

### Options

| Option | Description | Default |
| --- | --- | --- |
| --env | Target environment | production |
| --verbose | Enable verbose output | false |
| --dry-run | Simulate deployment | false |

### Examples

```bash
# Deploy to production
myapp deploy

# Deploy to staging with verbose output
myapp deploy --env staging --verbose
```
    """
    console.print(Markdown(help_text.strip()))


def main():
    """Run all Markdown demos."""
    console = get_console()

    console.print()
    console.print(
        Panel(
            "[bold]ChalkBox - Markdown Component Demo[/bold]",
            style="magenta",
            expand=False,
        )
    )

    demo_basic_usage()
    demo_advanced_features()
    demo_styling()
    demo_use_cases()

    console.print("\n[bold green]✓  Markdown demo completed![/bold green]")
    console.print(
        "\n[dim]Markdown is perfect for: documentation, help text, release notes, and formatted output[/dim]\n"
    )


if __name__ == "__main__":
    main()
