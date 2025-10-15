# Contributing to ChalkBox

Thank you for your interest in contributing to ChalkBox! This document provides guidelines and instructions for contributing to the project.

## Philosophy

ChalkBox is designed to be **tiny and focused**:

- **Simplicity**: Easy to use, easy to understand
- **Reliability**: Graceful error handling with robust fallbacks
- **Composability**: Small, composable pieces that work together
- **Consistency**: Unified theming and API patterns
- **Documentation**: Clear examples and docs

## What I Welcome

I welcome contributions that:

- **Improve existing components** - Bug fixes, performance improvements, better error handling
- **Fix bugs** - Report and fix issues you encounter
- **Enhance documentation** - Improve README, add examples, clarify usage
- **Add tests** - Increase test coverage, add edge cases
- **Report issues** - Bug reports, feature requests, documentation issues
- **Improve demos** - Better examples, new use cases, workflow demonstrations

## What I Don't Accept

Please **do not** submit pull requests that:

- **Add new components** without prior discussion (open an issue first)
- **Change core API** without RFC (Request for Comments)
- **Add heavy dependencies** - Keep ChalkBox lightweight
- **Break backward compatibility** - Maintain API stability
- **Remove fail-safe behavior** - Components must handle errors gracefully

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/bulletinmybeard/chalkbox
cd chalkbox
```

### 2. Set Up Development Environment

**Requirements:**

- Python 3.12+ (ChalkBox uses modern Python features like the `type` statement)
- Poetry for dependency management

```bash
# Verify Python version
python --version  # Should be 3.12 or higher

# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### 3. Run Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=chalkbox

# Run specific test file
poetry run pytest tests/test_alert.py
```

### 4. Check Code Quality

```bash
# Format code
poetry run ruff format chalkbox/ tests/

# Check linting
poetry run ruff check chalkbox/ tests/

# Auto-fix linting issues
poetry run ruff check --fix chalkbox/ tests/

# Format Markdown files
poetry run mdformat *.md docs/ demos/

# Type checking
poetry run mypy chalkbox/

# Security check
poetry run bandit -r chalkbox/
```

## Development Workflow

### Making Changes

1. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/my-improvement
   ```
2. **Make your changes** following coding standards (see below)
3. **Add tests** for new functionality or bug fixes
4. **Run the test suite** and ensure all tests pass
5. **Check code quality** with Ruff, MyPy, Bandit, and mdformat
6. **Update documentation** if needed (README, docstrings, examples)

### Coding Standards

**Python Style**:

- Follow PEP 8 (enforced by Ruff)
- Maximum line length: 100 characters
- Use modern type hints (Python 3.12+ style: `dict[str, str]` not `Dict[str, str]`)
- Prefer explicit over implicit

**Markdown Style**:

- CommonMark compliant (enforced by mdformat)
- Maximum line length: 100 characters (matches Python)
- Consistent bullet points and list formatting
- Use fenced code blocks with language identifiers

**Component Design**:

- **Handle errors gracefully** - Catch expected exceptions, return safe fallbacks
- **Support non-TTY** - Components must work in CI/CD
- **Return Rich renderables** - Implement `__rich__()` method
- **Use context managers** - For stateful components
- **Access theme via `get_theme()`** - For consistent styling
- **Use `get_console()`** - For singleton console access

**Example fail-safe pattern**:

```python
def my_component(data: dict) -> Panel:
    """Create component from data.

    Handles invalid input gracefully by returning an error display.
    """
    try:
        # Try to process data
        content = process_data(data)
        return Panel(content, title="Success")
    except Exception as e:
        # Fail gracefully with informative message
        console = get_console()
        console.log(f"[yellow]Warning:[/yellow] Could not process data: {e}")
        return Panel("[dim]No data available[/dim]", title="Error", border_style="red")
```

**Testing**:

- Write tests for new features and bug fixes
- Test both success and failure cases
- Test non-TTY behavior (set `console.is_terminal = False`)
- Use pytest fixtures for common setup
- Aim for >90% code coverage

**Documentation**:

- Add docstrings to all public functions and classes
- Include examples in docstrings for complex features
- Update README if adding new functionality
- Add demo scripts for new components

### Commit Messages

Use clear, descriptive commit messages:

```
Good:
- Fix Spinner duplicate output when transient=False
- Add secret masking to KeyValue component
- Update README with installation instructions

Bad:
- Fix bug
- Update code
- Changes
```

Format: `<type>: <description>`

Types:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions or modifications
- `refactor`: Code refactoring
- `style`: Formatting changes (no logic change)
- `chore`: Maintenance tasks

