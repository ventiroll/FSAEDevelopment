import rclpy
from rclpy.node import Node

try:
    from aer_interfaces.msg import ControlCmd
except ImportError:
    from std_msgs.msg import Header
    class ControlCmd:
        def __init__(self):
            self.header = Header()
            self.steering_angle_rad = 0.0
            self.target_velocity_mps = 0.0
            self.target_brake_pressure_bar = 0.0
            self.emergency_stop = False

class DemoInverterNode(Node):
    def __init__(self):
        super().__init__('demo_inverter_node')

        self.declare_parameter('throttle_mode', 'medium')
        self.declare_parameter('publish_rate_hz', 10.0)
        self.declare_parameter('target_speed_mps', -1.0)

        self.PRESETS = {
            'slow':   {'speed_mps': 1.0, 'voltage': '1.0V (20% Torque)'},
            'medium': {'speed_mps': 2.5, 'voltage': '2.5V (50% Torque)'},
            'hard':   {'speed_mps': 5.0, 'voltage': '4.5V (90% Torque)'},
        }

        mode = str(self.get_parameter('throttle_mode').value).lower()
        custom_speed = float(self.get_parameter('target_speed_mps').value)

        if custom_speed >= 0.0:
            self.target_speed = custom_speed
            self.voltage_desc = f"~{(custom_speed/5.0)*4.5:.2f}V Custom DAC"
            self.mode_name = f"custom ({custom_speed:.1f} m/s)"
        elif mode in self.PRESETS:
            self.target_speed = self.PRESETS[mode]['speed_mps']
            self.voltage_desc = self.PRESETS[mode]['voltage']
            self.mode_name = mode
        else:
            self.get_logger().warn(f"Unknown throttle_mode '{mode}'. Defaulting to 'medium'.")
            self.target_speed = self.PRESETS['medium']['speed_mps']
            self.voltage_desc = self.PRESETS['medium']['voltage']
            self.mode_name = 'medium'

        rate_hz = float(self.get_parameter('publish_rate_hz').value)
        timer_period = 1.0 / max(rate_hz, 1.0)

        self.cmd_pub = self.create_publisher(ControlCmd, '/control/command', 10)
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.get_logger().info('==================================================')
        self.get_logger().info('  SDSU AER - Micro-ROS Inverter Demo Node Started')
        self.get_logger().info(f'   Selected Mode : [{self.mode_name.upper()}]')
        self.get_logger().info(f'   Target Speed  : {self.target_speed:.2f} m/s')
        self.get_logger().info(f'   STM32 DAC Output: {self.voltage_desc} -> CM200 Inverter')
        self.get_logger().info(f'   Publishing    : {rate_hz:.1f} Hz -> Topic [/control/command]')
        self.get_logger().info('==================================================')

        self.last_log_time = 0.0

    def timer_callback(self):
        msg = ControlCmd()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.steering_angle_rad = 0.0
        msg.target_velocity_mps = self.target_speed
        msg.target_brake_pressure_bar = 0.0
        msg.emergency_stop = False

        self.cmd_pub.publish(msg)

        now_sec = self.get_clock().now().nanoseconds / 1e9
        if now_sec - self.last_log_time >= 1.0:
            self.get_logger().info(
                f'[DEMO STREAM] Jetson -> micro-ROS | Speed: {self.target_speed:.1f} m/s | Signal: {self.voltage_desc}'
            )
            self.last_log_time = now_sec

def main(args=None):
    rclpy.init(args=args)
    node = DemoInverterNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Stopping Demo Node. Sending 0.0 m/s neutral signal...')
        stop_msg = ControlCmd()
        stop_msg.target_velocity_mps = 0.0
        node.cmd_pub.publish(stop_msg)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
