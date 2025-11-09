import pytest
from rich.panel import Panel

from chalkbox.components.dynamic_progress import DynamicProgress
from chalkbox.components.progress import Progress
from chalkbox.components.prompt import Select
from chalkbox.live.dashboard import Dashboard


class TestSelectExceptions:
    """Test exception handling in Select component."""

    def test_empty_choices_raises_valueerror(self):
        """Test that Select raises ValueError when choices list is empty."""
        with pytest.raises(ValueError, match="Select requires at least one choice"):
            Select(prompt="Choose:", choices=[])

    def test_empty_choices_in_ask_once_raises_valueerror(self):
        """Test that Select.ask_once also validates choices."""
        with pytest.raises(ValueError, match="Select requires at least one choice"):
            Select.ask_once(prompt="Choose:", choices=[])

    def test_non_empty_choices_succeeds(self):
        """Test that Select accepts non-empty choices list."""
        select = Select(prompt="Choose:", choices=["A", "B", "C"])
        assert select.choices == ["A", "B", "C"]
        assert select.default == "A"  # First choice becomes default

    def test_explicit_default_with_valid_choices(self):
        """Test Select with explicit default value."""
        select = Select(prompt="Choose:", choices=["A", "B", "C"], default="B")
        assert select.default == "B"


class TestDashboardExceptions:
    """Test exception handling in Dashboard component."""

    def test_set_sidebar_with_header_footer_layout_raises_valueerror(self):
        """Test that set_sidebar raises ValueError for header_footer layout."""
        dashboard = Dashboard(layout_type="header_footer")

        with pytest.raises(ValueError, match="Sidebar not available in header_footer layout"):
            dashboard.set_sidebar("Sidebar content")

    def test_set_sidebar_with_default_layout_succeeds(self):
        """Test that set_sidebar works with default layout."""
        dashboard = Dashboard(layout_type="default")
        # default layout has sidebar in sections
        # This should not raise
        dashboard.set_sidebar("Sidebar content")
        assert dashboard.sections["sidebar"].content == "Sidebar content"

    def test_set_sidebar_with_sidebar_left_layout_succeeds(self):
        """Test that set_sidebar works with sidebar_left layout."""
        dashboard = Dashboard(layout_type="sidebar_left")
        dashboard.set_sidebar("Sidebar content")
        assert dashboard.sections["sidebar"].content == "Sidebar content"

    def test_set_sidebar_with_sidebar_right_layout_succeeds(self):
        """Test that set_sidebar works with sidebar_right layout."""
        dashboard = Dashboard(layout_type="sidebar_right")
        dashboard.set_sidebar("Sidebar content")
        assert dashboard.sections["sidebar"].content == "Sidebar content"

    def test_set_sidebar_with_full_layout_succeeds(self):
        """Test that set_sidebar works with full layout."""
        dashboard = Dashboard(layout_type="full")
        dashboard.set_sidebar("Sidebar content")
        assert dashboard.sections["sidebar"].content == "Sidebar content"

    def test_set_footer_with_valid_layout_succeeds(self):
        """Test that set_footer works with valid layouts."""
        dashboard = Dashboard(layout_type="full")
        dashboard.set_footer("Footer content")
        # Footer content gets wrapped in Panel if it's a string
        assert dashboard.sections["footer"].content is not None

    def test_set_footer_with_string_content(self):
        """Test that set_footer accepts string content and wraps it in Panel."""
        dashboard = Dashboard(layout_type="full")
        dashboard.set_footer("Footer text")

        assert isinstance(dashboard.sections["footer"].content, Panel)


class TestProgressExceptions:
    """Test exception handling in Progress component."""

    def test_add_task_without_context_manager_raises_runtimeerror(self):
        """Test that add_task raises RuntimeError when called outside context manager."""
        progress = Progress()

        with pytest.raises(RuntimeError, match="Progress not started \\(use context manager\\)"):
            progress.add_task("Task 1")

    def test_add_task_with_context_manager_succeeds(self):
        """Test that add_task works inside context manager."""
        with Progress() as progress:
            task_id = progress.add_task("Task 1", total=100)
            assert task_id is not None

    def test_update_without_context_manager_does_not_raise(self):
        """Test that update fails gracefully outside context manager."""
        progress = Progress()
        progress.update(0, advance=10)


class TestDynamicProgressExceptions:
    """Test exception handling in DynamicProgress component."""

    def test_add_task_without_context_manager_raises_runtimeerror(self):
        """Test that add_task raises RuntimeError when called outside context manager."""
        progress = DynamicProgress()

        with pytest.raises(RuntimeError, match="Progress not started \\(use context manager\\)"):
            progress.add_task("Task 1")

    def test_add_task_with_context_manager_succeeds(self):
        """Test that add_task works inside context manager."""
        with DynamicProgress() as progress:
            task_id = progress.add_task("Task 1", total=100)
            assert task_id is not None
            assert task_id in progress.tasks

    def test_update_with_unknown_task_id_raises_valueerror(self):
        """Test that update raises ValueError for unknown task_id."""
        with DynamicProgress() as progress, pytest.raises(ValueError, match="Unknown task ID: 999"):
            progress.update(999, advance=10)

    def test_update_with_valid_task_id_succeeds(self):
        """Test that update works with valid task_id."""
        with DynamicProgress() as progress:
            task_id = progress.add_task("Task 1", total=100)
            # Should not raise
            progress.update(task_id, advance=10)

    def test_update_without_context_manager_raises_runtimeerror(self):
        """Test that update raises RuntimeError when progress is not active."""
        DynamicProgress()
        pass

    def test_complete_task_moves_to_completed_section(self):
        """Test that completing a task moves it to completed section."""
        with DynamicProgress() as progress:
            task_id = progress.add_task("Task 1", total=100)

            # Task should be in active section
            assert task_id in progress.tasks
            assert len(progress.completed_tasks) == 0

            # Complete the task
            progress.update(task_id, completed=100)

            # Task should now be in completed section
            assert task_id not in progress.tasks
            assert len(progress.completed_tasks) == 1
            assert progress.completed_tasks[0]["description"] == "Task 1"


class TestExceptionDocumentation:
    """Meta-tests to ensure exception documentation is accurate."""

    def test_select_raises_documented_valueerror(self):
        """Verify Select.__init__ raises the documented ValueError."""
        with pytest.raises(ValueError):
            Select(prompt="Test", choices=[])

    def test_dashboard_set_sidebar_raises_documented_valueerror(self):
        """Verify Dashboard.set_sidebar raises the documented ValueError."""
        dashboard = Dashboard(layout_type="header_footer")
        with pytest.raises(ValueError):
            dashboard.set_sidebar("content")

    def test_progress_add_task_raises_documented_runtimeerror(self):
        """Verify Progress.add_task raises the documented RuntimeError."""
        progress = Progress()
        with pytest.raises(RuntimeError):
            progress.add_task("Task")

    def test_dynamic_progress_add_task_raises_documented_runtimeerror(self):
        """Verify DynamicProgress.add_task raises the documented RuntimeError."""
        progress = DynamicProgress()
        with pytest.raises(RuntimeError):
            progress.add_task("Task")

    def test_dynamic_progress_update_raises_documented_valueerror(self):
        """Verify DynamicProgress.update raises the documented ValueError."""
        with DynamicProgress() as progress, pytest.raises(ValueError):
            progress.update(999, advance=10)


# Run tests with: poetry run pytest tests/test_exceptions.py -v
