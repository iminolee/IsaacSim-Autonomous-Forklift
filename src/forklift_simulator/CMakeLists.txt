cmake_minimum_required(VERSION 2.8.3)
project(forklift_simulator)

## Compile as C++11, supported in ROS Kinetic and newer
add_compile_options(-std=c++11)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  urdf
)

catkin_package(
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

# add_executable(key_control src/key_control.cpp)
# target_link_libraries(key_control ${catkin_LIBRARIES})
