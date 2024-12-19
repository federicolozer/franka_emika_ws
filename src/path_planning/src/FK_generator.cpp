#include "utils.hpp"
#include "ros/ros.h"
#include <franka_gazebo/model_kdl.h>
#include <Eigen/Dense>
#include <string>
#include <cstdlib>
#include <iostream>
#include <fstream>

const std::array<double, 7> q_min = {{-2.8973, -1.7628, -2.8973, -3.0718, -2.8973, -0.0175, -2.8973}};
const std::array<double, 7> q_max = {{2.8973, 1.7628, 2.8973, -0.0698, 2.8973, 3.7525, 2.8973}};



int main(int argc, char** argv) {
    ros::init(argc, argv, "FK_generator");
    ros::NodeHandle n;

    std::ofstream output;
    output.open("/home/lozer/franka_emika_ws/src/neural_network/data/poses.csv");
    output << "x,y,z,Rx,Ry,Rz,q7\n";

    std::array<double, 7> q = {0, 0, 0, 0, 0, 0, 0};

    for (int n=0; n<111; n++) {
        for (int i=1; i<7; i++) {
            int diff = round((q_max[i] - q_min[i])*100);

            q[i] =  q_min[i] + static_cast<float>(rand() % diff)/100;
        }

        std::array<double, 16> identity = {1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1};
        urdf::Model robot;
        robot.initParam("robot_description");
        franka_gazebo::ModelKDL model = franka_gazebo::ModelKDL(robot, "panda_link0", "panda_link8");

        std::array<double, 16> pose_EE = model.pose(franka::Frame::kFlange, q, identity, identity);

        Eigen::Matrix4d aframe(pose_EE.data());
        std::array<float, 3> euler = frameToEuler(aframe);

        float x = aframe(0, 3);
        float y = aframe(1, 3);
        float z = aframe(2, 3);

        float Rx = euler[0];
        float Ry = euler[1];
        float Rz = euler[2]; 

        output << x << "," << y << "," << z << "," << Rx << "," << Ry << "," << Rz << "," << q[6] << "\n"; 
    }

    output.close();
    return 0;
}
