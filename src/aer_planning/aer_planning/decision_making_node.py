import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float64

class DecisionMakingNode(Node):
    def __init__(self):
        super().__init__('decision_making')
        self.sub_traj = self.create_subscription(String, '/lanekeeping_trajectory', self.traj_cb, 10)
        self.sub_path = self.create_subscription(String, '/planned_path', self.path_cb, 10)
        self.sub_obj = self.create_subscription(String, '/detected_obj', self.obj_cb, 10)
        self.sub_obst = self.create_subscription(String, '/detected_obst', self.obst_cb, 10)

        self.pub_speed = self.create_publisher(Float64, '/planned_speed', 10)
        self.pub_steer = self.create_publisher(Float64, '/planned_steer', 10)
        self.get_logger().info('Decision Making Funnel Node initialized (FSM + Rule-based Tree)')

    def traj_cb(self, msg): self.process_funnel()
    def path_cb(self, msg): pass
    def obj_cb(self, msg): pass
    def obst_cb(self, msg): pass

    def process_funnel(self):
        s_msg = Float64()
        s_msg.data = 3.0 # target m/s
        st_msg = Float64()
        st_msg.data = 0.05 # steer rad
        self.pub_speed.publish(s_msg)
        self.pub_steer.publish(st_msg)

def main(args=None):
    rclpy.init(args=args)
    node = DecisionMakingNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
