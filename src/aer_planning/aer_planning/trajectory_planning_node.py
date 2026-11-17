import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class TrajectoryPlanningNode(Node):
    def __init__(self):
        super().__init__('trajectory_planning')
        self.sub = self.create_subscription(String, '/detected_lane', self.lane_cb, 10)
        self.pub = self.create_publisher(String, '/lanekeeping_trajectory', 10)
        self.get_logger().info('Trajectory Planning Node initialized')

    def lane_cb(self, msg: String):
        out = String()
        out.data = 'lanekeeping_path_waypoints'
        self.pub.publish(out)

def main(args=None):
    rclpy.init(args=args)
    node = TrajectoryPlanningNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
