#include <franka_gazebo/model_kdl.h>

#include <Eigen/Dense>
#include <string>
#include <ros/ros.h>
#include <chrono>




int main(int argc, char** argv) {
  ros::init(argc, argv, "fk_test");
  ros::NodeHandle nh;
  
  std::array<double, 7> q = {0, -0.785398163397, 0, -2.3561944899, 0, 1.57079632679, 0.785398163397};

  for (int i=0; i<10; i++){
    std::cout << rand() << std::endl;
  }



  std::array<double, 16> identity = {1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1};
  urdf::Model robot;
  robot.initParam("robot_description");
  //model = std::make_unique<franka_gazebo::ModelKDL>(robot, "panda_link0", "panda_link8");
  franka_gazebo::ModelKDL model = franka_gazebo::ModelKDL(robot, "panda_link0", "panda_link8");

  std::array<double, 16> pose_EE = model.pose(franka::Frame::kFlange, q, identity, identity);

  Eigen::Matrix4d aframe(Eigen::Matrix4d(pose_EE.data()));

  std::cout << "Actual frame:" << std::endl;
  std::cout << aframe << std::endl << std::endl;
}
