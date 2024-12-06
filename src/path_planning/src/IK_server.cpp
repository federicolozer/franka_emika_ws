#include "IK_solver.hpp"
#include "ros/ros.h"
#include "path_planning/IK.h"
#include <eigen3/Eigen/Dense>



bool CallbackIK(path_planning::IK::Request  &req, path_planning::IK::Response &res){
    boost::array<double, 16> O_T_EE_array;
    for (int i=0; i<sizeof(req.O_T_EE_array)/sizeof(req.O_T_EE_array[0]); i++){
        O_T_EE_array[i] = static_cast<double>(req.O_T_EE_array[i]);
    }
    Eigen::Map< Eigen::Matrix<double, 4, 4> > O_T_EE(O_T_EE_array.data());

    double q7 = static_cast<double>(req.q7);

    boost::array<double, 7> q_actual_array;
    for (int i=0; i<sizeof(req.q_actual_array)/sizeof(req.q_actual_array[0]); i++){
        q_actual_array[i] = static_cast<double>(req.q_actual_array[i]);
    }

    std::cout << O_T_EE << std::endl;

    boost::array<double, 7> q_array = franka_IK(O_T_EE, q7, q_actual_array);

    res.q_array = q_array;
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