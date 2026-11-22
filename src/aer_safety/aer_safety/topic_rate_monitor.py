"""
monitors topic publishing rates and detects stale topics.
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class TopicRateStatus:
    """stores the health status of one monitored topic."""

    healthy: bool
    observed_rate_hz: float
    message_age_seconds: float


class TopicRateMonitor:
    """checks whether topics publish at their required rates."""

    def __init__(
        self,
        expected_rates_hz: Dict[str, float],
        minimum_rate_ratio: float = 0.80,
        stale_timeout_seconds: float = 0.50,
    ):
        self.expected_rates_hz = expected_rates_hz
        self.minimum_rate_ratio = minimum_rate_ratio
        self.stale_timeout_seconds = stale_timeout_seconds

        self.message_counts: Dict[str, int] = {
            topic: 0
            for topic in expected_rates_hz
        }

        self.first_message_times: Dict[str, Optional[float]] = {
            topic: None
            for topic in expected_rates_hz
        }

        self.last_message_times: Dict[str, Optional[float]] = {
            topic: None
            for topic in expected_rates_hz
        }

    def record_message(
        self,
        topic_name: str,
        current_time_seconds: float,
    ) -> None:
        """records the time that a topic published a message."""

        if topic_name not in self.expected_rates_hz:
            raise ValueError(
                f"unknown topic: {topic_name}"
            )

        last_time = self.last_message_times[topic_name]

        if (
            last_time is not None
            and current_time_seconds < last_time
        ):
            raise ValueError(
                "message timestamp cannot move backward"
            )
        # starts a new rate window after a stale period.
        if (
            last_time is not None
            and current_time_seconds - last_time
            > self.stale_timeout_seconds
        ):
            self.first_message_times[topic_name] = (
                current_time_seconds
            )
            self.message_counts[topic_name] = 0
            

        if self.first_message_times[topic_name] is None:
            self.first_message_times[topic_name] = (
                current_time_seconds
            )

        self.last_message_times[topic_name] = (
            current_time_seconds
        )

        self.message_counts[topic_name] += 1

    def evaluate_topic(
        self,
        topic_name: str,
        current_time_seconds: float,
    ) -> TopicRateStatus:
        """evaluates the publishing rate and freshness of a topic."""

        if topic_name not in self.expected_rates_hz:
            raise ValueError(
                f"unknown topic: {topic_name}"
            )

        first_time = self.first_message_times[topic_name]
        last_time = self.last_message_times[topic_name]
        message_count = self.message_counts[topic_name]

        if first_time is None or last_time is None:
            return TopicRateStatus(
                healthy=False,
                observed_rate_hz=0.0,
                message_age_seconds=float("inf"),
            )

        message_age_seconds = (
            current_time_seconds - last_time
        )

        elapsed_seconds = last_time - first_time

        if message_count < 2 or elapsed_seconds <= 0.0:
            observed_rate_hz = 0.0
        else:
            observed_rate_hz = (
                (message_count - 1)
                / elapsed_seconds
            )

        minimum_rate_hz = (
            self.expected_rates_hz[topic_name]
            * self.minimum_rate_ratio
        )

        healthy = (
            message_count >= 2
            and observed_rate_hz >= minimum_rate_hz
            and message_age_seconds <= self.stale_timeout_seconds
        )

        return TopicRateStatus(
            healthy=healthy,
            observed_rate_hz=observed_rate_hz,
            message_age_seconds=message_age_seconds,
        )