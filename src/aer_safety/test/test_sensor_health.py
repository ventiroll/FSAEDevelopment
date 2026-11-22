import unittest
from aer_safety.sensor_health import SensorHealthChecker

class TestSensorHealthChecker(unittest.TestCase):

    def setUp(self):
        # defines the sensors required by the vehicle.
        self.sensors = [
            "camera",
            "lidar",
            "gps",
            "imu",
            "encoder",
        ]

        # creates a health checker for the tests.
        self.checker = SensorHealthChecker(
            required_sensors=self.sensors,
            stale_timeout_seconds=0.200,
            startup_timeout_seconds=1.0,
        )

    def test_all_sensors_are_ready(self):
        # records a message from every sensor.
        for sensor in self.sensors:
            self.checker.record_sensor_message(
                sensor_name=sensor,
                curr_time=0.5,
            )

        # evaluates the system shortly after receiving the messages.
        result = self.checker.evaluate(curr_time=0.6)

        self.assertTrue(result.system_ready)
        self.assertFalse(result.emergency_required)

    def test_missing_sensor_causes_emergency(self):
        # records messages from every sensor except the encoder.
        for sensor in self.sensors[:-1]:
            self.checker.record_sensor_message(
                sensor_name=sensor,
                curr_time=0.5,
            )

        # evaluates after the one-second startup timeout.
        result = self.checker.evaluate(curr_time=1.1)

        self.assertFalse(result.system_ready)
        self.assertTrue(result.emergency_required)
        self.assertIn("encoder", result.missing_sensors)

    def test_stale_sensor_causes_emergency(self):
        # records messages from every sensor.
        for sensor in self.sensors:
            self.checker.record_sensor_message(
                sensor_name=sensor,
                curr_time=0.5,
            )

        # evaluates after the 200 ms stale-data limit.
        result = self.checker.evaluate(curr_time=0.8)

        self.assertFalse(result.system_ready)
        self.assertTrue(result.emergency_required)
        self.assertEqual(
            set(result.stale_sensors),
            set(self.sensors),
        )

    def test_unknown_sensor_is_rejected(self):
        # verifies that an invalid sensor name raises an error.
        with self.assertRaises(ValueError):
            self.checker.record_sensor_message(
                sensor_name="unknown_sensor",
                curr_time=0.5,
            )


if __name__ == "__main__":
    unittest.main()