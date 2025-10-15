from chalkbox import (
    CodeBlock,
    Divider,
    JsonView,
    Markdown,
    get_console,
)


def demo_code_block():
    """Demonstrate CodeBlock component."""
    console = get_console()

    console.print("\n[bold cyan]═══ CodeBlock Component Demo ═══[/bold cyan]\n")

    # Python code
    Divider.section("Python Code Example").print()

    python_code = """def fibonacci(n):
    \"\"\"Generate Fibonacci sequence up to n.\"\"\"
    a, b = 0, 1
    result = []
    while a < n:
        result.append(a)
        a, b = b, a + b
    return result

# Generate first 10 Fibonacci numbers
numbers = fibonacci(100)
print(f"Fibonacci: {numbers}")"""

    code_block = CodeBlock.python(python_code, line_numbers=True, theme="monokai")
    code_block.print()
    console.print()

    # JavaScript code
    Divider.section("JavaScript Code Example").print()

    js_code = """// Async function to fetch user data
async function fetchUserData(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Failed to fetch user:', error);
        throw error;
    }
}

// Usage
fetchUserData(123).then(user => console.log(user));"""

    CodeBlock.javascript(js_code, line_numbers=True).print()
    console.print()

    # SQL code
    Divider.section("SQL Query Example").print()

    sql_code = """SELECT
    u.username,
    u.email,
    COUNT(o.id) as order_count,
    SUM(o.total) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at >= '2024-01-01'
GROUP BY u.id, u.username, u.email
HAVING COUNT(o.id) > 0
ORDER BY total_spent DESC
LIMIT 10;"""

    CodeBlock.sql(sql_code, line_numbers=True).print()
    console.print()

    # JSON code
    Divider.section("JSON Configuration Example").print()

    json_code = """{
  "server": {
    "host": "0.0.0.0",
    "port": 8080,
    "ssl": {
      "enabled": true,
      "cert": "/path/to/cert.pem",
      "key": "/path/to/key.pem"
    }
  },
  "database": {
    "host": "localhost",
    "port": 5432,
    "name": "myapp_db",
    "pool_size": 10
  },
  "features": ["auth", "api", "websockets"]
}"""

    CodeBlock.json(json_code, line_numbers=False).print()
    console.print()

    # Bash script
    Divider.section("Bash Script Example").print()

    bash_code = """#!/bin/bash
# Deployment script

set -e  # Exit on error

echo "Starting deployment..."

# Build the application
echo "Building application..."
npm run build

# Run tests
echo "Running tests..."
npm test

# Deploy to server
echo "Deploying to production..."
rsync -avz --delete dist/ user@server:/var/www/app/

echo "Deployment complete!"
"""

    CodeBlock.bash(bash_code, line_numbers=True).print()
    console.print()

    # Code with highlighted lines
    Divider.section("Code with Highlighted Lines").print()

    highlighted_code = """def calculate_total(items):
    subtotal = sum(item['price'] for item in items)
    tax = subtotal * 0.08  # This line has a bug!
    total = subtotal + tax
    return total"""

    CodeBlock(
        highlighted_code,
        language="python",
        line_numbers=True,
        highlight_lines={3},  # Highlight line 3
    ).print()
    console.print()


def demo_markdown():
    """Demonstrate Markdown component."""
    console = get_console()

    console.print("\n[bold cyan]═══ Markdown Component Demo ═══[/bold cyan]\n")

    # Heading
    Divider.section("Markdown Headings").print()

    heading_md = """# Main Heading (H1)

## Section Heading (H2)

### Subsection (H3)

#### Detail Level (H4)"""

    Markdown(heading_md).print()
    console.print()

    # Lists
    Divider.section("Markdown Lists").print()

    lists_md = """**Unordered List:**

- Python
- JavaScript
- Rust
- Go

**Ordered List:**

1. Clone the repository
2. Install dependencies
3. Run the tests
4. Deploy to production

**Nested List:**

- Backend
  - API endpoints
  - Database models
  - Authentication
- Frontend
  - React components
  - State management
  - Routing"""

    Markdown(lists_md).print()
    console.print()

    # Code blocks in Markdown
    Divider.section("Markdown with Code Blocks").print()

    code_md = """Here's how to use the API:

```python
import requests

response = requests.get('https://api.example.com/users')
users = response.json()
print(f"Found {len(users)} users")
```

And here's the response format:

```json
{
  "users": [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
  ]
}
```"""

    Markdown(code_md).print()
    console.print()

    # Tables
    Divider.section("Markdown Tables").print()

    table_md = Markdown.table(
        headers=["Name", "Role", "Status"],
        rows=[
            ["Alice", "Developer", "Active"],
            ["Bob", "Designer", "Active"],
            ["Carol", "Manager", "On Leave"],
        ],
    )
    table_md.print()
    console.print()

    # Quotes
    Divider.section("Markdown Blockquotes").print()

    quote_md = Markdown.quote("The best way to predict the future is to invent it.\n- Alan Kay")
    quote_md.print()
    console.print()

    # Rich markdown document
    Divider.section("Full Markdown Document").print()

    doc_md = """# Project Documentation

## Overview

This project demonstrates the **ChalkBox** library for creating beautiful CLI applications.

## Features

- ✅ Themed components
- ✅ Easy to use API
- ✅ Type-safe with Python 3.12
- ✅ Rich text formatting

## Installation

```bash
pip install chalkbox
```

## Quick Start

```python
from chalkbox import Console, Alert

console = Console()
console.print(Alert.success("Hello, ChalkBox!"))
```

> **NOTE:** Check out the examples directory for more demos!

## License

MIT License - see LICENSE file for details."""

    Markdown(doc_md).print()
    console.print()


