cmake_minimum_required(VERSION 3.0.2)
project(path_planning)



find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
  franka_gazebo
)

find_package(Eigen3 REQUIRED)

## Generate services in the 'srv' folder
add_service_files(
  FILES
  IK.srv
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
    franka_gazebo
  DEPENDS #system_lib
)



###########
## Build ##
###########

include_directories(include
  ${catkin_INCLUDE_DIRS}
)

# IK server
add_executable(IK_server
  src/IK_server.cpp
)

target_link_libraries(IK_server
  ${catkin_LIBRARIES}
)

# fk test
add_executable(FK_generator
  src/FK_generator.cpp
)

target_link_libraries(FK_generator
  ${catkin_LIBRARIES}
)

# quater test
add_executable(quater_tester
  src/quater_tester.cpp
)

target_link_libraries(quater_tester
  ${catkin_LIBRARIES}
)



#############
## Install ##
#############

catkin_install_python(PROGRAMS
  scripts/controller.py
  scripts/Panda_trajectory_planner.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
