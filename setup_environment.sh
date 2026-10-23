#!/bin/bash
echo "=== Setting up AER ROS 2 Jazzy Environment ==="
if [ -f /opt/ros/jazzy/setup.bash ]; then
    source /opt/ros/jazzy/setup.bash
fi
colcon build --symlink-install
if [ -f install/setup.bash ]; then
    source install/setup.bash
fi
echo "Setup Complete! Run: ros2 launch aer_bringup simulation_launch.py"
