import logging
from pathlib import Path
import tempfile

from chalkbox.logging.bridge import (
    ChalkBoxRichHandler,
    JSONFileHandler,
    StructuredLogger,
    get_logger,
    setup_logging,
)


class TestChalkBoxRichHandler:
    """Tests for ChalkBoxRichHandler."""

    def test_handler_creation(self):
        """Test handler creation."""
        handler = ChalkBoxRichHandler()
        assert handler is not None
        assert handler.rich_tracebacks is True

    def test_handler_default_settings(self):
        """Test default settings are applied."""
        handler = ChalkBoxRichHandler()
        # Verify handler was configured with defaults
        assert handler.theme is not None
        assert handler.highlighter is not None


class TestJSONFileHandler:
    """Tests for JSONFileHandler."""

    def test_handler_creation(self):
        """Test JSON handler creation."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            handler = JSONFileHandler(f.name)
            assert handler.filename == Path(f.name)

    def test_handler_emit(self):
        """Test emitting log record."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            handler = JSONFileHandler(f.name)
            logger = logging.getLogger("test")
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)

            logger.info("Test message")

            # Verify file was written
            assert Path(f.name).exists()
            content = Path(f.name).read_text()
            assert "Test message" in content
            assert "INFO" in content


class TestSetupLogging:
    """Tests for setup_logging function."""

    def setup_method(self):
        """Clear handlers before each test."""
        logging.getLogger().handlers.clear()

    def test_setup_logging_default(self):
        """Test default logging setup."""
        logger = setup_logging()
        assert logger is not None
        assert len(logger.handlers) > 0
        assert logger.level == logging.INFO

    def test_setup_logging_custom_level(self):
        """Test logging with custom level."""
        logger = setup_logging(level="DEBUG")
        assert logger.level == logging.DEBUG

    def test_setup_logging_with_json_file(self):
        """Test logging with JSON file."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            logger = setup_logging(json_file=f.name)
            assert len(logger.handlers) == 2  # Rich + JSON

    def test_setup_logging_clears_existing_handlers(self):
        """Test that setup clears existing handlers."""
        # Add a handler
        logger = logging.getLogger()
        logger.addHandler(logging.NullHandler())
        assert len(logger.handlers) > 0

        # Setup should clear it
        setup_logging()
        # Should have only ChalkBox handler(s)
        assert all(isinstance(h, ChalkBoxRichHandler | JSONFileHandler) for h in logger.handlers)


class TestGetLogger:
    """Tests for get_logger function."""

    def setup_method(self):
        """Clear handlers before each test."""
        logging.getLogger().handlers.clear()

    def test_get_logger_creates_logger(self):
        """Test getting a logger."""
        logger = get_logger("test_logger")
        assert logger is not None
        assert logger.name == "test_logger"

    def test_get_logger_sets_level(self):
        """Test getting logger with custom level."""
        logger = get_logger("test", level="DEBUG")
        assert logger.level == logging.DEBUG

    def test_get_logger_with_handlers_already_present(self):
        """Test get_logger when handlers already exist (e.g., from pytest)."""
        # This test verifies get_logger doesn't error when handlers exist
        logger = get_logger("test")
        assert logger is not None
        assert logger.name == "test"


class TestStructuredLogger:
    """Tests for StructuredLogger."""

    def test_structured_logger_creation(self):
        """Test structured logger creation."""
        logger = logging.getLogger("test")
        structured = StructuredLogger(logger)
        assert structured.logger is logger

    def test_structured_logger_debug(self):
        """Test debug logging with extra data."""
        logger = logging.getLogger("test")
        structured = StructuredLogger(logger)
        # Should not raise
        structured.debug("Debug message", key="value")

    def test_structured_logger_info(self):
        """Test info logging with extra data."""
        logger = logging.getLogger("test")
        structured = StructuredLogger(logger)
        structured.info("Info message", user_id=123)

    def test_structured_logger_warning(self):
        """Test warning logging with extra data."""
        logger = logging.getLogger("test")
        structured = StructuredLogger(logger)
        structured.warning("Warning message", code="W001")

    def test_structured_logger_error(self):
        """Test error logging with extra data."""
        logger = logging.getLogger("test")
        structured = StructuredLogger(logger)
        structured.error("Error message", error_code=500)
