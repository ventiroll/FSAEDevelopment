"""
defines the logic used to determine whether the vehicle sensors are healthy.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class SensorHealthStatus:
    system_ready: bool # true when every required sensor is publishing recent data
    emergency_required: bool # true when the vehicle should enter an emergency state
    missing_sensors: List[str]  # sensors that have not published any data yet
    stale_sensors: List[str] # sensors that have published data, but the data is too old


# checks whether every required sensor has recently published valid data
class SensorHealthChecker:
    def __init__(
        self,
        required_sensors: List[str],
        stale_timeout_seconds: float = 0.200,
        startup_timeout_seconds: float = 1.0,
    ):
        self.required_sensors = required_sensors # names of the sensors that must be available
        self.stale_timeout_seconds = stale_timeout_seconds # maximum time allowed between sensor messages
        self.startup_timeout_seconds = startup_timeout_seconds # maximum time allowed for sensors to begin publishing

        # stores the most recent message time for every sensor
        # none means that the sensor has not published yet
        self.last_received_time: Dict[str, Optional[float]] = {
            sensor: None
            for sensor in required_sensors
        }
        
        self.start_time: Optional[float] = None # stores when the startup health check began

    # starts the sensor health-check timer
    def start(self, curr_time: float) -> None:
        self.start_time = curr_time # saves the time when the health check started

    # records that a sensor has successfully published a message
    def record_sensor_message(
        self,
        sensor_name: str,
        curr_time: float,
    ) -> None:
        # prevents unknown sensor names from being accepted
        if sensor_name not in self.last_received_time:
            raise ValueError(f"Unknown sensor: {sensor_name}")

        self.last_received_time[sensor_name] = curr_time # stores the time of the newest message from the sensor

    # evaluates the current health status of all sensors
    def evaluate(
        self,
        curr_time: float,
    ) -> SensorHealthStatus:

        # starts the timer automatically if evaluate() is called first
        if self.start_time is None:
            self.start(curr_time)

        start_time = self.start_time # stores the start time locally after checking that it is not none

        # protects the calculation if the start time is unavailable
        if start_time is None:
            raise RuntimeError("Sensor health checker was not started.")

        missing_sensors: List[str] = [] # stores sensors that have not published any messages
        stale_sensors: List[str] = [] # stores sensors whose latest message is too old

        # checks every required sensor
        for sensor_name, last_time in self.last_received_time.items():

            # marks the sensor as missing if it has never published
            if last_time is None:
                missing_sensors.append(sensor_name)
                continue

            time_since_message = curr_time - last_time # calculates how long ago the most recent message was received

            # marks the sensor as stale if the message is too old
            if time_since_message > self.stale_timeout_seconds:
                stale_sensors.append(sensor_name)

        # determines whether the startup timeout has expired
        startup_timeout_expired = (
            curr_time - start_time
            >= self.startup_timeout_seconds
        )

        # the system is ready when every sensor is present and current
        system_ready = (
            len(missing_sensors) == 0
            and len(stale_sensors) == 0
        )

        # requires an emergency when a sensor is stale or fails during startup
        emergency_required = (
            len(stale_sensors) > 0
            or (
                startup_timeout_expired
                and len(missing_sensors) > 0
            )
        )

        # returns the complete sensor health result
        return SensorHealthStatus(
            system_ready=system_ready,
            emergency_required=emergency_required,
            missing_sensors=missing_sensors,
            stale_sensors=stale_sensors,
        )