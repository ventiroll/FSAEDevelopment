#!/usr/bin/env python3
"""
mock_cone_publisher.py

A test harness for safety_monitor_node, matched to its real topics:
  - publishes aer_interfaces/ConeArray on /perception/cone_array
    (the input safety_monitor_node watches for staleness)
  - subscribes to /vehicle/dssi_status and /control/command
    (the outputs safety_monitor_node produces) and logs every change,
    so you can see the trip/recovery behaviour in one place.

CONE DATA CONTENT DOESN'T MATTER HERE
--------------------------------------
safety_monitor_node only cares about *when* a ConeArray message arrives
(it timestamps arrival with self.get_clock().now() in sensor_cb), not
what's inside it. So this publishes a bare, default-constructed
ConeArray() each tick - no need to fill in fake cone positions.

HEADS UP ON THE LATCHING BEHAVIOUR
------------------------------------
As written, safety_monitor_node currently has no path back to DRIVING
once it trips to EMERGENCY - there's no "else" branch resetting
self.current_dssi when fresh data resumes. So in the scenarios below,
expect DSSI to go to EMERGENCY and STAY there after a dropout, even
once this harness resumes publishing. That's a property of the node
as currently written, not a bug in this test script - confirm whether
that's the behaviour you actually want.

HOW TO USE
----------
1. Steady state (should stay in DRIVING, no SAFETY TRIP logs):
     ros2 run aer_safety mock_cone_publisher

2. Automated, scripted dropout test (no manual Ctrl+C needed):
     ros2 run aer_safety mock_cone_publisher --ros-args \
       -p auto_drop_after_sec:=5.0 -p resume_after_sec:=10.0
   Publishes normally for 5s, goes silent for 10s (you should see
   safety_monitor_node's SAFETY TRIP log appear ~0.2-0.25s into that
   gap), then resumes publishing - at which point, given the latching
   note above, watch whether DSSI actually returns to DRIVING or not.

3. Borderline/jitter test, to check if your 200 ms threshold is
   realistic once a real, slightly-slower perception pipeline is
   driving this topic instead of a mock:
     ros2 run aer_safety mock_cone_publisher --ros-args -p rate_hz:=3.0
"""

import rclpy
from rclpy.node import Node
from aer_interfaces.msg import ConeArray, DssiStatus, ControlCmd


class MockConePublisher(Node):

    def __init__(self):
        super().__init__('mock_cone_publisher')

        self.declare_parameter('rate_hz', 10.0)
        self.declare_parameter('auto_drop_after_sec', 0.0)   # 0 = disabled
        self.declare_parameter('resume_after_sec', 0.0)      # 0 = disabled

        self.rate_hz = self.get_parameter('rate_hz').value
        self.auto_drop_after_sec = self.get_parameter('auto_drop_after_sec').value
        self.resume_after_sec = self.get_parameter('resume_after_sec').value

        self.cone_pub = self.create_publisher(ConeArray, '/perception/cone_array', 10)

        self.dssi_sub = self.create_subscription(
            DssiStatus, '/vehicle/dssi_status', self.dssi_cb, 10)
        self.cmd_sub = self.create_subscription(
            ControlCmd, '/control/command', self.cmd_cb, 10)

        self.start_time = self.get_clock().now()
        self.publishing = True
        self.last_logged_status = None

        period_sec = 1.0 / self.rate_hz
        self.pub_timer = self.create_timer(period_sec, self.maybe_publish)

        if self.auto_drop_after_sec > 0.0:
            self.drop_timer = self.create_timer(self.auto_drop_after_sec, self.trigger_drop)

        self.get_logger().info(
            f'Publishing fake ConeArray on /perception/cone_array at '
            f'{self.rate_hz:.1f} Hz.'
        )

    def trigger_drop(self):
        self.drop_timer.cancel()  # one-shot: don't let this timer fire again
        if not self.publishing:
            return  # already dropped, don't re-arm
        self.publishing = False
        self.get_logger().warn('--- SIMULATING SENSOR DROPOUT (paused publishing) ---')
        if self.resume_after_sec > 0.0:
            self.resume_timer = self.create_timer(self.resume_after_sec, self.resume_publishing)

    def resume_publishing(self):
        self.resume_timer.cancel()  # one-shot: don't let this timer fire again
        if self.publishing:
            return
        self.publishing = True
        self.get_logger().warn('--- RESUMING PUBLISHING ---')

    def maybe_publish(self):
        if self.publishing:
            self.cone_pub.publish(ConeArray())

    def dssi_cb(self, msg: DssiStatus):
        if msg.status != self.last_logged_status:
            label = 'EMERGENCY' if msg.status == DssiStatus.EMERGENCY else str(msg.status)
            self.get_logger().info(f'[dssi_status changed] -> {label}')
            self.last_logged_status = msg.status

    def cmd_cb(self, msg: ControlCmd):
        if msg.emergency_stop:
            self.get_logger().info(
                f'[control/command] emergency_stop=True, '
                f'target_velocity={msg.target_velocity_mps}, '
                f'brake_pressure={msg.target_brake_pressure_bar} bar'
            )


def main(args=None):
    rclpy.init(args=args)
    node = MockConePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()