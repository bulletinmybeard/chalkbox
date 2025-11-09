import time

import pytest

from chalkbox.components.dynamic_progress import DynamicProgress


class TestDynamicProgress:
    """Tests for DynamicProgress component."""

    def test_creation(self):
        """Test basic dynamic progress creation."""
        progress = DynamicProgress()
        assert progress.transient is False
        assert progress.show_section_titles is False
        assert progress.tasks == {}
        assert progress.completed_tasks == []
        assert progress.active is None
        assert progress.completed is None

    def test_creation_with_options(self):
        """Test dynamic progress with custom settings."""
        progress = DynamicProgress(transient=True, show_section_titles=True)
        assert progress.transient is True
        assert progress.show_section_titles is True

    def test_add_task_outside_context(self):
        """Test that add_task raises error outside context manager."""
        progress = DynamicProgress()
        with pytest.raises(RuntimeError, match="Progress not started"):
            progress.add_task("Test task")

    def test_context_manager_lifecycle(self):
        """Test context manager properly initializes and cleans up."""
        progress = DynamicProgress()
        assert progress.active is None
        assert progress.completed is None
        assert progress._live is None

        with progress:
            assert progress.active is not None
            assert progress.completed is not None
            assert progress._live is not None

        assert progress.active is not None
        assert progress.completed is not None

    def test_add_task_returns_stable_id(self):
        """Test that add_task returns stable external task IDs."""
        with DynamicProgress() as progress:
            task1 = progress.add_task("Task 1", total=100)
            task2 = progress.add_task("Task 2", total=100)

            assert task1 != task2
            assert task1 in progress.tasks
            assert task2 in progress.tasks

    def test_task_metadata_stored(self):
        """Test that task metadata is properly stored."""
        with DynamicProgress() as progress:
            task_id = progress.add_task("Test task", total=100)

            assert task_id in progress.tasks
            task_data = progress.tasks[task_id]
            assert task_data["description"] == "Test task"
            assert task_data["total"] == 100
            assert "start_ms" in task_data
            assert "active_id" in task_data

    def test_update_task(self):
        """Test updating task progress."""
        with DynamicProgress() as progress:
            task_id = progress.add_task("Test task", total=100)

            progress.update(task_id, advance=50)

            assert task_id in progress.tasks
            assert len(progress.completed_tasks) == 0

    def test_update_unknown_task_raises_error(self):
        """Test that updating unknown task raises ValueError."""
        with DynamicProgress() as progress, pytest.raises(ValueError, match="Unknown task ID"):
            progress.update(999, advance=10)

    def test_task_completion_moves_to_completed(self):
        """Test that completed tasks move to completed section."""
        with DynamicProgress() as progress:
            task_id = progress.add_task("Fast task", total=100)

            progress.update(task_id, completed=100)

            time.sleep(0.01)

            assert task_id not in progress.tasks
            assert len(progress.completed_tasks) == 1

            completed_task = progress.completed_tasks[0]
            assert completed_task["description"] == "Fast task"
            assert "finish_ms" in completed_task
            assert "duration_ms" in completed_task

    def test_completed_tasks_sorted_by_duration(self):
        """Test that completed tasks are sorted by duration (fastest first)."""
        with DynamicProgress() as progress:
            # Add tasks
            task1 = progress.add_task("Slow task", total=100)
            task2 = progress.add_task("Fast task", total=100)
            task3 = progress.add_task("Medium task", total=100)

            # Complete tasks with different durations
            time.sleep(0.05)  # 50ms
            progress.update(task2, completed=100)  # Fast: ~50ms

            time.sleep(0.05)  # Additional 50ms
            progress.update(task3, completed=100)  # Medium: ~100ms

            time.sleep(0.05)  # Additional 50ms
            progress.update(task1, completed=100)  # Slow: ~150ms

            assert len(progress.completed_tasks) == 3
            assert progress.completed_tasks[0]["description"] == "Fast task"
            assert progress.completed_tasks[1]["description"] == "Medium task"
            assert progress.completed_tasks[2]["description"] == "Slow task"

            durations = [t["duration_ms"] for t in progress.completed_tasks]
            assert durations[0] < durations[1] < durations[2]

    def test_millisecond_precision_ordering(self):
        """Test that millisecond precision enables correct ordering."""
        with DynamicProgress() as progress:
            # Add tasks
            task1 = progress.add_task("Task 1", total=100)
            task2 = progress.add_task("Task 2", total=100)

            # Complete tasks with very small time difference (< 1 second)
            time.sleep(0.01)  # 10ms
            progress.update(task1, completed=100)

            time.sleep(0.015)  # 15ms
            progress.update(task2, completed=100)

            assert len(progress.completed_tasks) == 2
            assert progress.completed_tasks[0]["description"] == "Task 1"
            assert progress.completed_tasks[1]["description"] == "Task 2"

            # Duration difference should be ~15ms
            duration_diff = (
                progress.completed_tasks[1]["duration_ms"]
                - progress.completed_tasks[0]["duration_ms"]
            )
            assert 10 < duration_diff < 30  # Allow some timing variance

    def test_update_description(self):
        """Test updating task description."""
        with DynamicProgress() as progress:
            task_id = progress.add_task("Original", total=100)

            progress.update(task_id, description="Updated")

            assert progress.tasks[task_id]["description"] == "Updated"

    def test_remove_task_from_active(self):
        """Test removing task from active section."""
        with DynamicProgress() as progress:
            task_id = progress.add_task("Test task", total=100)

            progress.remove_task(task_id)

            assert task_id not in progress.tasks

    def test_multiple_tasks_parallel_completion(self):
        """Test multiple tasks completing at different times."""
        with DynamicProgress() as progress:
            # Add 5 tasks
            tasks = [progress.add_task(f"Task {i}", total=100) for i in range(5)]

            # Complete in random order with delays
            delays = [0.03, 0.01, 0.05, 0.02, 0.04]  # Milliseconds
            for task_id, delay in zip(tasks, delays, strict=False):
                time.sleep(delay)
                progress.update(task_id, completed=100)

            assert len(progress.completed_tasks) == 5
            assert len(progress.tasks) == 0

            durations = [t["duration_ms"] for t in progress.completed_tasks]
            assert durations == sorted(durations)

    def test_empty_progress_group(self):
        """Test that empty progress doesn't error."""
        with DynamicProgress() as progress:
            group = progress._build_group()

            assert group is not None


