FROM osrf/ros:jazzy-desktop

# Install essential build tools & ROS 2 packages
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-colcon-common-extensions \
    ros-jazzy-nav-msgs \
    ros-jazzy-sensor-msgs \
    ros-jazzy-geometry-msgs \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /workspace/aer_ws

# Auto-source ROS 2 Jazzy and workspace setup file
RUN echo 'source /opt/ros/jazzy/setup.bash' >> /root/.bashrc
RUN echo 'if [ -f /workspace/aer_ws/install/setup.bash ]; then source /workspace/aer_ws/install/setup.bash; fi' >> /root/.bashrc

CMD ["/bin/bash"]
