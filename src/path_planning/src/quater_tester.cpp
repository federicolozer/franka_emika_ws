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

Eigen::IOFormat MatFmt(1, 0, ", ", ";\n", "[", "]", "[", "]");





int main(int argc, char** argv) {
    std::cout << std::fixed << std::setprecision(2);
    
    double x;
    double y;
    double z;

    std::cin >> x;
    std::cin >> y;
    std::cin >> z;
    Eigen::Matrix4d aframe = eulerToFrame({{ x, y, z}}, 0, 0, 0);

    std::cout << std::endl << "Initial EE pose:" << std::endl;
    std::cout << std::fixed << aframe << std::endl << std::endl;
    

    Eigen::Quaterniond quater = frameToQuaternion(aframe);
    
    std::cout << std::endl << "Quaternion:" << std::endl;
    std::cout << "{" << quater.w() << " " << quater.x() << " " << quater.y() << " " << quater.z() << "}" << std::endl;

    Eigen::Matrix4d frame = quaternionToFrame(quater, 0, 0, 0);

    std::cout << std::endl << "Final EE pose:" << std::endl;
    std::cout << std::fixed << frame << std::endl << std::endl;
    

    return 0;
}
