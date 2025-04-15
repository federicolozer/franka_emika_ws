cmake_minimum_required(VERSION 3.10.2)
project(path_planning)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
  xacro
  roslib
  #scipy
)

find_package(Eigen3 REQUIRED)

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
    roslib
)



###########
## Build ##
###########

include_directories(include
  ${catkin_INCLUDE_DIRS}
  ${EIGEN3_INCLUDE_DIRS}
  ../neural_network/include
)

# IK server
add_executable(IK_server
  src/IK_server.cpp
)

target_link_libraries(IK_server
  ${catkin_LIBRARIES}
)

# computeWorkspace
add_executable(computeWorkspace
  src/computeWorkspace.cpp
)

target_link_libraries(computeWorkspace
  ${catkin_LIBRARIES}
)




#############
## Install ##
#############

catkin_install_python(PROGRAMS
  scripts/cl_main.py
  scripts/gui_main.py
  scripts/controller.py
  scripts/Panda_trajectory_planner.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY robots
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
