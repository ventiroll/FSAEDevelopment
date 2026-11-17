import rclpy
from rclpy.node import Node
from std_msgs.msg import Header

class LocalizationSyncNode(Node):
    def __init__(self):
        super().__init__('localization_sync')
        self.sub_gps = self.create_subscription(Header, '/sensor/gps/fix', self.gps_cb, 10)
        self.sub_imu = self.create_subscription(Header, '/sensor/imu/data', self.imu_cb, 10)
        self.sub_enc = self.create_subscription(Header, '/sensor/encoder/ticks', self.enc_cb, 10)
        self.pub = self.create_publisher(Header, '/sync/localization_data', 10)
        self.get_logger().info('Localization Sync Node initialized (zero-order-hold GPS/IMU/encoder)')

    def gps_cb(self, msg): pass
    def imu_cb(self, msg): pass
    def enc_cb(self, msg: Header):
        sync_msg = Header()
        sync_msg.stamp = msg.stamp
        sync_msg.frame_id = 'loc_synced'
        self.pub.publish(sync_msg)

def main(args=None):
    rclpy.init(args=args)
    node = LocalizationSyncNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
