cmake_minimum_required(VERSION 3.10.2)
project(user_interface)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
)

catkin_package(
  LIBRARIES user_interface
  CATKIN_DEPENDS 
    roscpp 
    rospy 
    std_msgs
)



#############
## Install ##
#############

catkin_install_python(PROGRAMS
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
