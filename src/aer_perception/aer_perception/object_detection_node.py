import rclpy
from rclpy.node import Node
from std_msgs.msg import Header, String

class ObjectDetectionNode(Node):
    def __init__(self):
        super().__init__('object_detection')
        self.sub = self.create_subscription(Header, '/sync/camera_pair', self.cam_cb, 10)
        self.pub = self.create_publisher(String, '/detected_obj', 10)
        self.get_logger().info('Object Detection Node initialized (YOLO11)')

    def cam_cb(self, msg: Header):
        out = String()
        out.data = 'yolo11_bounding_boxes'
        self.pub.publish(out)

def main(args=None):
    rclpy.init(args=args)
    node = ObjectDetectionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
