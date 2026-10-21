import rclpy
from rclpy.node import Node
from aer_interfaces.msg import ConeArray, Cone
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped

class PathPlannerNode(Node):
    def __init__(self):
        super().__init__('path_planner_node')
        self.subscription = self.create_subscription(
            ConeArray,
            '/perception/cone_array',
            self.cone_callback,
            10
        )
        self.path_pub = self.create_publisher(Path, '/planning/target_path', 10)

    def cone_callback(self, msg: ConeArray):
        blue_cones = [c for c in msg.cones if c.color == Cone.BLUE]
        yellow_cones = [c for c in msg.cones if c.color == Cone.YELLOW]

        blue_cones.sort(key=lambda c: c.x)
        yellow_cones.sort(key=lambda c: c.x)

        path_msg = Path()
        path_msg.header = msg.header

        num_pairs = min(len(blue_cones), len(yellow_cones))
        for i in range(num_pairs):
            b = blue_cones[i]
            y = yellow_cones[i]

            mid_x = (b.x + y.x) / 2.0
            mid_y = (b.y + y.y) / 2.0

            pose = PoseStamped()
            pose.header = msg.header
            pose.pose.position.x = mid_x
            pose.pose.position.y = mid_y
            pose.pose.position.z = 0.0
            pose.pose.orientation.w = 1.0
            path_msg.poses.append(pose)

        self.path_pub.publish(path_msg)

def main(args=None):
    rclpy.init(args=args)
    node = PathPlannerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
