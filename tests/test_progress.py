import pytest

from chalkbox.components.progress import Progress


class TestProgress:
    """Tests for Progress component."""

    def test_progress_creation(self):
        """Test basic progress creation."""
        progress = Progress()
        assert progress.transient is False
        assert progress.expand is False
        assert progress.auto_refresh is True
        assert progress._progress is None

    def test_progress_custom_settings(self):
        """Test progress with custom settings."""
        progress = Progress(transient=True, expand=True, auto_refresh=False)
        assert progress.transient is True
        assert progress.expand is True
        assert progress.auto_refresh is False

    def test_progress_add_task_outside_context(self):
        """Test that add_task raises error outside context manager."""
        progress = Progress()
        with pytest.raises(RuntimeError, match="Progress not started"):
            progress.add_task("Test task")

    def test_progress_create_simple(self):
        """Test simple progress factory."""
        progress = Progress.create_simple("Processing...")
        assert progress.transient is True

    def test_progress_create_download(self):
        """Test download progress factory."""
        progress = Progress.create_download()
        assert progress._progress is not None
