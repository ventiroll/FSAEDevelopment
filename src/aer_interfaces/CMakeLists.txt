cmake_minimum_required(VERSION 3.8)
project(aer_interfaces)

find_package(ament_cmake REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Cone.msg"
  "msg/ConeArray.msg"
  "msg/ControlCmd.msg"
  "msg/VehicleState.msg"
  "msg/DssiStatus.msg"
  DEPENDENCIES std_msgs geometry_msgs
)

ament_package()
