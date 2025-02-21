#include "IK_solver.hpp"
#include "cast_tools.hpp"
#include <eigen3/Eigen/Dense>
#include <stdexcept>
#include <sys/socket.h>
#include <netinet/in.h>
#include <cmath>


boost::array<double, 7> q_actual_array = {{0, -0.785398163397, 0, -2.3561944899, 0, 1.57079632679, 0.785398163397}};



void printFrame(Eigen::Matrix4d O_T_EE_tmp) {
    std::array<float, 3> euler = frameToEuler(O_T_EE_tmp); 
    std::string msg1 = "rosrun gazebo_ros spawn_model -file /home/lozer/franka_emika_ws/src/path_planning/data/models/frame/model.sdf -sdf -model frame ";
    std::stringstream ss;
    ss << "-x " << O_T_EE_tmp(0, 3) << " -y " << O_T_EE_tmp(1, 3) << " -z " << O_T_EE_tmp(2, 3) << " -R " << euler[0]<<  " -P " << euler[1] << " -Y " << euler[2];
    std::string msg2 = ss.str();

    //rosrun gazebo_ros spawn_model -file /home/lozer/franka_emika_ws/src/path_planning/data/models/human/model.sdf -sdf -model human
    
    system("rosservice call gazebo/delete_model '{model_name: frame}'");
    system((msg1+msg2).c_str());
}



boost::array<boost::array<double, 7>, 4> IK_fromQuater(Eigen::Quaterniond quater, std::array<double, 3> O_EE, double q7, int mode, bool dispFrame) {  
    Eigen::Matrix4d O_T_EE_mat = quaternionToFrame(quater, O_EE[0], O_EE[1], O_EE[2]);
    Eigen::Matrix4d O_T_EE_tmp;   

    if (mode == 1) { // horz
        Eigen::Matrix4d O_T_EE_rot(O_T_EE_mat.data());
        Eigen::Matrix4d baseToWall_rot;
        baseToWall_rot << 0.0, 0.0, 1.0, -0.333,
                            0.0, -1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0, 0.7,
                            0.0, 0.0, 0.0, 1.0;
        O_T_EE_tmp = baseToWall_rot.inverse()*O_T_EE_rot;
    }
    else if (mode == 2) { // horz_rev
        Eigen::Matrix4d O_T_EE_rot(O_T_EE_mat.data());
        Eigen::Matrix4d baseToWall_rot;
        baseToWall_rot << 0.0, 0.0, 1.0, -0.333,
                            0.0, 1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0, 0.7,
                            0.0, 0.0, 0.0, 1.0;
        O_T_EE_tmp = baseToWall_rot.inverse()*O_T_EE_rot;
    }
    else if (mode == 3) { // ceil
        Eigen::Matrix4d O_T_EE_rot(O_T_EE_mat.data());
        Eigen::Matrix4d baseToWall_rot;
        baseToWall_rot << 1.0, 0.0, 0.0, 0.0,
                            0.0, -1.0, 0.0, 0.0,
                            0.0, 0.0, -1.0, 1.033,
                            0.0, 0.0, 0.0, 1.0;
        O_T_EE_tmp = baseToWall_rot.inverse()*O_T_EE_rot;
    }
    else {
        O_T_EE_tmp = Eigen::Matrix4d(O_T_EE_mat.data());
    }
    Eigen::Map< Eigen::Matrix4d > O_T_EE(O_T_EE_tmp.data());

    if (dispFrame) {
        printFrame(O_T_EE_mat); //display frame in gazebo
    }
    boost::array<boost::array<double, 7>, 4> q_array_list = franka_IK(O_T_EE, q7, q_actual_array);

    return q_array_list;
}



void server() {
    // Socket initialization
    int serverSocket = socket(AF_INET, SOCK_STREAM, 0);

    sockaddr_in serverAddress;
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_port = htons(8080);
    serverAddress.sin_addr.s_addr = INADDR_ANY;

    bind(serverSocket, (struct sockaddr*)&serverAddress, sizeof(serverAddress));

    while (true) {
        listen(serverSocket, 5);
        int new_socket = accept(serverSocket, nullptr, nullptr);

        std::chrono::time_point<std::chrono::system_clock> t_start = std::chrono::system_clock::now();

        // Recostructing message
        char msg;
        recv(new_socket, &msg, 1, 0);

        if (msg == '0') {
            std::cout << "Server shut down" << std::endl;
            close(new_socket);
            break;
        }

        int nArgs = 10;
        double* buffer = new double[nArgs];
        recv(new_socket, buffer, nArgs*8, 0);

        std::array<double, 4> quaternion;
        for (int i=0; i<4; i++) {
            quaternion[i] = buffer[i];
        }
        Eigen::Quaterniond quater(quaternion.data());

        std::array<double, 3> O_EE;
        for (int i=0; i<3; i++) {
            O_EE[i] = buffer[i+4];
        }
  
        double q7 = buffer[7];
        int mode = buffer[8];
        bool dispFrame = buffer[9];

        std::cout << "mode = " << std::endl << mode << std::endl;

        boost::array<boost::array<double, 7>, 4> q_array_list = IK_fromQuater(quater, O_EE, q7, mode, dispFrame);

        send(new_socket, &q_array_list[0], sizeof(q_array_list[0]), 0);
        send(new_socket, &q_array_list[1], sizeof(q_array_list[1]), 0);
        send(new_socket, &q_array_list[2], sizeof(q_array_list[2]), 0);
        send(new_socket, &q_array_list[3], sizeof(q_array_list[3]), 0);
        
        close(new_socket);

        delete buffer;

        std::chrono::time_point<std::chrono::system_clock> t_end = std::chrono::system_clock::now();
        std::chrono::duration<double> t_elaps = t_end - t_start;
        std::cout << std::endl << "----------------" << std::endl;
        std::cout << std::endl << "Elapsed time for IK server: " << t_elaps.count() << "s" << std::endl;
        std::cout << "----------------" << std::endl;
    }
    
    close(serverSocket);
}




int main(int argc, char** argv) {
    ros::init(argc, argv, "IK_server");
    ros::NodeHandle n;

    std::fixed;
    std::setprecision(2);

    std::cout << "Ready" << std::endl;
    server();

    return 0;
}