### Submitting a Pull Request

1. **Push your branch** to your fork:
   ```bash
   git push origin feature/my-improvement
   ```
2. **Open a Pull Request** on GitHub with:
   - Clear title describing the change
   - Description of what you changed and why
   - Reference to any related issues (`Fixes #123`)
   - Screenshots for UI changes (if applicable)
3. **Respond to feedback** - Maintainers may request changes
4. **Keep your PR updated** - Rebase if needed to resolve conflicts

## Proposing New Components

If you want to add a new component:

1. **Open an issue first** with:
   - Component name and purpose
   - Example usage code
   - Explanation of why it belongs in ChalkBox (vs user-defined)
   - How it fits with existing components
2. **Wait for feedback** before implementing
3. **Discuss API design** with maintainers
4. **Get approval** before submitting PR

## Reporting Issues

### Bug Reports

Include:

- ChalkBox version (`poetry show chalkbox`)
- Python version (`python --version`)
- Operating system
- Minimal code to reproduce
- Expected behavior
- Actual behavior
- Error messages (if any)

### Feature Requests

Include:

- Clear description of the feature
- Use case and motivation
- Example code showing desired usage
- Why it belongs in ChalkBox vs user code

## Building and Publishing

### Local Test Build

Before publishing to PyPI, test the build locally:

```bash
# Clean previous builds
rm -rf dist/

# Build package
poetry build

# Create test virtual environment
python -m venv test_chalkbox_venv
source test_chalkbox_venv/bin/activate

# Install from local build
pip install dist/chalkbox-*.whl

# Test import and functionality
python -c "from chalkbox import Alert; print(Alert.success('Build works!'))"

# Deactivate and clean up
deactivate
rm -rf test_chalkbox_venv
```

## Development Tips

### Running Examples

The repository includes demos for testing and learning:

**Component Demos** - Individual component examples:

```bash
poetry run python demos/components/divider.py
poetry run python demos/components/section.py
poetry run python demos/components/stepper.py
poetry run python demos/components/prompt.py
poetry run python demos/components/tree.py
poetry run python demos/components/keyvalue.py
poetry run python demos/components/table.py
poetry run python demos/components/status.py
poetry run python demos/components/spinner.py
poetry run python demos/components/column_layout.py
poetry run python demos/components/code_block.py
poetry run python demos/components/json_view.py
poetry run python demos/components/progress.py
poetry run python demos/components/markdown.py
poetry run python demos/components/multipanel.py
```

**Theming Demo** - Showcase theming with custom theme files:

```bash
poetry run python demos/theming/demo.py         # Default theme
poetry run python demos/theming/demo.py dark    # Dark theme
poetry run python demos/theming/demo.py light   # Light theme
```

**Real-World Showcases** - Multi-component demonstrations:

```bash
poetry run python demos/showcases/responsive_layouts.py
poetry run python demos/showcases/layout_components.py
poetry run python demos/showcases/basic_components.py
poetry run python demos/showcases/interactive_components.py
poetry run python demos/showcases/dashboard_builder.py
poetry run python demos/showcases/content_components.py
poetry run python demos/showcases/live_components.py
```

**Workflow Simulations** - Complete application patterns:

```bash
poetry run python demos/workflows/api_testing.py
poetry run python demos/workflows/ci_pipeline.py
poetry run python demos/workflows/code_quality.py
poetry run python demos/workflows/comprehensive_demo.py
poetry run python demos/workflows/data_processing.py
poetry run python demos/workflows/dependency_management.py
poetry run python demos/workflows/dev_environment.py
poetry run python demos/workflows/diagnostic_tool.py
poetry run python demos/workflows/environment_check.py
poetry run python demos/workflows/file_operations.py
poetry run python demos/workflows/log_analysis.py
poetry run python demos/workflows/project_setup.py
poetry run python demos/workflows/release_deployment.py
poetry run python demos/workflows/system_installation.py
```

### Testing Theme Changes

```bash
# Create test theme file
mkdir -p ~/.chalkbox
cat > ~/.chalkbox/theme.toml << EOF
[colors]
primary = "magenta"
success = "bright_green"

[glyphs]
success = ""
EOF

# Run demo to see changes
poetry run python demos/components/alert.py
```

### Debugging Components

```python
from chalkbox import get_console

console = get_console()

# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Test component
from chalkbox import Alert
console.print(Alert.success("Debug message"))

# Check if terminal is detected
print(f"Is terminal: {console.is_terminal}")
print(f"Console size: {console.size}")
```

Thank you for contributing to ChalkBox! \w
