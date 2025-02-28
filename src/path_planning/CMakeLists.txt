cmake_minimum_required(VERSION 3.10.2)
project(path_planning)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
)

find_package(Eigen3 REQUIRED)
find_package(Franka 0.8.0 REQUIRED)

## Generate services in the 'srv' folder
add_service_files(
  FILES
  IK_fromFrame.srv
  IK_fromQuater.srv
)

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
    xacro
)



###########
## Build ##
###########

include_directories(include
  ${catkin_INCLUDE_DIRS}
  ${Franka_INCLUDE_DIRS}
  ${EIGEN3_INCLUDE_DIRS}
)

# IK server
add_executable(IK_server
  src/IK_server.cpp
)

target_link_libraries(IK_server
  ${catkin_LIBRARIES}
  ${Franka_LIBRARIES}
)




#############
## Install ##
#############

catkin_install_python(PROGRAMS
  scripts/main.py
  scripts/control_tools.py
  scripts/Panda_trajectory_planner.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY robots
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
