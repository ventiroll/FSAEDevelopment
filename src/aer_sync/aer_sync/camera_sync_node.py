import rclpy
from rclpy.node import Node
from std_msgs.msg import Header

class CameraSyncNode(Node):
    def __init__(self):
        super().__init__('camera_sync')
        self.sub = self.create_subscription(Header, '/sensor/camera/raw', self.sync_cb, 10)
        self.pub = self.create_publisher(Header, '/sync/camera_pair', 10)
        self.get_logger().info('Camera Sync Node initialized (downsample frame pair)')

    def sync_cb(self, msg: Header):
        # Downsample / sync logic
        sync_msg = Header()
        sync_msg.stamp = msg.stamp
        sync_msg.frame_id = 'camera_synced'
        self.pub.publish(sync_msg)

def main(args=None):
    rclpy.init(args=args)
    node = CameraSyncNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
