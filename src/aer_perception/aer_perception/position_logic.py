"""
provides testable position and orientation estimation logic.
"""

from dataclasses import dataclass
from typing import Optional
import math


@dataclass
class PositionEstimate:
    """stores the estimated vehicle position and orientation."""

    x_meters: float
    y_meters: float
    yaw_radians: float


@dataclass
class PositionResult:
    """stores the result of a position-estimation cycle."""

    valid: bool
    estimate: Optional[PositionEstimate]
    error: Optional[str]


class PositionEstimator:
    """validates gps and imu data and calculates vehicle position."""

    def __init__(
        self,
        origin_latitude: float = 0.0,
        origin_longitude: float = 0.0,
    ):
        self.origin_latitude = origin_latitude
        self.origin_longitude = origin_longitude

    def estimate(
        self,
        latitude: float,
        longitude: float,
        yaw_radians: float,
        gps_valid: bool = True,
        imu_valid: bool = True,
    ) -> PositionResult:
        """creates a local position estimate from gps and imu data."""

        if not gps_valid:
            return PositionResult(
                valid=False,
                estimate=None,
                error="gps data is invalid",
            )

        if not imu_valid:
            return PositionResult(
                valid=False,
                estimate=None,
                error="imu data is invalid",
            )

        if not all(
            math.isfinite(value)
            for value in (latitude, longitude, yaw_radians)
        ):
            return PositionResult(
                valid=False,
                estimate=None,
                error="position data contains a non-finite value",
            )

        if not -90.0 <= latitude <= 90.0:
            return PositionResult(
                valid=False,
                estimate=None,
                error="latitude is outside the valid range",
            )

        if not -180.0 <= longitude <= 180.0:
            return PositionResult(
                valid=False,
                estimate=None,
                error="longitude is outside the valid range",
            )

        # converts latitude and longitude into local x and y distances.
        meters_per_degree_latitude = 110540.0
        meters_per_degree_longitude = (
            111320.0
            * math.cos(math.radians(self.origin_latitude))
        )

        x_meters = (
            longitude - self.origin_longitude
        ) * meters_per_degree_longitude

        y_meters = (
            latitude - self.origin_latitude
        ) * meters_per_degree_latitude

        # keeps yaw within the range -pi to pi.
        normalized_yaw = math.atan2(
            math.sin(yaw_radians),
            math.cos(yaw_radians),
        )

        return PositionResult(
            valid=True,
            estimate=PositionEstimate(
                x_meters=x_meters,
                y_meters=y_meters,
                yaw_radians=normalized_yaw,
            ),
            error=None,
        )