"""
builds normal and emergency uart commands.
"""


class UartCommandBuilder:
    """creates uart payloads for normal and emergency operation."""

    def build_payload(
        self,
        speed_meters_per_second: float,
        steering_radians: float,
        emergency_state: bool,
    ) -> str:
        """creates the correct payload for the current system state."""

        if emergency_state:
            return (
                "[UART TX -> STM32] EMERGENCY_STATE=1 | "
                "SPEED=0.0m/s | BRAKE=MAX | EBS_ACTUATE"
            )

        return (
            "[UART TX -> STM32] "
            f"SPEED={speed_meters_per_second:.2f}m/s | "
            f"STEER={steering_radians:.3f}rad"
        )