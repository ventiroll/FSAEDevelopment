"""
provides testable logic for object and obstacle detection results.
"""

from dataclasses import dataclass
from typing import List

@dataclass
class Detection:
    """stores one detected object or obstacle."""

    label: str
    confidence: float
    distance_meters: float
    position: str

@dataclass
class DetectionResult:
    """stores the result of one detection cycle."""

    detected: bool
    detections: List[Detection]
    safe_to_continue: bool

class ObjectDetectionLogic:
    """validates simulated camera detection results."""

    def __init__(self, minimum_confidence: float = 0.50):
        self.minimum_confidence = minimum_confidence

    def process(
        self,
        detections: List[Detection],
    ) -> DetectionResult:
        """keeps only valid object detections."""

        valid_detections = [
            detection
            for detection in detections
            if detection.confidence >= self.minimum_confidence
            and detection.distance_meters >= 0.0
        ]

        return DetectionResult(
            detected=len(valid_detections) > 0,
            detections=valid_detections,
            safe_to_continue=True,
        )

class ObstacleDetectionLogic:
    """determines whether an obstacle requires a safety response."""

    def __init__(self, stopping_distance_meters: float = 2.0):
        self.stopping_distance_meters = stopping_distance_meters

    def process(
        self,
        obstacles: List[Detection],
    ) -> DetectionResult:
        """marks the vehicle unsafe when an obstacle is too close."""

        valid_obstacles = [
            obstacle
            for obstacle in obstacles
            if obstacle.distance_meters >= 0.0
        ]

        unsafe_obstacles = [
            obstacle
            for obstacle in valid_obstacles
            if obstacle.distance_meters <= self.stopping_distance_meters
        ]

        return DetectionResult(
            detected=len(valid_obstacles) > 0,
            detections=valid_obstacles,
            safe_to_continue=len(unsafe_obstacles) == 0,
        )