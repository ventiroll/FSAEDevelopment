import unittest

from aer_safety.safety_actions import SafetyActionController


class TestSafetyActionController(unittest.TestCase):
    """tests emergency-state and vehicle-stop behavior."""

    def setUp(self):
        self.controller = SafetyActionController(
            stopped_speed_limit=0.05,
        )

    def test_healthy_system_continues_operation(self):
        action = self.controller.evaluate_system(
            sensors_ready=True,
            command_valid=True,
            communication_healthy=True,
        )

        self.assertFalse(action.emergency_state)
        self.assertFalse(action.vehicle_stopped)
        self.assertTrue(action.autonomous_enabled)
        self.assertEqual(action.errors, [])

    def test_sensor_failure_triggers_safety_state(self):
        action = self.controller.evaluate_system(
            sensors_ready=False,
            command_valid=True,
            communication_healthy=True,
        )

        self.assertTrue(action.emergency_state)
        self.assertTrue(action.vehicle_stopped)
        self.assertFalse(action.autonomous_enabled)
        self.assertEqual(action.throttle_command, 0.0)
        self.assertIn("sensor health failure", action.errors)

    def test_invalid_command_triggers_safety_state(self):
        action = self.controller.evaluate_system(
            sensors_ready=True,
            command_valid=False,
            communication_healthy=True,
        )

        self.assertTrue(action.emergency_state)
        self.assertTrue(action.vehicle_stopped)
        self.assertFalse(action.autonomous_enabled)
        self.assertIn("invalid control command", action.errors)

    def test_communication_failure_triggers_safety_state(self):
        action = self.controller.evaluate_system(
            sensors_ready=True,
            command_valid=True,
            communication_healthy=False,
        )

        self.assertTrue(action.emergency_state)
        self.assertTrue(action.vehicle_stopped)
        self.assertFalse(action.autonomous_enabled)
        self.assertIn("communication failure", action.errors)

    def test_multiple_errors_are_reported(self):
        action = self.controller.evaluate_system(
            sensors_ready=False,
            command_valid=False,
            communication_healthy=False,
        )

        self.assertTrue(action.emergency_state)
        self.assertEqual(len(action.errors), 3)

    def test_vehicle_stop_is_successful(self):
        stop_verified = self.controller.verify_vehicle_stop(
            actual_speed=0.02,
        )

        self.assertTrue(stop_verified)

    def test_vehicle_stop_failure_is_detected(self):
        stop_verified = self.controller.verify_vehicle_stop(
            actual_speed=0.50,
        )

        self.assertFalse(stop_verified)


if __name__ == "__main__":
    unittest.main()