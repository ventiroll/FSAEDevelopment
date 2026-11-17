#!/bin/bash
set -e

echo "=================================================="
echo " Aztec Electric Racing (AER) Environment Setup"
echo "=================================================="

source /opt/ros/jazzy/setup.bash

echo "[1/2] Building ROS 2 workspace packages..."
colcon build --symlink-install

echo "[2/2] Sourcing workspace overlay..."
source install/setup.bash

echo "Setup Complete! Run: ros2 launch aer_bringup full_system_launch.py"
