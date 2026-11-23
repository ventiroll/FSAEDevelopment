import os
import unittest
import yaml


class TestNodeParameters(unittest.TestCase):
    """
    Unit Test Suite for Full-System Node Parameter Validation
    Location: src/aer_bringup/aer_bringup/test/test_nodes_parameters.py
    """

    @classmethod
    def setUpClass(cls):
        test_dir = os.path.dirname(os.path.abspath(__file__))

        # Search relative to this test file first, then fall back to ROS 2 share dir
        candidate_paths = [
            # src/aer_bringup/config/params.yaml
            os.path.normpath(os.path.join(test_dir, '..', '..', 'config', 'params.yaml')),
            # src/aer_bringup/aer_bringup/config/params.yaml (if nested inside inner package)
            os.path.normpath(os.path.join(test_dir, '..', 'config', 'params.yaml')),
        ]

        # Try ROS 2 package share directory if running inside a built workspace
        try:
            from ament_index_python.packages import get_package_share_directory
            share_dir = get_package_share_directory('aer_bringup')
            candidate_paths.append(os.path.join(share_dir, 'config', 'params.yaml'))
        except Exception:
            pass

        cls.params_path = next((p for p in candidate_paths if os.path.exists(p)), None)

        assert cls.params_path is not None, (
            "params.yaml missing! Searched the following candidate locations:\n"
            + "\n".join(candidate_paths)
        )

        with open(cls.params_path, 'r') as f:
            cls.config = yaml.safe_load(f)

    def test_params_file_loaded(self):
        """Ensure params.yaml is non-empty and correctly formatted."""
        self.assertIsNotNone(self.config, "params.yaml file is empty or invalid YAML")
        self.assertIsInstance(self.config, dict, "Root YAML element must be a dictionary")

    def test_global_kinematic_parameters(self):
        """Verify global vehicle kinematics parameters under /** wildcard block."""
        self.assertIn('/**', self.config, "Global '/**' wildcard block missing in params.yaml")

        global_params = self.config['/**']['ros__parameters']

        required_globals = [
            'wheelbase_m',
            'track_width_m',
            'max_steering_angle_rad',
            'max_speed_mps',
            'ebs_trigger_speed_mps'
        ]

        for param in required_globals:
            self.assertIn(param, global_params, f"Global parameter '{param}' missing under /**")

        # Validate physical kinematic constraints
        self.assertGreaterEqual(global_params['wheelbase_m'], 1.525, "Wheelbase must be >= 1.525 m per FSAE rules")
        self.assertGreater(global_params['track_width_m'], 0.0, "Track width must be positive")
        self.assertLessEqual(global_params['max_steering_angle_rad'], 0.50, "Max steering angle exceeds physical rack limits")

    def test_safety_monitor_parameters(self):
        """Verify Safety Monitor node parameter block and FSAE SW-03 200 ms rule."""
        self.assertIn('safety_monitor_node', self.config, "safety_monitor_node block missing from params.yaml")

        safety_params = self.config['safety_monitor_node']['ros__parameters']

        self.assertIn('stale_data_timeout_sec', safety_params)
        self.assertIn('check_frequency_hz', safety_params)
        self.assertIn('enable_hardware_ebs_trip', safety_params)

        # Enforce exact 200 ms FSAE stale data threshold rule
        self.assertAlmostEqual(
            safety_params['stale_data_timeout_sec'],
            0.200,
            places=3,
            msg="FSAE SW-03 rule mandates exact 200 ms (0.200 s) stale data timeout"
        )

    def test_all_14_nodes_coverage(self):
        """Verify that parameter coverage exists for key system node categories."""
        expected_nodes = [
            'safety_monitor_node',
            'controller_node',
            'uart_bridge_node',
            'object_detection_node',
            'lane_detection_node',
            'obstacle_detection_node',
            'position_estimation_node',
            'global_path_planning_node',
            'decision_making_node',
            'camera_driver_node',
            'lidar_driver_node',
            'imu_driver_node'
        ]
        for node_name in expected_nodes:
            self.assertIn(node_name, self.config, f"Node '{node_name}' is missing a parameter block in params.yaml")


if __name__ == '__main__':
    unittest.main()