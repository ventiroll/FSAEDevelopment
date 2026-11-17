from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    throttle_mode_arg = DeclareLaunchArgument(
        'throttle_mode',
        default_value='medium',
        description='Throttle preset mode: slow (1.0 m/s), medium (2.5 m/s), hard (5.0 m/s)'
    )

    return LaunchDescription([
        throttle_mode_arg,
        Node(
            package='aer_demo_inverter',
            executable='demo_inverter_node',
            name='demo_inverter_node',
            parameters=[{
                'throttle_mode': LaunchConfiguration('throttle_mode'),
            }],
            output='screen'
        )
    ])
