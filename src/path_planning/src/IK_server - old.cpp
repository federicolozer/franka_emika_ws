#include "IK_solver.hpp"
#include "ros/ros.h"
#include "path_planning/IK.h"
#include <eigen3/Eigen/Dense>
#include <franka_gazebo/model_kdl.h>


Eigen::IOFormat MatFmt(1, 0, ", ", ";\n", "[", "]", "[", "]");



bool CallbackIK(path_planning::IK::Request  &req, path_planning::IK::Response &res) {
    boost::array<double, 16> O_T_EE_array;
    for (int i=0; i<sizeof(req.O_T_EE_array)/sizeof(req.O_T_EE_array[0]); i++) {
        O_T_EE_array[i] = static_cast<double>(req.O_T_EE_array[i]);
    }
    Eigen::Map< Eigen::Matrix<double, 4, 4> > O_T_EE(O_T_EE_array.data());

    double q7 = static_cast<double>(req.q7);

    boost::array<double, 7> q_actual_array;
    for (int i=0; i<sizeof(req.q_actual_array)/sizeof(req.q_actual_array[0]); i++) {
        q_actual_array[i] = static_cast<double>(req.q_actual_array[i]);
    }

    boost::array<boost::array<double, 7>, 4> q_array_array = franka_IK(O_T_EE, q7, q_actual_array);

    std::cout << std::endl << std::endl;
    std::cout << "--- q_array array:" << std::endl;
    boost::array<double, 7> q_array_temp;
    for (int j=0; j<4; j++) {
        q_array_temp = q_array_array[j];
        for (int i=0; i<sizeof(q_array_temp)/sizeof(q_array_temp[0]); i++) {
            std::cout << q_array_temp[i] << " ";
        }
        std::cout << std::endl;
    }

    boost::array<double, 7> q_array = franka_IK_CC(O_T_EE, q7, q_actual_array);

    std::cout << "--- q_array:" << std::endl;
    for (int i=0; i<sizeof(q_array)/sizeof(q_array[0]); i++) {
        std::cout << q_array[i] << " ";
    }
    std::cout << std::endl;



    //----------------------------------------------------------------------------

    /*std::cout << std::endl << "Initial EE pose:" << std::endl;
    std::cout << std::fixed << std::setprecision(1) << O_T_EE.format(MatFmt) << std::endl << std::endl;

    std::array<double, 16> identity = {1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1};
    urdf::Model robot;
    robot.initParam("robot_description");
    franka_gazebo::ModelKDL model = franka_gazebo::ModelKDL(robot, "panda_link0", "panda_link8");

    std::cout << "q_array_new:" << std::endl;
    std::array<double, 7> q_array_new;
    for (int i=0; i<sizeof(q_array)/sizeof(q_array[0]); i++) {
        q_array_new[i] = q_array[i];
    }

    std::array<double, 16> O_T_EE_array_new = model.pose(franka::Frame::kFlange, q_array_new, identity, identity);

    Eigen::Map< Eigen::Matrix<double, 4, 4> > O_T_EE_new(O_T_EE_array_new.data());

    std::cout << std::endl << "Final EE pose:" << std::endl;
    std::cout << std::fixed << std::setprecision(1) << O_T_EE_new.format(MatFmt) << std::endl << std::endl; */

    //----------------------------------------------------------------------------
    




    res.q_array = q_array;
    return true;
}



int main(int argc, char **argv) {
    ros::init(argc, argv, "IK_server");
    ros::NodeHandle n;

    std::fixed;
    std::setprecision(2);

    ros::ServiceServer service = n.advertiseService("IK_service", CallbackIK);
    ROS_INFO("Calculating inverse kinematics.. ");
    ros::spin();

    return 0;
}