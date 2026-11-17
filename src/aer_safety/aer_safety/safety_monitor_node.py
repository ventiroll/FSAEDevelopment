import rclpy
from rclpy.node import Node
from std_msgs.msg import Header, Bool

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
        self.timeout_sec = float(self.get_parameter('stale_data_timeout_sec').value)

        self.driver_topics = [
            '/sensor/camera/raw',
            '/sensor/lidar/pointcloud',
            '/sensor/gps/fix',
            '/sensor/imu/data',
            '/sensor/encoder/ticks'
        ]

        now = self.get_clock().now()
        self.last_timestamps = {topic: now for topic in self.driver_topics}

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

    def check_liveliness(self):
        now = self.get_clock().now()
        emergency = False
        stale_topic = ""
        max_dt_ms = 0.0

        for topic, last_time in self.last_timestamps.items():
            dt_sec = (now - last_time).nanoseconds / 1e9
            dt_ms = dt_sec * 1000.0

            if dt_sec > self.timeout_sec:
                emergency = True
                stale_topic = topic
                max_dt_ms = dt_ms
                break

        msg = Bool()
        msg.data = emergency
        self.emergency_pub.publish(msg)

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
