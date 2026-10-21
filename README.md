# SDSU Aztec Electric Racing (AER) - Formula SAE Driverless ROS 2 Workspace

This repository contains the autonomous software infrastructure for San Diego State University (SDSU) Aztec Electric Racing (Project 44).
Built for **ROS 2 Jazzy Jalisco** on **Ubuntu 24.04 LTS ARM64** (matching the NVIDIA Jetson Orin Nano Super & STM32 NUCLEO-G474RE ECU architecture).

---

## Workspace Structure
- **`aer_interfaces`**: Custom ROS 2 message definitions (`Cone`, `ConeArray`, `ControlCmd`, `VehicleState`, `DssiStatus`).
- **`aer_perception`**: Camera/LiDAR processing nodes & synthetic cone publisher.
- **`aer_planning`**: Track centerline and trajectory waypoint planner ($\ge 10\text{ Hz}$).
- **`aer_control`**: Stanley steering controller & velocity regulator ($\ge 10\text{ Hz}$).
- **`aer_safety`**: Stale data monitor enforcing Rule SW-03 ($\le 200\text{ ms}$ timeout) & DSSI status state machine.
- **`aer_stm32_bridge`**: CAN/Serial communication bridge connecting ROS 2 to the STM32 vehicle ECU.
- **`aer_bringup`**: Central configuration (`params.yaml`) and launch files (`simulation_launch.py` and `vehicle_launch.py`).

---

## 🚀 Option 2: Running with VS Code Dev Containers (Recommended for Mac)

### Prerequisites on Mac:
1. Install **VS Code** on macOS.
2. Install the **Dev Containers** extension in VS Code.
3. Install **OrbStack** (or Docker Desktop) on macOS.

### Quick Start:
1. Open the `aer_ws` folder in VS Code (`File -> Open Folder... -> aer_ws`).
2. VS Code will detect the `.devcontainer` folder and prompt: **"Reopen in Container"**. Click it!
3. VS Code will automatically start the official `ros:jazzy-desktop` container, install ROS dependencies, compile all 6 packages, and set up your IntelliSense.
4. Open the VS Code integrated terminal (`Ctrl + ~`) and launch the simulation:
   ```bash
   ros2 launch aer_bringup simulation_launch.py
   ```

---

## Manual Build (Local Linux / Jetson)
1. Make setup script executable:
   ```bash
   chmod +x setup_environment.sh
   ./setup_environment.sh
   ```
2. Launch developer simulation with RViz2:
   ```bash
   ros2 launch aer_bringup simulation_launch.py
   ```
