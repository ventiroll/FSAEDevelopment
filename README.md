# SDSU Aztec Electric Racing (AER) - ROS 2 & Micro-ROS Inverter Demo Package

## Overview
This standalone 1-node ROS 2 package (`aer_demo_inverter`) is specifically designed for live presentations and proof-of-concept hardware demos. 

It runs on the **NVIDIA Jetson Orin Nano Super** without requiring physical sensors or perception pipelines. Instead, you can pass command-line arguments (e.g., `throttle_mode:='slow'`, `'medium'`, or `'hard'`) to instantly push target velocity instructions over ROS 2 to an **STM32 NUCLEO-G474RE** microcontroller running **micro-ROS**. 

The STM32 parses the ROS 2 message (`/control/command`) and outputs a proportional **0–5V analog DAC signal** directly to the **Cascadia Motion CM200 Inverter**.

---

## Architecture Flow

```text
[ MacBook / Jetson CLI ] 
       │  (Passes argument: throttle_mode:='slow' | 'medium' | 'hard')
       ▼
[ Jetson: demo_inverter_node ] 
       │  (Publishes aer_interfaces/msg/ControlCmd @ 10 Hz)
       ▼  [Topic: /control/command]
[ STM32 Microcontroller (micro-ROS) ] 
       │  (Converts target_velocity_mps -> 12-bit DAC voltage)
       ▼  [0 – 5V Analog DAC Hardware Output]
[ Cascadia Motion CM200 Inverter ] ──► Motor Torque / Spin
```

---

## Throttle Presets & Voltage Mapping

| Preset Command | Target Speed | STM32 DAC Voltage Output | Inverter Action |
| :--- | :--- | :--- | :--- |
| `throttle_mode:=slow` | **1.0 m/s** | **~1.0 V DC** | ~20% Low Speed / Demonstration |
| `throttle_mode:=medium` | **2.5 m/s** | **~2.5 V DC** | ~50% Mid Speed / Cruise |
| `throttle_mode:=hard` | **5.0 m/s** | **~4.5 V DC** | ~90% High Torque Acceleration |

---

## Quick Start / Presentation Commands

### 1. Build and Source the Package
```bash
colcon build --packages-select aer_demo_inverter
source install/setup.bash
```

### 2. Run Demo Node with Presets (Method A: `ros2 run`)
```bash
# Demo Preset 1: Slow / Low Voltage
ros2 run aer_demo_inverter demo_inverter_node --ros-args -p throttle_mode:=slow

# Demo Preset 2: Medium / Mid Voltage (Default)
ros2 run aer_demo_inverter demo_inverter_node --ros-args -p throttle_mode:=medium

# Demo Preset 3: Hard / High Voltage
ros2 run aer_demo_inverter demo_inverter_node --ros-args -p throttle_mode:=hard
```

### 3. Run Demo Node via Launch File (Method B: `ros2 launch`)
```bash
ros2 launch aer_demo_inverter demo_launch.py throttle_mode:=hard
```

### 4. Custom Speed Override (Direct m/s input)
```bash
# Pass custom target speed in meters/second (e.g. 3.5 m/s)
ros2 run aer_demo_inverter demo_inverter_node --ros-args -p target_speed_mps:=3.5
```

### 5. Inspect Live Topic Stream (Second Terminal Tab for Demo Screen)
```bash
ros2 topic echo /control/command
```

---

## File Layout Included in Zip Package

- `aer_demo_inverter/`:
  - `aer_demo_inverter/demo_inverter_node.py`: ROS 2 Python Node with CLI presets and logging.
  - `launch/demo_launch.py`: ROS 2 launch file supporting launch arguments.
  - `config/demo_params.yaml`: Central parameter configuration.
  - `package.xml` & `setup.py`: Standard ROS 2 Jazzy build files.
- `stm32_micro_ros_demo/`:
  - `main.cpp`: Complete C++ micro-ROS firmware for STM32 DAC signal generation.
