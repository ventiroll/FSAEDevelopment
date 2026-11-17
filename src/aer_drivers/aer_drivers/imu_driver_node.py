import rclpy
from rclpy.node import Node
from std_msgs.msg import Header

class ImuDriverNode(Node):
    def __init__(self):
        super().__init__('imu_driver')
        self.pub = self.create_publisher(Header, '/sensor/imu/data', 10)
        self.timer = self.create_timer(0.01, self.publish_imu) # 100 Hz
        self.get_logger().info('IMU Driver Node initialized (100 Hz)')

    def publish_imu(self):
        msg = Header()
        msg.stamp = self.get_clock().now().to_msg()
        msg.frame_id = 'imu_frame'
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = ImuDriverNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
