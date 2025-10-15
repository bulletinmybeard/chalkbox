from chalkbox import Stepper
from chalkbox.components.stepper import StepStatus


class TestStepper:
    """Tests for Stepper component."""

    def test_stepper_creation(self):
        """Test basic stepper creation."""
        stepper = Stepper(title="Test Steps")
        assert stepper.title == "Test Steps"
        assert len(stepper._steps) == 0

    def test_stepper_add_steps(self):
        """Test adding steps."""
        stepper = Stepper()
        idx1 = stepper.add_step("Step 1", "Description 1")
        idx2 = stepper.add_step("Step 2")

        assert idx1 == 0
        assert idx2 == 1
        assert len(stepper._steps) == 2
        assert stepper._steps[0].description == "Description 1"

    def test_stepper_from_list(self):
        """Test creating stepper from list."""
        steps = ["Step 1", "Step 2", "Step 3"]
        stepper = Stepper.from_list(steps)

        assert len(stepper._steps) == 3
        assert all(s.status == StepStatus.PENDING for s in stepper._steps)

    def test_stepper_status_changes(self):
        """Test step status changes."""
        stepper = Stepper()
        stepper.add_steps(["Step 1", "Step 2", "Step 3"])

        # Start step
        stepper.start(0)
        assert stepper._steps[0].status == StepStatus.RUNNING

        # Complete step
        stepper.complete(0)
        assert stepper._steps[0].status == StepStatus.DONE

        # Fail step
        stepper.fail(1, "Error message")
        assert stepper._steps[1].status == StepStatus.FAILED

        # Skip step
        stepper.skip(2)
        assert stepper._steps[2].status == StepStatus.SKIPPED

    def test_stepper_next(self):
        """Test stepping through steps."""
        stepper = Stepper()
        stepper.add_steps(["Step 1", "Step 2", "Step 3"])

        # Next should start first step
        idx = stepper.next()
        assert idx == 0
        assert stepper._steps[0].status == StepStatus.RUNNING

        # Next should complete current and start next
        idx = stepper.next()
        assert idx == 1
        assert stepper._steps[0].status == StepStatus.DONE
        assert stepper._steps[1].status == StepStatus.RUNNING
