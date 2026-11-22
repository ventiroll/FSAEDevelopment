import unittest

from aer_bridge.control_logic import (
    ActuatorFeedback,
    ControlCommand,
    ControlValidator,
)


class TestControlValidator(unittest.TestCase):
    """tests steering, speed, and actuator validation."""

    def setUp(self):
        self.validator = ControlValidator()

    def test_valid_command_is_accepted(self):
        result = self.validator.validate_command(
            ControlCommand(
                steering_radians=0.2,
                speed_meters_per_second=3.0,
            )
        )

        self.assertTrue(result.valid)
        self.assertEqual(result.steering_signal, 0.2)
        self.assertEqual(result.throttle_signal, 0.6)
        self.assertIsNone(result.error)

    def test_unsafe_steering_command_is_rejected(self):
        result = self.validator.validate_command(
            ControlCommand(
                steering_radians=0.8,
                speed_meters_per_second=3.0,
            )
        )

        self.assertFalse(result.valid)
        self.assertIsNone(result.steering_signal)
        self.assertEqual(
            result.error,
            "steering command exceeds the safe limit",
        )

    def test_unsafe_speed_command_is_rejected(self):
        result = self.validator.validate_command(
            ControlCommand(
                steering_radians=0.2,
                speed_meters_per_second=6.0,
            )
        )

        self.assertFalse(result.valid)
        self.assertIsNone(result.throttle_signal)
        self.assertEqual(
            result.error,
            "speed command exceeds the safe limit",
        )

    def test_negative_speed_is_rejected(self):
        result = self.validator.validate_command(
            ControlCommand(
                steering_radians=0.0,
                speed_meters_per_second=-1.0,
            )
        )

        self.assertFalse(result.valid)

    def test_matching_feedback_does_not_trigger_failure(self):
        failure_detected = self.validator.detect_control_failure(
            command=ControlCommand(
                steering_radians=0.2,
                speed_meters_per_second=3.0,
            ),
            feedback=ActuatorFeedback(
                steering_radians=0.21,
                speed_meters_per_second=3.1,
            ),
            elapsed_seconds=0.3,
        )

        self.assertFalse(failure_detected)

    def test_incorrect_feedback_triggers_failure(self):
        failure_detected = self.validator.detect_control_failure(
            command=ControlCommand(
                steering_radians=0.2,
                speed_meters_per_second=3.0,
            ),
            feedback=ActuatorFeedback(
                steering_radians=0.0,
                speed_meters_per_second=0.0,
            ),
            elapsed_seconds=0.3,
        )

        self.assertTrue(failure_detected)

    def test_feedback_before_timeout_does_not_trigger_failure(self):
        failure_detected = self.validator.detect_control_failure(
            command=ControlCommand(
                steering_radians=0.2,
                speed_meters_per_second=3.0,
            ),
            feedback=ActuatorFeedback(
                steering_radians=0.0,
                speed_meters_per_second=0.0,
            ),
            elapsed_seconds=0.1,
        )

        self.assertFalse(failure_detected)


if __name__ == "__main__":
    unittest.main()