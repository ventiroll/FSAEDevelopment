# Aztec Electric Racing (AER) Autonomous ROS 2 Workspace

This repository contains the complete 14-node autonomous vehicle software stack built for ROS 2 Jazzy.

## System Architecture (14 Nodes across 7 Packages)

1. **`aer_drivers`**: Camera, LiDAR, GPS, IMU, Wheel Encoder nodes.
2. **`aer_sync`**: Camera pair downsampling and localization synchronization nodes.
3. **`aer_perception`**: Lane detection (RANSAC/Pure Pursuit), Object detection (YOLO11), Position estimation (EKF), Obstacle detection (DBSCAN).
4. **`aer_planning`**: Trajectory planning, Global path planning, Decision-making funnel.
5. **`aer_safety`**: 200 ms timeout safety monitor (watchdog rule SW-03 / DT.3.2).
6. **`aer_bridge`**: UART hardware serialization to STM32 NUCLEO-G474RE microcontroller.
7. **`aer_bringup`**: Centralized configuration (`params.yaml`) and system launch (`full_system_launch.py`).

## Quick Start (Dev Container)

1. Open this directory in VS Code.
2. Click **Reopen in Container** when prompted.
3. Build & launch:
   ```bash
   ./setup_environment.sh
   ros2 launch aer_bringup full_system_launch.py
   ```
