import rclpy
from rclpy.node import Node
from std_msgs.msg import Header

class EncoderDriverNode(Node):
    def __init__(self):
        super().__init__('encoder_driver')
        self.pub = self.create_publisher(Header, '/sensor/encoder/ticks', 10)
        self.timer = self.create_timer(0.01, self.publish_ticks) # 100 Hz
        self.get_logger().info('Encoder Driver Node initialized (100 Hz)')

    def publish_ticks(self):
        msg = Header()
        msg.stamp = self.get_clock().now().to_msg()
        msg.frame_id = 'encoder_frame'
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = EncoderDriverNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