def demo_json_view():
    """Demonstrate JsonView component."""
    console = get_console()

    console.print("\n[bold cyan]═══ JsonView Component Demo ═══[/bold cyan]\n")

    # Simple dictionary
    Divider.section("Simple JSON Object").print()

    simple_data = {
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com",
        "active": True,
    }

    JsonView.from_dict(simple_data).print()
    console.print()

    # Nested structure
    Divider.section("Nested JSON Structure").print()

    nested_data = {
        "user": {
            "id": 123,
            "username": "johndoe",
            "profile": {
                "firstName": "John",
                "lastName": "Doe",
                "avatar": "https://example.com/avatar.jpg",
            },
            "settings": {
                "theme": "dark",
                "notifications": True,
                "language": "en",
            },
        },
        "stats": {
            "posts": 42,
            "followers": 1234,
            "following": 567,
        },
    }

    JsonView.from_dict(nested_data).print()
    console.print()

    # Array of objects
    Divider.section("JSON Array").print()

    array_data = [
        {"id": 1, "name": "Alice", "role": "admin"},
        {"id": 2, "name": "Bob", "role": "user"},
        {"id": 3, "name": "Carol", "role": "moderator"},
    ]

    JsonView.from_list(array_data).print()
    console.print()

    # Pretty vs Compact
    Divider.section("Pretty JSON").print()

    data = {"server": "api.example.com", "port": 8080, "ssl": True, "timeout": 30}

    JsonView.pretty(data).print()
    console.print()

    # Configuration example
    Divider.section("Configuration JSON").print()

    config = {
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "myapp",
            "pool": {"min": 2, "max": 10, "idle_timeout": 10000},
        },
        "redis": {
            "host": "localhost",
            "port": 6379,
            "db": 0,
        },
        "logging": {
            "level": "info",
            "format": "json",
            "outputs": ["stdout", "file"],
        },
        "features": {
            "authentication": True,
            "api_versioning": True,
            "rate_limiting": {"enabled": True, "requests_per_minute": 100},
        },
    }

    JsonView(config, sort_keys=True).print()
    console.print()


def demo_combined():
    """Demonstrate combining Phase 3 components."""
    console = get_console()

    console.print("\n[bold cyan]═══ Combined Components Demo ═══[/bold cyan]\n")

    Divider.section("API Documentation Example").print()

    # Markdown documentation
    doc = """## POST /api/users

Create a new user account.

### Request Body"""

    Markdown(doc).print()
    console.print()

    # JSON request example
    request_data = {
        "username": "johndoe",
        "email": "john@example.com",
        "password": "********",
        "profile": {"firstName": "John", "lastName": "Doe"},
    }

    console.print("[bold]Request Example:[/bold]")
    JsonView(request_data, indent=2).print()
    console.print()

    # Markdown response doc
    response_doc = """### Response

Returns the created user object:"""

    Markdown(response_doc).print()
    console.print()

    # JSON response example
    response_data = {
        "id": 123,
        "username": "johndoe",
        "email": "john@example.com",
        "created_at": "2025-01-15T12:34:56Z",
        "profile": {"firstName": "John", "lastName": "Doe"},
    }

    console.print("[bold]Response Example:[/bold]")
    JsonView(response_data, indent=2).print()
    console.print()

    # Code implementation
    implementation_doc = """### Implementation Example"""

    Markdown(implementation_doc).print()
    console.print()

    impl_code = """import requests

def create_user(username, email, password):
    url = "https://api.example.com/users"
    data = {
        "username": username,
        "email": email,
        "password": password
    }

    response = requests.post(url, json=data)
    response.raise_for_status()

    return response.json()

# Create a new user
user = create_user("johndoe", "john@example.com", "secret")
print(f"Created user: {user['id']}")"""

    CodeBlock.python(impl_code, line_numbers=True).print()
    console.print()


def main():
    """Run all Phase 3 demos."""
    console = get_console()

    console.print(
        "\n[bold magenta]╔════════════════════════════════════════════════╗[/bold magenta]"
    )
    console.print("[bold magenta]║   ChalkBox - Phase 3 Components Demo           ║[/bold magenta]")
    console.print(
        "[bold magenta]╚════════════════════════════════════════════════╝[/bold magenta]\n"
    )

    demo_code_block()
    demo_markdown()
    demo_json_view()
    demo_combined()

    console.print("\n[bold green]✓  Phase 3 demo completed![/bold green]")
    console.print(
        "\nNew components: [cyan]CodeBlock[/cyan], [cyan]Markdown[/cyan], [cyan]JsonView[/cyan]\n"
    )


if __name__ == "__main__":
    main()
