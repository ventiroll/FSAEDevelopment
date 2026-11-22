import unittest

from aer_safety.topic_rate_monitor import TopicRateMonitor


class TestTopicRateMonitor(unittest.TestCase):
    """tests topic frequency and stale-message detection."""

    def setUp(self):
        self.monitor = TopicRateMonitor(
            expected_rates_hz={
                "/sensor/imu/data": 10.0,
                "/sensor/gps/fix": 5.0,
            },
            minimum_rate_ratio=0.80,
            stale_timeout_seconds=0.50,
        )

    def test_healthy_topic_rate_is_detected(self):
        for timestamp in [0.0, 0.1, 0.2, 0.3, 0.4]:
            self.monitor.record_message(
                "/sensor/imu/data",
                timestamp,
            )

        status = self.monitor.evaluate_topic(
            "/sensor/imu/data",
            0.5,
        )

        self.assertTrue(status.healthy)
        self.assertAlmostEqual(
            status.observed_rate_hz,
            10.0,
        )

    def test_slow_topic_rate_is_detected(self):
        for timestamp in [0.0, 0.3, 0.6, 0.9]:
            self.monitor.record_message(
                "/sensor/imu/data",
                timestamp,
            )

        status = self.monitor.evaluate_topic(
            "/sensor/imu/data",
            1.0,
        )

        self.assertFalse(status.healthy)
        self.assertAlmostEqual(
            status.observed_rate_hz,
            3.33,
            places=1,
        )

    def test_stale_topic_is_detected(self):
        self.monitor.record_message(
            "/sensor/gps/fix",
            0.0,
        )
        self.monitor.record_message(
            "/sensor/gps/fix",
            0.2,
        )

        status = self.monitor.evaluate_topic(
            "/sensor/gps/fix",
            1.0,
        )

        self.assertFalse(status.healthy)
        self.assertGreater(
            status.message_age_seconds,
            0.50,
        )

    def test_topic_recovers_after_new_messages(self):
        self.monitor.record_message(
            "/sensor/gps/fix",
            0.0,
        )
        self.monitor.record_message(
            "/sensor/gps/fix",
            0.2,
        )

        failed_status = self.monitor.evaluate_topic(
            "/sensor/gps/fix",
            1.0,
        )

        self.assertFalse(failed_status.healthy)

        self.monitor.record_message(
            "/sensor/gps/fix",
            1.1,
        )
        self.monitor.record_message(
            "/sensor/gps/fix",
            1.3,
        )

        recovered_status = self.monitor.evaluate_topic(
            "/sensor/gps/fix",
            1.4,
        )

        self.assertTrue(recovered_status.healthy)

    def test_unknown_topic_is_rejected(self):
        with self.assertRaises(ValueError):
            self.monitor.record_message(
                "/unknown/topic",
                0.0,
            )

    def test_backward_timestamp_is_rejected(self):
        self.monitor.record_message(
            "/sensor/imu/data",
            1.0,
        )

        with self.assertRaises(ValueError):
            self.monitor.record_message(
                "/sensor/imu/data",
                0.5,
            )


if __name__ == "__main__":
    unittest.main()