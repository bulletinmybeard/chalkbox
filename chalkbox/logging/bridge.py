import json
import logging
from pathlib import Path
from threading import Lock
from typing import Any

from rich.logging import RichHandler
from rich.text import Text

from ..core.console import get_console
from ..core.theme import get_theme


class ChalkBoxRichHandler(RichHandler):
    """Extended RichHandler with ChalkBox theming."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize with ChalkBox defaults."""
        console = kwargs.pop("console", get_console())
        kwargs.setdefault("rich_tracebacks", True)
        kwargs.setdefault("markup", True)
        kwargs.setdefault("show_time", True)
        kwargs.setdefault("show_level", True)
        kwargs.setdefault("show_path", True)

        self.theme = get_theme()

        super().__init__(console=console, **kwargs)

    def get_level_text(self, record: logging.LogRecord) -> Text:
        """Render log level with ChalkBox theme colors."""
        level_name = record.levelname
        style_map = {
            "debug": self.theme.get_style("debug"),
            "info": self.theme.get_style("info"),
            "warning": self.theme.get_style("warning"),
            "error": self.theme.get_style("error"),
            "critical": self.theme.get_style("critical"),
        }
        style = style_map.get(level_name.lower(), self.theme.get_style("default"))
        return Text.styled(level_name.ljust(8), style)


class JSONFileHandler(logging.Handler):
    """Handler that writes JSON logs to a file for machine parsing."""

    _file_lock = Lock()

    def __init__(self, filename: str, **kwargs: Any) -> None:
        """Initialize JSON file handler."""
        super().__init__(**kwargs)
        self.filename = Path(filename)
        self.filename.parent.mkdir(parents=True, exist_ok=True)

    def emit(self, record: logging.LogRecord) -> None:
        """Write log record as JSON."""
        try:
            log_entry = {
                "timestamp": record.created,
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
            }

            if hasattr(record, "extra_data"):
                log_entry["extra"] = record.extra_data

            if record.exc_info:
                import traceback

                log_entry["exception"] = traceback.format_exception(*record.exc_info)

            with self._file_lock, open(self.filename, "a") as f:
                json.dump(log_entry, f)
                f.write("\n")
        except Exception:
            self.handleError(record)


def setup_logging(
    level: str = "INFO",
    format: str | None = None,
    json_file: str | None = None,
    show_time: bool = True,
    show_level: bool = True,
    show_path: bool = True,
    rich_tracebacks: bool = True,
    *,
    replace_handlers: bool = True,
) -> logging.Logger:
    """Setup opinionated logging configuration."""
    root_logger = logging.getLogger()

    if replace_handlers:
        root_logger.handlers.clear()

    log_level = getattr(logging, level.upper(), logging.INFO)
    root_logger.setLevel(log_level)

    rich_handler = ChalkBoxRichHandler(
        show_time=show_time,
        show_level=show_level,
        show_path=show_path,
        rich_tracebacks=rich_tracebacks,
    )

    if format:
        rich_handler.setFormatter(logging.Formatter(format))

    root_logger.addHandler(rich_handler)

    if json_file:
        json_handler = JSONFileHandler(json_file)
        json_handler.setLevel(log_level)
        root_logger.addHandler(json_handler)

    return root_logger


def get_logger(name: str, level: str | None = None, **kwargs: Any) -> logging.Logger:
    """Get a logger with ChalkBox configuration."""
    if not logging.getLogger().handlers:
        setup_logging(level=level or "INFO", **kwargs)

    logger = logging.getLogger(name)

    if level:
        log_level = getattr(logging, level.upper(), logging.INFO)
        logger.setLevel(log_level)

    return logger


class StructuredLogger:
    """Logger wrapper for structured logging with extra data."""

    def __init__(self, logger: logging.Logger):
        """Initialize with a logger."""
        self.logger = logger

    def log(self, level: str, message: str, **extra_data: Any) -> None:
        """Log with structured extra data."""
        log_method = getattr(self.logger, level.lower())
        log_method(message, extra={"extra_data": extra_data})

    def debug(self, message: str, **extra_data: Any) -> None:
        """Log debug with extra data."""
        self.log("debug", message, **extra_data)

    def info(self, message: str, **extra_data: Any) -> None:
        """Log info with extra data."""
        self.log("info", message, **extra_data)

    def warning(self, message: str, **extra_data: Any) -> None:
        """Log warning with extra data."""
        self.log("warning", message, **extra_data)

    def error(self, message: str, **extra_data: Any) -> None:
        """Log error with extra data."""
        self.log("error", message, **extra_data)


def get_structured_logger(name: str, level: str | None = None, **kwargs: Any) -> StructuredLogger:
    """Get a structured logger with ChalkBox configuration."""
    return StructuredLogger(get_logger(name, level=level, **kwargs))
