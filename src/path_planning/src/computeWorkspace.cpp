#include "kinematics.hpp"
#include "cast_tools.hpp"
#include "progressbar.hpp"
#include <ros/package.h>
#include <iostream>
#include <fstream>
#include<cmath>

std::string workspace_path = ros::package::getPath("path_planning") + "/data/workspace/workspace.csv";
int n_div = 8;



int iterateJointPos(int n_div, int jnt, std::vector<boost::array<double, 7>> *q_array_list, boost::array<double, 7> &q_array) {
    if (jnt == 7) {
        q_array_list->push_back(q_array);
        return 1;
    }
    for (int i=0; i<=n_div; i++) {
        q_array[jnt] = q_min[jnt]+(q_max[jnt]-q_min[jnt])/n_div*i;
        iterateJointPos(n_div, jnt+1, q_array_list, q_array);
    }
}




int main(int argc, char** argv) {
    //ros::init(argc, argv, "computeWorkspace");
    //ros::NodeHandle n;
//
    //std::string mode;
    //n.getParam("/mode", mode);

    //std::cout << "Mode = " << mode << std::endl;

    //boost::array<double, 7> q_actual_array = {{0, -0.785398163397, 0, -2.3561944899, 0, 1.57079632679, 0.785398163397}};
    //double q7 = -0.238573;
//
    //Eigen::Matrix4d O_T_EE_mat;
    //O_T_EE_mat << -1.0, 0.0, 0.0, 0.0,
    //            0.0, 1.0, 0.0, 0.0,
    //            0.0, 0.0, -1.0, 0.1034,
    //            0.0, 0.0, 0.0, 1.0;
//
    //Eigen::Quaterniond quater = frameToQuaternion(O_T_EE_mat);
    //std::cout << "Quaternion = " << quater.x() << " " << quater.y() << " " << quater.z() << " " << quater.w() << std::endl;
//
    //Eigen::Map< Eigen::Matrix4d > O_T_EE(O_T_EE_mat.data());
//
    //std::cout << "INPUT -----------" << std::endl;
    //std::cout << O_T_EE << std::endl;
//
    //boost::array<boost::array<double, 7>, 4> q_array_list = IK_solver(O_T_EE, q7, q_actual_array, true);
//
    //for (int i=0; i<4; i++) {
    //    std::cout << std::endl << "Array = ";
    //    for (int j=0; j<7; j++) {
    //        std::cout << q_array_list[i][j] << " ";
    //    }
    //    Eigen::Matrix4d res = FK_solver(q_array_list[i], true);
//
    //    std::cout << "OUTPUT -----------" << std::endl;
    //    std::cout << res << std::endl;
    //}

    std::cout << workspace_path << std::endl;
    std::ofstream file;
    file.open(workspace_path);
    file << "Qx, Qy, Qz, Qw, x, y, z" << std::endl;

    std::cout << std::pow(n_div, 7) << std::endl;

    progressbar bar(std::pow(n_div, 7));
    bar.set_niter(std::pow(n_div, 7));
    bar.reset();
    bar.set_done_char("█");

    std::vector<boost::array<double, 7>> *q_array_list = new std::vector<boost::array<double, 7>>;
    //std::vector<Eigen::Matrix4d> *config_list = new std::vector<Eigen::Matrix4d>;
    boost::array<double, 7> q_array;
    iterateJointPos(n_div, 0, q_array_list, q_array);

    
    for (int i=0; i<q_array_list->size(); i++) { 
        Eigen::Matrix4d frame = FK_solver((*q_array_list)[i], false);
        //config_list->push_back(config);
        Eigen::Quaterniond quater = frameToQuaternion(frame);
        file << quater.x() << "," << quater.y() << "," << quater.z() << "," << quater.w() << "," << frame(0,3) << "," << frame(1,3) << "," << frame(2,3) << std::endl;
        bar.update();
    }
}