import rclpy
from rclpy.node import Node
from std_msgs.msg import Header

class LidarDriverNode(Node):
    def __init__(self):
        super().__init__('lidar_driver')
        self.pub = self.create_publisher(Header, '/sensor/lidar/pointcloud', 10)
        self.timer = self.create_timer(0.05, self.publish_cloud) # 20 Hz
        self.get_logger().info('LiDAR Driver Node initialized (20 Hz)')

    def publish_cloud(self):
        msg = Header()
        msg.stamp = self.get_clock().now().to_msg()
        msg.frame_id = 'lidar_frame'
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = LidarDriverNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
