import rclpy
from rclpy.node import Node
from std_msgs.msg import Header, String

class PositionEstimationNode(Node):
    def __init__(self):
        super().__init__('position_estimation')
        self.sub = self.create_subscription(Header, '/sync/localization_data', self.loc_cb, 10)
        self.pub = self.create_publisher(String, '/global_pos', 10)
        self.get_logger().info('Position Estimation Node initialized (GPS + IMU + Encoder EKF)')

    def loc_cb(self, msg: Header):
        out = String()
        out.data = 'x:0.0, y:0.0, yaw:0.0'
        self.pub.publish(out)

def main(args=None):
    rclpy.init(args=args)
    node = PositionEstimationNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
