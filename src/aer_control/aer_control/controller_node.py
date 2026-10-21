import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path
from aer_interfaces.msg import ControlCmd, VehicleState
import math

class ControllerNode(Node):
    def __init__(self):
        super().__init__('controller_node')
        self.declare_parameter('target_speed_mps', 5.0)
        self.declare_parameter('k_stanley', 0.5)

        self.path_sub = self.create_subscription(Path, '/planning/target_path', self.path_callback, 10)
        self.state_sub = self.create_subscription(VehicleState, '/vehicle/state', self.state_callback, 10)
        self.cmd_pub = self.create_publisher(ControlCmd, '/control/command', 10)

        self.current_state = VehicleState()

    def state_callback(self, msg: VehicleState):
        self.current_state = msg

    def path_callback(self, msg: Path):
        if len(msg.poses) < 2:
            return

        target_v = self.get_parameter('target_speed_mps').value
        k_s = self.get_parameter('k_stanley').value

        p1 = msg.poses[0].pose.position
        p2 = msg.poses[1].pose.position

        dx = p2.x - p1.x
        dy = p2.y - p1.y
        path_heading = math.atan2(dy, dx)

        cross_track_error = p1.y
        v = max(self.current_state.current_speed_mps, 1.0)

        steering_angle = path_heading + math.atan2(k_s * cross_track_error, v)
        steering_angle = max(min(steering_angle, 0.436), -0.436)

        cmd = ControlCmd()
        cmd.header.stamp = self.get_clock().now().to_msg()
        cmd.steering_angle_rad = steering_angle
        cmd.target_velocity_mps = target_v
        cmd.target_brake_pressure_bar = 0.0
        cmd.emergency_stop = False

        self.cmd_pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = ControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
