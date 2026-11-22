import unittest

from aer_bridge.uart_protocol import UartCommandBuilder


class TestUartCommandBuilder(unittest.TestCase):
    """tests normal and emergency uart commands."""

    def setUp(self):
        self.builder = UartCommandBuilder()

    def test_normal_command_contains_controls(self):
        payload = self.builder.build_payload(
            speed_meters_per_second=3.0,
            steering_radians=0.05,
            emergency_state=False,
        )

        self.assertIn("SPEED=3.00m/s", payload)
        self.assertIn("STEER=0.050rad", payload)
        self.assertNotIn("EMERGENCY_STATE=1", payload)

    def test_emergency_command_sets_speed_to_zero(self):
        payload = self.builder.build_payload(
            speed_meters_per_second=3.0,
            steering_radians=0.05,
            emergency_state=True,
        )

        self.assertIn("EMERGENCY_STATE=1", payload)
        self.assertIn("SPEED=0.0m/s", payload)
        self.assertIn("BRAKE=MAX", payload)
        self.assertIn("EBS_ACTUATE", payload)

    def test_emergency_overrides_normal_speed(self):
        payload = self.builder.build_payload(
            speed_meters_per_second=5.0,
            steering_radians=0.4,
            emergency_state=True,
        )

        self.assertIn("SPEED=0.0m/s", payload)
        self.assertNotIn("SPEED=5.00m/s", payload)

    def test_emergency_blocks_normal_steering(self):
        payload = self.builder.build_payload(
            speed_meters_per_second=2.0,
            steering_radians=0.4,
            emergency_state=True,
        )

        self.assertNotIn("STEER=0.400rad", payload)

    def test_normal_command_does_not_request_emergency_actions(self):
        payload = self.builder.build_payload(
            speed_meters_per_second=2.0,
            steering_radians=-0.1,
            emergency_state=False,
        )

        self.assertNotIn("BRAKE=MAX", payload)
        self.assertNotIn("EBS_ACTUATE", payload)


if __name__ == "__main__":
    unittest.main()