#include "IK_solver.hpp"
#include "ros/ros.h"
#include "path_planning/IK.h"
#include <eigen3/Eigen/Dense>



bool CallbackIK(path_planning::IK::Request  &req, path_planning::IK::Response &res){
    boost::array<float, 16> O_T_EE_array = req.O_T_EE_array;
    Eigen::Map< Eigen::Matrix<float, 4, 4> > O_T_EE(O_T_EE_array.data());
    float q7 = req.q7;
    boost::array<float, 7> q_actual_array = req.q_actual_array;

    std::cout << O_T_EE << std::endl;

    //boost::array<float, 7> q_array = franka_IK(O_T_EE, q7, q_actual_array);

    //res.q_array = q_array;
    return true;
}



int main(int argc, char **argv){
    ros::init(argc, argv, "IK_server");
    ros::NodeHandle n;

    ros::ServiceServer service = n.advertiseService("IK_service", CallbackIK);
    ROS_INFO("Calculating inverse kinematics.. ");
    ros::spin();

    return 0;
}