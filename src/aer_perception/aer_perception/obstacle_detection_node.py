import rclpy
from rclpy.node import Node
from std_msgs.msg import Header, String

class ObstacleDetectionNode(Node):
    def __init__(self):
        super().__init__('obstacle_detection')
        self.sub_lidar = self.create_subscription(Header, '/sensor/lidar/pointcloud', self.lidar_cb, 10)
        self.sub_enc = self.create_subscription(Header, '/sensor/encoder/ticks', self.enc_cb, 10)
        self.pub = self.create_publisher(String, '/detected_obst', 10)
        self.get_logger().info('Obstacle Detection Node initialized (LiDAR + DBSCAN)')

    def enc_cb(self, msg): pass
    def lidar_cb(self, msg: Header):
        out = String()
        out.data = 'dbscan_clusters'
        self.pub.publish(out)

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleDetectionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
