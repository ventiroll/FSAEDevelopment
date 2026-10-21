from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_bringup = get_package_share_directory('aer_bringup')
    param_file = os.path.join(pkg_bringup, 'config', 'params.yaml')

    return LaunchDescription([
        Node(package='aer_perception', executable='mock_sensor_node', name='mock_sensor_node', output='screen'),
        Node(package='aer_planning', executable='path_planner_node', name='path_planner_node', output='screen'),
        Node(package='aer_control', executable='controller_node', name='controller_node', parameters=[param_file], output='screen'),
        Node(package='aer_safety', executable='safety_monitor_node', name='safety_monitor_node', output='screen'),
        Node(package='aer_stm32_bridge', executable='micro_ros_bridge_node', name='micro_ros_bridge_node', output='screen'),
    ])
