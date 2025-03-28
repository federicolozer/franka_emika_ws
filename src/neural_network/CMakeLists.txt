cmake_minimum_required(VERSION 3.10.2)
project(neural_network)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
  roslib
)

find_package(Eigen3 REQUIRED)
find_package(PythonLibs 3.8 REQUIRED)

## Generate added messages and services with any dependencies listed here
generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
  INCLUDE_DIRS include
  LIBRARIES neural_network
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
  ${PYTHON_INCLUDE_DIRS}
  ${catkin_INCLUDE_DIRS}
  ${EIGEN3_INCLUDE_DIRS}
  ../path_planning/include
)

# dataset_creator
add_executable(dataset_creator
  src/dataset_creator.cpp
)

target_link_libraries(dataset_creator
  ${PYTHON_LIBRARIES}
  ${catkin_LIBRARIES}
)

# test_creator
add_executable(test_creator
  src/test_creator.cpp
)

target_link_libraries(test_creator
  ${PYTHON_LIBRARIES}
  ${catkin_LIBRARIES}
)



#############
## Install ##
#############

catkin_install_python(PROGRAMS
  scripts/human_poses.py
  scripts/human_poses_test.py
  scripts/NN_engine.py
  scripts/NN_trainer.py
  scripts/pose_plotter.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
