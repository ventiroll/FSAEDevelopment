import rclpy
from rclpy.node import Node
from aer_interfaces.msg import ConeArray, DssiStatus, ControlCmd

class SafetyMonitorNode(Node):
    def __init__(self):
        super().__init__('safety_monitor_node')
        self.last_sensor_time = self.get_clock().now()
        self.max_allowed_stale_sec = 0.200

        self.sensor_sub = self.create_subscription(ConeArray, '/perception/cone_array', self.sensor_cb, 10)
        self.dssi_pub = self.create_publisher(DssiStatus, '/vehicle/dssi_status', 10)
        self.cmd_pub = self.create_publisher(ControlCmd, '/control/command', 10)

        self.current_dssi = DssiStatus.DRIVING
        self.check_timer = self.create_timer(0.05, self.monitor_liveliness)

    def sensor_cb(self, msg: ConeArray):
        self.last_sensor_time = self.get_clock().now()

    def monitor_liveliness(self):
        now = self.get_clock().now()
        dt = (now - self.last_sensor_time).nanoseconds / 1e9

        dssi_msg = DssiStatus()

        if dt > self.max_allowed_stale_sec:
            self.get_logger().error(f'SAFETY TRIP: Sensor data stale by {dt*1000:.1f} ms (> 200 ms)! Triggering Emergency State.')
            self.current_dssi = DssiStatus.EMERGENCY

            e_cmd = ControlCmd()
            e_cmd.header.stamp = now.to_msg()
            e_cmd.emergency_stop = True
            e_cmd.target_velocity_mps = 0.0
            e_cmd.target_brake_pressure_bar = 30.0
            self.cmd_pub.publish(e_cmd)

        dssi_msg.status = self.current_dssi
        self.dssi_pub.publish(dssi_msg)

def main(args=None):
    rclpy.init(args=args)
    node = SafetyMonitorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
