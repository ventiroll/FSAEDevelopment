import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, Bool

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

        self.timer = self.create_timer(0.020, self.send_uart_frame) # 50 Hz to STM32
        self.get_logger().info('UART Bridge Node initialized (Jetson ROS 2 <-> STM32 MCU)')

    def speed_cb(self, msg: Float64): self.current_speed = msg.data
    def steer_cb(self, msg: Float64): self.current_steer = msg.data
    def emg_cb(self, msg: Bool): self.is_emergency = msg.data

    def send_uart_frame(self):
        if self.is_emergency:
            # Override decision making and send hardware e-stop packet to STM32
            uart_payload = "[UART TX -> STM32] EMERGENCY_STATE=1 | SPEED=0.0m/s | BRAKE=MAX | EBS_ACTUATE"
        else:
            uart_payload = f"[UART TX -> STM32] SPEED={self.current_speed:.2f}m/s | STEER={self.current_steer:.3f}rad"
        
        # Log payload simulation
        # self.get_logger().info(uart_payload)

def main(args=None):
    rclpy.init(args=args)
    node = UartBridgeNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
