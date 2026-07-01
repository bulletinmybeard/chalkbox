from collections.abc import Generator

import pytest

from chalkbox.core.console import reset_console
import chalkbox.core.theme as theme_module
from chalkbox.core.theme import Theme, reset_theme


@pytest.fixture
def isolated_theme() -> Generator[None, None, None]:
    """Reset global theme before and after a test."""
    original: Theme | None = theme_module._theme
    reset_theme()
    yield
    theme_module._theme = original


@pytest.fixture
def isolated_console() -> Generator[None, None, None]:
    """Reset global console before and after a test."""
    reset_console()
    yield
    reset_console()
