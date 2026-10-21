import rclpy
from rclpy.node import Node
from aer_interfaces.msg import ControlCmd, VehicleState

class MicroRosBridgeNode(Node):
    def __init__(self):
        super().__init__('micro_ros_bridge_node')
        self.cmd_sub = self.create_subscription(ControlCmd, '/control/command', self.cmd_cb, 10)
        self.state_pub = self.create_publisher(VehicleState, '/vehicle/state', 10)
        self.last_cmd = ControlCmd()
        self.feedback_timer = self.create_timer(0.05, self.publish_feedback)

    def cmd_cb(self, msg: ControlCmd):
        self.last_cmd = msg

    def publish_feedback(self):
        state = VehicleState()
        state.header.stamp = self.get_clock().now().to_msg()
        state.current_speed_mps = self.last_cmd.target_velocity_mps
        state.current_steering_angle_rad = self.last_cmd.steering_angle_rad
        state.brake_pressure_bar = self.last_cmd.target_brake_pressure_bar
        self.state_pub.publish(state)

def main(args=None):
    rclpy.init(args=args)
    node = MicroRosBridgeNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
