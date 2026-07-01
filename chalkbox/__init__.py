try:
    from importlib.metadata import PackageNotFoundError, version

    try:
        __version__ = version("chalkbox")
    except PackageNotFoundError:
        __version__ = "2.4.0"
except ImportError:
    __version__ = "2.4.0"

from .components.alert import Alert
from .components.align import Align
from .components.bar import Bar
from .components.code import CodeBlock
from .components.columns import ColumnLayout
from .components.divider import Divider
from .components.dynamic_progress import DynamicProgress
from .components.json_view import JsonView
from .components.kv import KeyValue
from .components.layout import MultiPanel
from .components.markdown import Markdown
from .components.padding import Padding
from .components.progress import Progress
from .components.progress_columns import MinuteSecondsColumn
from .components.prompt import Confirm, FloatInput, Input, IntInput, NumberInput, Select
from .components.section import Section
from .components.spinner import Spinner
from .components.status import Status, status
from .components.status_card import StatusCard
from .components.stepper import Stepper
from .components.table import Table
from .components.tree import Tree
from .core.console import Console, get_console, reset_console
from .core.theme import Theme, get_theme, reset_theme, set_theme
from .live.dashboard import Dashboard, DashboardSection
from .live.wrapper import LiveComponent, LiveLayout, LiveTable
from .logging.bridge import (
    StructuredLogger,
    get_logger,
    get_structured_logger,
    setup_logging,
)

__all__ = [
    "Align",
    "Alert",
    "Bar",
    "CodeBlock",
    "ColumnLayout",
    "Confirm",
    "Console",
    "Dashboard",
    "DashboardSection",
    "Divider",
    "DynamicProgress",
    "FloatInput",
    "Input",
    "IntInput",
    "JsonView",
    "KeyValue",
    "LiveComponent",
    "LiveLayout",
    "LiveTable",
    "Markdown",
    "MinuteSecondsColumn",
    "MultiPanel",
    "NumberInput",
    "Padding",
    "Progress",
    "Section",
    "Select",
    "Spinner",
    "Status",
    "StatusCard",
    "Stepper",
    "StructuredLogger",
    "Table",
    "Theme",
    "Tree",
    "__version__",
    "get_console",
    "get_logger",
    "get_structured_logger",
    "get_theme",
    "reset_console",
    "reset_theme",
    "set_theme",
    "setup_logging",
    "status",
]
