#include "cast_tools.hpp"
#include "ros/ros.h"
#include <franka_gazebo/model_kdl.h>
#include <Eigen/Dense>
#include <string>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include "IK_solver.hpp"


Eigen::IOFormat MatFmt(1, 0, ", ", ";\n", "[", "]", "[", "]");





int main(int argc, char** argv) {
    std::cout << std::fixed << std::setprecision(2);

    double w;
    double x;
    double y;
    double z;

    std::cout << "Enter quaternion values.." << std::endl;
    std::cin >> w;
    std::cin >> x;
    std::cin >> y;
    std::cin >> z;

    boost::array<double, 4> quaternion = {w, x, y, z};
    Eigen::Quaterniond aquater(quaternion.data());
    
    std::cout << std::endl << "Initial Quaternion:" << std::endl;
    std::cout << "{" << aquater.w() << " " << aquater.x() << " " << aquater.y() << " " << aquater.z() << "}" << std::endl;

    Eigen::Matrix4d frame = quaternionToFrame(aquater, 0, 0, 0);

    std::cout << std::endl << "EE pose:" << std::endl;
    std::cout << std::fixed << frame << std::endl << std::endl;

    Eigen::Quaterniond quater = frameToQuaternion(frame);
    
    std::cout << std::endl << "Final Quaternion:" << std::endl;
    std::cout << "{" << quater.w() << " " << quater.x() << " " << quater.y() << " " << quater.z() << "}" << std::endl;


    


    return 0;
}
