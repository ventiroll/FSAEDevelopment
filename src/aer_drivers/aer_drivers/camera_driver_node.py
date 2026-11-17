import rclpy
from rclpy.node import Node
from std_msgs.msg import Header

class CameraDriverNode(Node):
    def __init__(self):
        super().__init__('camera_driver')
        self.pub = self.create_publisher(Header, '/sensor/camera/raw', 10)
        self.timer = self.create_timer(0.033, self.publish_frame) # 30 Hz
        self.get_logger().info('Camera Driver Node initialized (30 Hz)')

    def publish_frame(self):
        msg = Header()
        msg.stamp = self.get_clock().now().to_msg()
        msg.frame_id = 'camera_optical_frame'
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = CameraDriverNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
