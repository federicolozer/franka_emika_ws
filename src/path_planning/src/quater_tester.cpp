#include "utils.hpp"
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

    /*double x;
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
    std::cout << std::fixed << frame << std::endl << std::endl;*/

    Eigen::Quaterniond quater(0.9332,  0.0248,  0.2982, -0.1991);  //------------------- MOD
    
    std::cout << std::endl << "Quaternion:" << std::endl;
    std::cout << "{" << quater.w() << " " << quater.x() << " " << quater.y() << " " << quater.z() << "}" << std::endl;

    Eigen::Matrix4d frame = quaternionToFrame(quater, 0.3839, -0.3270,  0.4975);  //------------------- MOD

    Eigen::Map< Eigen::Matrix<double, 4, 4> > O_T_EE(frame.data());
    std::cout << O_T_EE << std::endl << std::endl;

    double q7 = 0.2979;  //------------------- MOD

    boost::array<double, 7> q_actual_array = {{0, -0.785398163397, 0, -2.3561944899, 0, 1.57079632679, 0.785398163397}};

    boost::array<double, 7> q_array = franka_IK(O_T_EE, q7, q_actual_array);

    std::cout << "q_array:" << std::endl;
    for (int i=0; i<sizeof(q_array)/sizeof(q_array[0]); i++){
        std::cout << std::endl << q_array[i] << " " << std::endl;
    }
    

    return 0;
}
