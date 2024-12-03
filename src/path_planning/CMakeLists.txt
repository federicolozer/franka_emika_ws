cmake_minimum_required(VERSION 3.0.2)
project(path_planning)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
)

catkin_package(
INCLUDE_DIRS include
LIBRARIES path_planning
CATKIN_DEPENDS roscpp rospy std_msgs
DEPENDS system_lib
)

include_directories(
include
  ${catkin_INCLUDE_DIRS}
)

add_library(${PROJECT_NAME}
  src/panda_joint_position_controller.cpp
)

# installations
install(TARGETS path_planning
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
install(DIRECTORY include/${PROJECT_NAME}/
  DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
)
install(DIRECTORY launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
install(DIRECTORY config
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
install(FILES panda_controllers_plugin.xml
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
catkin_install_python(PROGRAMS
  scripts/controller.py
  scripts/Panda_trajectory_planner.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