class TestMinuteSecondsColumn:
    """Test custom time column format."""

    def test_minute_seconds_format(self):
        """Test that MinuteSecondsColumn formats time as M:SS."""
        from chalkbox.components.progress_columns import MinuteSecondsColumn

        class MockTask:
            def __init__(self, elapsed_seconds):
                self.elapsed = elapsed_seconds

        column = MinuteSecondsColumn()

        # Test various durations
        # 5 seconds
        result = column.render(MockTask(5.0))
        assert "0:05" in str(result)

        # 65 seconds (1:05)
        result = column.render(MockTask(65.0))
        assert "1:05" in str(result)

        # 125 seconds (2:05)
        result = column.render(MockTask(125.0))
        assert "2:05" in str(result)

        # 0 seconds
        result = column.render(MockTask(0.0))
        assert "0:00" in str(result)

    def test_minute_seconds_no_milliseconds_displayed(self):
        """Test that milliseconds are not shown to user."""
        from chalkbox.components.progress_columns import MinuteSecondsColumn

        class MockTask:
            def __init__(self, elapsed_seconds):
                self.elapsed = elapsed_seconds

        column = MinuteSecondsColumn()

        # 5.789 seconds should show as 0:05, not 0:05.789
        result = column.render(MockTask(5.789))
        result_str = str(result)

        # Should have M:SS format only
        assert "0:05" in result_str
        assert "." not in result_str  # No decimal point (no milliseconds)
