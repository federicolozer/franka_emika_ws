#include "utils.hpp"
#include "ros/ros.h"
#include <franka_gazebo/model_kdl.h>
#include <Eigen/Dense>
#include <string>
#include <cstdlib>
#include <iostream>

const std::array<double, 7> q_min = {{-2.8973, -1.7628, -2.8973, -3.0718, -2.8973, -0.0175, -2.8973}};
const std::array<double, 7> q_max = {{2.8973, 1.7628, 2.8973, -0.0698, 2.8973, 3.7525, 2.8973}};



int main(int argc, char** argv) {
  ros::init(argc, argv, "IK_server");
  ros::NodeHandle n;

  std::array<double, 7> q = {0, 0, 0, 0, 0, 0, 0};

  
  for (int i=1; i<7; i++){
    int diff = round((q_max[i] - q_min[i])*100);
    q[i] +=  q_min[i] + static_cast<float>(rand() % diff)/100;
  }

  std::array<double, 16> identity = {1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1};
  urdf::Model robot;
  robot.initParam("robot_description");
  franka_gazebo::ModelKDL model = franka_gazebo::ModelKDL(robot, "panda_link0", "panda_link8");

  std::array<double, 16> pose_EE = model.pose(franka::Frame::kFlange, q, identity, identity);

  Eigen::Matrix4d aframe(pose_EE.data());
  std::array<float, 3> euler = frameToEuler(aframe);

  x = aframe(0, 3);
  y = aframe(1, 3);
  z = aframe(2, 3);

  Rx = euler[0];
  Ry = euler[1];
  Rz = euler[2];  

  std::ofstream myfile;
      myfile.open ("example.csv");
      myfile << "This is the first cell in the first column.\n";
      myfile << "a,b,c,\n";
      myfile << "c,s,v,\n";
      myfile << "1,2,3.456\n";
      myfile << "semi;colon";
      myfile.close();
      return 0;
}
