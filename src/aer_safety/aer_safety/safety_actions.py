"""
provides safety-state and vehicle-stop decision logic.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class SafetyAction:
    """stores the action required after a system error."""

    emergency_state: bool
    throttle_command: float
    vehicle_stopped: bool
    autonomous_enabled: bool
    errors: List[str]


class SafetyActionController:
    """determines whether the vehicle should continue or stop."""

    def __init__(self, stopped_speed_limit: float = 0.05):
        self.stopped_speed_limit = stopped_speed_limit

    def evaluate_system(
        self,
        sensors_ready: bool,
        command_valid: bool,
        communication_healthy: bool,
    ) -> SafetyAction:
        """creates a safety action from system health conditions."""

        errors = []

        if not sensors_ready:
            errors.append("sensor health failure")

        if not command_valid:
            errors.append("invalid control command")

        if not communication_healthy:
            errors.append("communication failure")

        if errors:
            return SafetyAction(
                emergency_state=True,
                throttle_command=0.0,
                vehicle_stopped=True,
                autonomous_enabled=False,
                errors=errors,
            )

        return SafetyAction(
            emergency_state=False,
            throttle_command=0.0,
            vehicle_stopped=False,
            autonomous_enabled=True,
            errors=[],
        )

    def verify_vehicle_stop(self, actual_speed: float) -> bool:
        """checks whether the vehicle speed is within the stopped limit."""

        return abs(actual_speed) <= self.stopped_speed_limit