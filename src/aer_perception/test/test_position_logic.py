import math
import unittest

from aer_perception.position_logic import PositionEstimator


class TestPositionEstimator(unittest.TestCase):
    """tests vehicle position and orientation estimation."""

    def setUp(self):
        self.estimator = PositionEstimator(
            origin_latitude=32.7157,
            origin_longitude=-117.1611,
        )

    def test_valid_gps_and_imu_data_produces_estimate(self):
        result = self.estimator.estimate(
            latitude=32.7160,
            longitude=-117.1608,
            yaw_radians=1.0,
        )

        self.assertTrue(result.valid)
        self.assertIsNotNone(result.estimate)
        self.assertIsNone(result.error)

    def test_invalid_gps_data_is_rejected(self):
        result = self.estimator.estimate(
            latitude=32.7160,
            longitude=-117.1608,
            yaw_radians=1.0,
            gps_valid=False,
        )

        self.assertFalse(result.valid)
        self.assertIsNone(result.estimate)
        self.assertEqual(result.error, "gps data is invalid")

    def test_invalid_imu_data_is_rejected(self):
        result = self.estimator.estimate(
            latitude=32.7160,
            longitude=-117.1608,
            yaw_radians=1.0,
            imu_valid=False,
        )

        self.assertFalse(result.valid)
        self.assertIsNone(result.estimate)
        self.assertEqual(result.error, "imu data is invalid")

    def test_invalid_latitude_is_rejected(self):
        result = self.estimator.estimate(
            latitude=95.0,
            longitude=-117.1608,
            yaw_radians=1.0,
        )

        self.assertFalse(result.valid)
        self.assertIsNone(result.estimate)

    def test_yaw_is_normalized(self):
        result = self.estimator.estimate(
            latitude=32.7160,
            longitude=-117.1608,
            yaw_radians=4.0,
        )

        self.assertTrue(result.valid)
        self.assertIsNotNone(result.estimate)
        self.assertTrue(
            -math.pi <= result.estimate.yaw_radians <= math.pi
        )


if __name__ == "__main__":
    unittest.main()