cmake_minimum_required(VERSION 3.0.2)
project(neural_network)



find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
)

find_package(Eigen3 REQUIRED)

## Generate added messages and services with any dependencies listed here
generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
  INCLUDE_DIRS include
  LIBRARIES path_planning
  CATKIN_DEPENDS 
    roscpp 
    rospy 
    std_msgs
  DEPENDS #system_lib
)



###########
## Build ##
###########

include_directories(include
  ${catkin_INCLUDE_DIRS}
)



#############
## Install ##
#############

catkin_install_python(PROGRAMS
  scripts/mul_tables_NN.py
  scripts/robot_pose_NN.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
