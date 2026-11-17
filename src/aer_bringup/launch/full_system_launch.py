import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_bringup = get_package_share_directory('aer_bringup')
    param_file = os.path.join(pkg_bringup, 'config', 'params.yaml')

    return LaunchDescription([
        # 1. Sensor Drivers Layer
        Node(package='aer_drivers', executable='camera_driver', name='camera_driver', parameters=[param_file], output='screen'),
        Node(package='aer_drivers', executable='lidar_driver', name='lidar_driver', parameters=[param_file], output='screen'),
        Node(package='aer_drivers', executable='gps_driver', name='gps_driver', parameters=[param_file], output='screen'),
        Node(package='aer_drivers', executable='imu_driver', name='imu_driver', parameters=[param_file], output='screen'),
        Node(package='aer_drivers', executable='encoder_driver', name='encoder_driver', parameters=[param_file], output='screen'),

        # 2. Sync Layer
        Node(package='aer_sync', executable='camera_sync', name='camera_sync', parameters=[param_file], output='screen'),
        Node(package='aer_sync', executable='localization_sync', name='localization_sync', parameters=[param_file], output='screen'),

        # 3. Perception Layer
        Node(package='aer_perception', executable='lane_detection', name='lane_detection', parameters=[param_file], output='screen'),
        Node(package='aer_perception', executable='object_detection', name='object_detection', parameters=[param_file], output='screen'),
        Node(package='aer_perception', executable='position_estimation', name='position_estimation', parameters=[param_file], output='screen'),
        Node(package='aer_perception', executable='obstacle_detection', name='obstacle_detection', parameters=[param_file], output='screen'),

        # 4. Planning Layer
        Node(package='aer_planning', executable='trajectory_planning', name='trajectory_planning', parameters=[param_file], output='screen'),
        Node(package='aer_planning', executable='global_path_planning', name='global_path_planning', parameters=[param_file], output='screen'),
        Node(package='aer_planning', executable='decision_making', name='decision_making', parameters=[param_file], output='screen'),

        # 5. Safety Monitor & Hardware Bridge Layer
        Node(package='aer_safety', executable='safety_monitor', name='safety_monitor', parameters=[param_file], output='screen'),
        Node(package='aer_bridge', executable='uart_bridge', name='uart_bridge', parameters=[param_file], output='screen'),
    ])
