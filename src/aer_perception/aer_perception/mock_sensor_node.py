import rclpy
from rclpy.node import Node
from aer_interfaces.msg import Cone, ConeArray
from std_msgs.msg import Header
import math

class MockSensorNode(Node):
    def __init__(self):
        super().__init__('mock_sensor_node')
        self.publisher_ = self.create_publisher(ConeArray, '/perception/cone_array', 10)
        self.timer = self.create_timer(0.1, self.publish_cones)

    def publish_cones(self):
        msg = ConeArray()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'

        for i in range(1, 10):
            x_pos = float(i * 2.5)
            y_offset = 0.1 * math.sin(x_pos * 0.2)

            c_blue = Cone()
            c_blue.x = x_pos
            c_blue.y = 1.5 + y_offset
            c_blue.z = 0.0
            c_blue.color = Cone.BLUE
            c_blue.confidence = 0.95
            msg.cones.append(c_blue)

            c_yellow = Cone()
            c_yellow.x = x_pos
            c_yellow.y = -1.5 + y_offset
            c_yellow.z = 0.0
            c_yellow.color = Cone.YELLOW
            c_yellow.confidence = 0.95
            msg.cones.append(c_yellow)

        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = MockSensorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
