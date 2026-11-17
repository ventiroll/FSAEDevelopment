import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class GlobalPathPlanningNode(Node):
    def __init__(self):
        super().__init__('global_path_planning')
        self.sub = self.create_subscription(String, '/global_pos', self.pos_cb, 10)
        self.pub = self.create_publisher(String, '/planned_path', 10)
        self.get_logger().info('Global Path Planning Node initialized')

    def pos_cb(self, msg: String):
        out = String()
        out.data = 'global_racetrack_waypoints'
        self.pub.publish(out)

def main(args=None):
    rclpy.init(args=args)
    node = GlobalPathPlanningNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
