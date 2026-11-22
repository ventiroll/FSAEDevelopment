import unittest

from aer_perception.detection_logic import (
    Detection,
    ObjectDetectionLogic,
    ObstacleDetectionLogic,
)

class TestObjectDetectionLogic(unittest.TestCase):
    """tests simulated object detection behavior."""

    def setUp(self):
        self.detector = ObjectDetectionLogic(
            minimum_confidence=0.50,
        )

    def test_valid_object_is_detected(self):
        result = self.detector.process(
            [
                Detection(
                    label="cone",
                    confidence=0.90,
                    distance_meters=8.0,
                    position="center",
                )
            ]
        )

        self.assertTrue(result.detected)
        self.assertEqual(len(result.detections), 1)
        self.assertTrue(result.safe_to_continue)

    def test_low_confidence_object_is_rejected(self):
        result = self.detector.process(
            [
                Detection(
                    label="cone",
                    confidence=0.30,
                    distance_meters=8.0,
                    position="center",
                )
            ]
        )

        self.assertFalse(result.detected)
        self.assertEqual(len(result.detections), 0)

    def test_no_objects_are_detected(self):
        result = self.detector.process([])

        self.assertFalse(result.detected)
        self.assertEqual(len(result.detections), 0)

class TestObstacleDetectionLogic(unittest.TestCase):
    """tests simulated obstacle safety behavior."""

    def setUp(self):
        self.detector = ObstacleDetectionLogic(
            stopping_distance_meters=2.0,
        )

    def test_close_obstacle_requires_safety_response(self):
        result = self.detector.process(
            [
                Detection(
                    label="obstacle",
                    confidence=0.95,
                    distance_meters=1.5,
                    position="center",
                )
            ]
        )

        self.assertTrue(result.detected)
        self.assertFalse(result.safe_to_continue)

    def test_far_obstacle_is_safe_to_continue(self):
        result = self.detector.process(
            [
                Detection(
                    label="obstacle",
                    confidence=0.95,
                    distance_meters=5.0,
                    position="right",
                )
            ]
        )

        self.assertTrue(result.detected)
        self.assertTrue(result.safe_to_continue)

    def test_negative_distance_is_rejected(self):
        result = self.detector.process(
            [
                Detection(
                    label="obstacle",
                    confidence=0.95,
                    distance_meters=-1.0,
                    position="center",
                )
            ]
        )

        self.assertFalse(result.detected)

if __name__ == "__main__":
    unittest.main()