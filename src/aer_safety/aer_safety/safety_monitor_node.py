import rclpy
from rclpy.node import Node
from std_msgs.msg import Header, Bool
from aer_safety.sensor_health import SensorHealthChecker
from typing import cast

class SafetyMonitorNode(Node):
    """
    Safety Monitor Node:
    Watches all sensor driver topics (/sensor/camera/raw, /sensor/lidar/pointcloud,
    /sensor/gps/fix, /sensor/imu/data, /sensor/encoder/ticks) for liveliness.
    If any topic stops updating for > 200 ms (0.200 sec), it triggers /emergency_state.
    """
    def __init__(self):
        super().__init__('safety_monitor')
        
        self.declare_parameter('stale_data_timeout_sec', 0.200)
        stale_timeout_value = cast(float, self.get_parameter("stale_data_timeout_sec").value,)
        self.timeout_sec = float(stale_timeout_value)
        
        self.driver_topics = [
            '/sensor/camera/raw',
            '/sensor/lidar/pointcloud',
            '/sensor/gps/fix',
            '/sensor/imu/data',
            '/sensor/encoder/ticks'
        ]
        
        # creates the sensor health checker without removing the existing logic.
        self.health_checker = SensorHealthChecker(
            required_sensors=self.driver_topics,
            stale_timeout_seconds=self.timeout_sec,
            startup_timeout_seconds=5.0,
        )

        # publishes whether all required sensors are ready.
        self.system_ready_pub = self.create_publisher(
            Bool,
            "/system_ready",
            10,
        )

        now = self.get_clock().now()
        self.last_timestamps = {topic: now for topic in self.driver_topics}
        
        # tracks sensors that have published at least one message.
        self.received_topics = set()

        # Subscribe to all sensor driver topics
        self.subs = []
        for topic in self.driver_topics:
            sub = self.create_subscription(
                Header,
                topic,
                lambda msg, t=topic: self.sensor_callback(t),
                10
            )
            self.subs.append(sub)

        self.emergency_pub = self.create_publisher(Bool, '/emergency_state', 10)

        # 50 Hz Liveliness Check Loop (20 ms interval)
        self.timer = self.create_timer(0.020, self.check_liveliness)
        self.get_logger().info(f'Safety Monitor initialized. Watching {len(self.driver_topics)} driver topics with {self.timeout_sec*1000:.0f} ms timeout threshold.')

    def sensor_callback(self, topic_name):
        self.last_timestamps[topic_name] = self.get_clock().now()
        self.received_topics.add(topic_name)
        
        # records the sensor message for the new health-check system.
        current_time = self.get_clock().now().nanoseconds / 1e9

        self.health_checker.record_sensor_message(
            sensor_name=topic_name,
            curr_time=current_time,
        )

    def check_liveliness(self):
        now = self.get_clock().now()
        emergency = False
        stale_topic = ""
        max_dt_ms = 0.0

        for topic, last_time in self.last_timestamps.items():
            if topic not in self.received_topics:
                continue
            
            dt_sec = (now - last_time).nanoseconds / 1e9
            dt_ms = dt_sec * 1000.0

            if dt_sec > self.timeout_sec:
                emergency = True
                stale_topic = topic
                max_dt_ms = dt_ms
                break
            
        # evaluates startup readiness and missing-sensor failures.
        current_time = self.get_clock().now().nanoseconds / 1e9

        health_status = self.health_checker.evaluate(
            curr_time=current_time,
        )

        # adds startup sensor failures to the existing emergency logic.
        emergency = emergency or health_status.emergency_required

        msg = Bool()
        msg.data = emergency
        self.emergency_pub.publish(msg)
        
        # publishes whether the system is ready for autonomous operation.
        ready_msg = Bool()
        ready_msg.data = health_status.system_ready

        self.system_ready_pub.publish(ready_msg)

        if emergency:
            self.get_logger().error(
                f'EMERGENCY STATE TRIGGERED! Topic [{stale_topic}] stale by {max_dt_ms:.1f} ms (> {self.timeout_sec*1000:.0f} ms threshold).'
            )

def main(args=None):
    rclpy.init(args=args)
    node = SafetyMonitorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
