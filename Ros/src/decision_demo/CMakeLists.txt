cmake_minimum_required(VERSION 3.1)
project(decision_demo)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake_module)
set(CMAKE_BUILD_TYPE Release)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
)

find_package(Eigen3 REQUIRED)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

catkin_package()
