import time
import unittest

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, String


class ContinuousInferenceTest(unittest.TestCase):
    """tests the message flow from perception to vehicle control."""

    @classmethod
    def setUpClass(cls):
        """starts ros 2 and creates the test node."""
        rclpy.init()

        cls.node = Node("continuous_inference_test")

        # stores whether each pipeline stage has produced a message.
        cls.received_messages = {
            "/detected_lane": False,
            "/detected_obj": False,
            "/detected_obst": False,
            "/planned_steer": False,
            "/planned_speed": False,
        }

        # stores the time when each topic is first observed.
        cls.first_message_times = {}

        # subscribes to perception outputs.
        cls.node.create_subscription(
            String,
            "/detected_lane",
            lambda msg: cls.record_message("/detected_lane"),
            10,
        )

        cls.node.create_subscription(
            String,
            "/detected_obj",
            lambda msg: cls.record_message("/detected_obj"),
            10,
        )

        cls.node.create_subscription(
            String,
            "/detected_obst",
            lambda msg: cls.record_message("/detected_obst"),
            10,
        )

        # subscribes to control outputs.
        cls.node.create_subscription(
            Float64,
            "/planned_steer",
            lambda msg: cls.record_message("/planned_steer"),
            10,
        )

        cls.node.create_subscription(
            Float64,
            "/planned_speed",
            lambda msg: cls.record_message("/planned_speed"),
            10,
        )

    @classmethod
    def record_message(cls, topic_name):
        """records that a message was received on a topic."""
        cls.received_messages[topic_name] = True

        # records only the first message time for each topic.
        if topic_name not in cls.first_message_times:
            cls.first_message_times[topic_name] = time.monotonic()

    @classmethod
    def tearDownClass(cls):
        """shuts down ros 2 after the test finishes."""
        cls.node.destroy_node()
        rclpy.shutdown()

    def test_perception_to_control_message_flow(self):
        """verifies that messages reach every stage of the pipeline."""
        timeout_seconds = 10.0
        deadline = time.monotonic() + timeout_seconds

        # waits until all expected topics have produced messages.
        while (
            time.monotonic() < deadline
            and not all(self.received_messages.values())
        ):
            rclpy.spin_once(self.node, timeout_sec=0.1)

        missing_topics = [
            topic
            for topic, received in self.received_messages.items()
            if not received
        ]

        self.assertEqual(
            missing_topics,
            [],
            f"the following topics did not receive messages: {missing_topics}",
        )

        # confirms that control messages were received after perception messages.
        perception_times = [
            self.first_message_times["/detected_lane"],
            self.first_message_times["/detected_obj"],
            self.first_message_times["/detected_obst"],
        ]

        control_times = [
            self.first_message_times["/planned_steer"],
            self.first_message_times["/planned_speed"],
        ]

        earliest_perception_time = min(perception_times)
        earliest_control_time = min(control_times)

        self.assertGreaterEqual(
            earliest_control_time,
            earliest_perception_time,
            "control output was received before perception output",
        )


if __name__ == "__main__":
    unittest.main()