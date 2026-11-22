"""
provides validation and actuator-monitoring logic for steering and speed.
"""

from dataclasses import dataclass
from typing import Optional
import math


@dataclass
class ControlCommand:
    """stores the requested steering and speed values."""

    steering_radians: float
    speed_meters_per_second: float


@dataclass
class ControlResult:
    """stores the result of validating a control command."""

    valid: bool
    steering_signal: Optional[float]
    throttle_signal: Optional[float]
    error: Optional[str]


@dataclass
class ActuatorFeedback:
    """stores the actual steering and speed values from the vehicle."""

    steering_radians: float
    speed_meters_per_second: float


class ControlValidator:
    """validates control commands and monitors actuator feedback."""

    def __init__(
        self,
        maximum_steering_radians: float = 0.5,
        maximum_speed_meters_per_second: float = 5.0,
        steering_tolerance_radians: float = 0.05,
        speed_tolerance_meters_per_second: float = 0.25,
        failure_timeout_seconds: float = 0.2,
    ):
        self.maximum_steering_radians = maximum_steering_radians
        self.maximum_speed_meters_per_second = (
            maximum_speed_meters_per_second
        )
        self.steering_tolerance_radians = steering_tolerance_radians
        self.speed_tolerance_meters_per_second = (
            speed_tolerance_meters_per_second
        )
        self.failure_timeout_seconds = failure_timeout_seconds

    def validate_command(
        self,
        command: ControlCommand,
    ) -> ControlResult:
        """checks whether a steering and speed command is safe."""

        if not math.isfinite(command.steering_radians):
            return ControlResult(
                valid=False,
                steering_signal=None,
                throttle_signal=None,
                error="steering command is not finite",
            )

        if not math.isfinite(command.speed_meters_per_second):
            return ControlResult(
                valid=False,
                steering_signal=None,
                throttle_signal=None,
                error="speed command is not finite",
            )

        if abs(command.steering_radians) > self.maximum_steering_radians:
            return ControlResult(
                valid=False,
                steering_signal=None,
                throttle_signal=None,
                error="steering command exceeds the safe limit",
            )

        if not (
            0.0
            <= command.speed_meters_per_second
            <= self.maximum_speed_meters_per_second
        ):
            return ControlResult(
                valid=False,
                steering_signal=None,
                throttle_signal=None,
                error="speed command exceeds the safe limit",
            )

        # converts speed into a normalized throttle signal.
        throttle_signal = (
            command.speed_meters_per_second
            / self.maximum_speed_meters_per_second
        )

        return ControlResult(
            valid=True,
            steering_signal=command.steering_radians,
            throttle_signal=throttle_signal,
            error=None,
        )

    def detect_control_failure(
        self,
        command: ControlCommand,
        feedback: ActuatorFeedback,
        elapsed_seconds: float,
    ) -> bool:
        """detects whether the vehicle failed to follow a command."""

        if elapsed_seconds < self.failure_timeout_seconds:
            return False

        steering_error = abs(
            feedback.steering_radians
            - command.steering_radians
        )

        speed_error = abs(
            feedback.speed_meters_per_second
            - command.speed_meters_per_second
        )

        return (
            steering_error > self.steering_tolerance_radians
            or speed_error > self.speed_tolerance_meters_per_second
        )