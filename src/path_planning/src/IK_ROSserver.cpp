#include "kinematics.hpp"
#include "cast_tools.hpp"
#include "ros/ros.h"
#include "path_planning/IK_fromFrame.h"
#include "path_planning/IK_fromQuater.h"
#include <eigen3/Eigen/Dense>
#include <stdexcept>
#include <sys/socket.h>
#include <netinet/in.h>
//dut di comeda

Eigen::IOFormat MatFmt(1, 0, ", ", ";\n", "[", "]", "[", "]");
boost::array<double, 7> q_actual_array = {{0, -0.785398163397, 0, -2.3561944899, 0, 1.57079632679, 0.785398163397}};



bool CallbackIK_fromFrame(path_planning::IK_fromFrame::Request &req, path_planning::IK_fromFrame::Response &res) {
    boost::array<double, 16> O_T_EE_array;
    for (int i=0; i<sizeof(req.O_T_EE_array)/sizeof(req.O_T_EE_array[0]); i++) {
        O_T_EE_array[i] = static_cast<double>(req.O_T_EE_array[i]);
    }
    
    Eigen::Matrix<double, 4, 4> O_T_EE_tmp;

    bool horz = req.horz;
    if (horz) {
        Eigen::Matrix<double, 4, 4> O_T_EE_rot(O_T_EE_array.data());
        std::cout << "O_T_EE = " << std::endl << O_T_EE_rot << std::endl;
        Eigen::Matrix<double, 4, 4> baseToWall_rot;
        baseToWall_rot << 0.0, 0.0, 1.0, -0.333, 
                            0.0, 1.0, 0.0, 0.0, 
                            -1.0, 0.0, 0.0, 0.7, 
                            0.0, 0.0, 0.0, 1.0;
        std::cout << "baseToWall_rot = " << std::endl << baseToWall_rot << std::endl;
        O_T_EE_tmp = baseToWall_rot.inverse()*O_T_EE_rot;
        std::cout << "dot product = " << std::endl << O_T_EE_tmp << std::endl;
    }
    else {
        O_T_EE_tmp = Eigen::Matrix<double, 4, 4>(O_T_EE_array.data());
    }
    Eigen::Map< Eigen::Matrix<double, 4, 4> > O_T_EE(O_T_EE_tmp.data());

    double q7 = static_cast<double>(req.q7);

    boost::array<double, 7> q_actual_array;
    for (int i=0; i<sizeof(req.q_actual_array)/sizeof(req.q_actual_array[0]); i++) {
        q_actual_array[i] = static_cast<double>(req.q_actual_array[i]);
    }


    boost::array<boost::array<double, 7>, 4> q_array_list = IK_solver(O_T_EE, q7, q_actual_array, false);

    res.q_array_1 = q_array_list[0];
    res.q_array_2 = q_array_list[1];
    res.q_array_3 = q_array_list[2];
    res.q_array_4 = q_array_list[3];

    return true;
}



bool CallbackIK_fromQuater(path_planning::IK_fromQuater::Request &req, path_planning::IK_fromQuater::Response &res) {  
    std::chrono::time_point<std::chrono::system_clock> t_start = std::chrono::system_clock::now();
    
    boost::array<double, 4> quaternion;
    for (int i=0; i<sizeof(req.quaternion)/sizeof(req.quaternion[0]); i++) {
        quaternion[i] = static_cast<double>(req.quaternion[i]);
    }
    Eigen::Quaterniond quater(quaternion.data());

    std::cout << "quaternion = " << quater.x() << " " << quater.y() << " " << quater.z() << " " << quater.w() << " " << std::endl;

    boost::array<double, 3> O_EE;
    for (int i=0; i<sizeof(req.O_EE)/sizeof(req.O_EE[0]); i++) {
        O_EE[i] = static_cast<double>(req.O_EE[i]);
    }

    Eigen::Matrix4d O_T_EE_mat = quaternionToFrame(quater, O_EE[0], O_EE[1], O_EE[2]);
    //Eigen::Map< Eigen::Matrix<double, 4, 4> > O_T_EE(O_T_EE_mat.data());

    Eigen::Matrix<double, 4, 4> O_T_EE_tmp;

    bool horz = req.horz;
    if (horz) {
        Eigen::Matrix<double, 4, 4> O_T_EE_rot(O_T_EE_mat.data());
        std::cout << "O_T_EE = " << std::endl << O_T_EE_rot << std::endl;
        Eigen::Matrix<double, 4, 4> baseToWall_rot;
        baseToWall_rot << 0.0, 0.0, 1.0, -0.333, 
                            0.0, 1.0, 0.0, 0.0, 
                            -1.0, 0.0, 0.0, 0.7, 
                            0.0, 0.0, 0.0, 1.0;
        std::cout << "baseToWall_rot = " << std::endl << baseToWall_rot << std::endl;
        O_T_EE_tmp = baseToWall_rot.inverse()*O_T_EE_rot;
        std::cout << "dot product = " << std::endl << O_T_EE_tmp << std::endl;
    }
    else {
        O_T_EE_tmp = Eigen::Matrix<double, 4, 4>(O_T_EE_mat.data());
    }
    Eigen::Map< Eigen::Matrix<double, 4, 4> > O_T_EE(O_T_EE_tmp.data());

    std::cout << "O_T_EE = " << std::endl << O_T_EE << std::endl;

    double q7 = static_cast<double>(req.q7);

    boost::array<double, 7> q_actual_array;
    for (int i=0; i<sizeof(req.q_actual_array)/sizeof(req.q_actual_array[0]); i++) {
        q_actual_array[i] = static_cast<double>(req.q_actual_array[i]);
    }

    boost::array<boost::array<double, 7>, 4> q_array_list = IK_solver(O_T_EE, q7, q_actual_array, false);

    res.q_array_1 = q_array_list[0];
    res.q_array_2 = q_array_list[1];
    res.q_array_3 = q_array_list[2];
    res.q_array_4 = q_array_list[3];

    std::chrono::time_point<std::chrono::system_clock> t_end = std::chrono::system_clock::now();
    std::chrono::duration<double> t_elaps = t_end - t_start;
    std::cout << std::endl << "Elapsed time for IK server: " << t_elaps.count() << "s" << std::endl;
    return true;
}




int main(int argc, char** argv) {
    ros::init(argc, argv, "IK_server");
    ros::NodeHandle n;

    std::fixed;
    std::setprecision(2);
    
    if (argc < 2) {
        std::cerr << "Error: mandatory argument" << std::endl;
    }
    else {
        if (std::string(argv[1]) == "--fromFrame") {
            ros::ServiceServer service = n.advertiseService("IK_service", CallbackIK_fromFrame);
            std::cout << std::endl << "Running" << std::endl;
            ros::spin();
        }
        else if (std::string(argv[1]) == "--fromQuater") {
            ros::ServiceServer service = n.advertiseService("IK_service", CallbackIK_fromQuater);
            std::cout << std::endl << "Running" << std::endl;
            ros::spin();
        }        
    }
    
    return 0;
}