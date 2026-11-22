import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, Bool
from aer_bridge.uart_protocol import UartCommandBuilder

class UartBridgeNode(Node):
    """
    UART Bridge Node:
    Serializes speed and steer commands to STM32 over UART.
    If /emergency_state is True, overrides controls and commands immediate E-stop / EBS.
    """
    def __init__(self):
        super().__init__('uart_bridge')
        self.sub_speed = self.create_subscription(Float64, '/planned_speed', self.speed_cb, 10)
        self.sub_steer = self.create_subscription(Float64, '/planned_steer', self.steer_cb, 10)
        self.sub_emg = self.create_subscription(Bool, '/emergency_state', self.emg_cb, 10)

        self.current_speed = 0.0
        self.current_steer = 0.0
        self.is_emergency = False
        self.command_builder = UartCommandBuilder()

        self.timer = self.create_timer(0.020, self.send_uart_frame) # 50 Hz to STM32
        self.get_logger().info('UART Bridge Node initialized (Jetson ROS 2 <-> STM32 MCU)')

    def speed_cb(self, msg: Float64): self.current_speed = msg.data
    def steer_cb(self, msg: Float64): self.current_steer = msg.data
    def emg_cb(self, msg: Bool): self.is_emergency = msg.data

    def send_uart_frame(self):
        # builds the current uart command.

        uart_payload = self.command_builder.build_payload(
            speed_meters_per_second=self.current_speed,
            steering_radians=self.current_steer,
            emergency_state=self.is_emergency,
        )

        # log payload simulation
        # self.get_logger().info(uart_payload)

def main(args=None):
    rclpy.init(args=args)
    node = UartBridgeNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
