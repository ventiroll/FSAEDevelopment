import rclpy
from rclpy.node import Node
from std_msgs.msg import Header

class GpsDriverNode(Node):
    def __init__(self):
        super().__init__('gps_driver')
        self.pub = self.create_publisher(Header, '/sensor/gps/fix', 10)
        self.timer = self.create_timer(0.1, self.publish_gps) # 10 Hz
        self.get_logger().info('GPS Driver Node initialized (10 Hz)')

    def publish_gps(self):
        msg = Header()
        msg.stamp = self.get_clock().now().to_msg()
        msg.frame_id = 'gps_frame'
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = GpsDriverNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
