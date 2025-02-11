#include "IK_solver.hpp"
#include "cast_tools.hpp"
#include <eigen3/Eigen/Dense>
#include <stdexcept>
#include <sys/socket.h>
#include <netinet/in.h>


boost::array<double, 7> q_actual_array = {{0, -0.785398163397, 0, -2.3561944899, 0, 1.57079632679, 0.785398163397}};



void printFrame(Eigen::Matrix4d O_T_EE_tmp) {
    std::array<float, 3> euler = frameToEuler(O_T_EE_tmp); 
    std::string msg1 = "rosrun gazebo_ros spawn_model -file /home/lozer/franka_emika_ws/src/path_planning/data/frame/model.sdf -sdf -model frame ";
    std::stringstream ss;
    ss << "-x " << O_T_EE_tmp(0, 3) << " -y " << O_T_EE_tmp(1, 3) << " -z " << O_T_EE_tmp(2, 3) << " -R " << euler[0]<<  " -P " << euler[1] << " -Y " << euler[2];
    std::string msg2= ss.str();

    std::cout << "----------------------" << std::endl;
    std::cout << (msg1+msg2).c_str() << std::endl;

    
    system("rosservice call gazebo/delete_model '{model_name: frame}'");
    system((msg1+msg2).c_str());
}



boost::array<boost::array<double, 7>, 4> IK_fromQuater(Eigen::Quaterniond quater, std::array<double, 3> O_EE, double q7, bool horz) {  
    std::chrono::time_point<std::chrono::system_clock> t_start = std::chrono::system_clock::now();
    
    std::cout << "quater = " << quater.x() << " " << quater.y() << " " << quater.z() << " " << quater.w() << " " << std::endl;
    std::cout << "O_EE = " << O_EE[0] << " " << O_EE[1] << " " << O_EE[2] << " " << std::endl;

    Eigen::Matrix4d O_T_EE_mat = quaternionToFrame(quater, O_EE[0], O_EE[1], O_EE[2]);

    Eigen::Matrix4d O_T_EE_tmp;   

    if (horz) {
        Eigen::Matrix4d O_T_EE_rot(O_T_EE_mat.data());
        std::cout << "O_T_EE = " << std::endl << O_T_EE_rot << std::endl;
        Eigen::Matrix4d baseToWall_rot;
        baseToWall_rot << 0.0, 0.0, 1.0, -0.333, 
                            0.0, 1.0, 0.0, 0.0, 
                            -1.0, 0.0, 0.0, 0.7, 
                            0.0, 0.0, 0.0, 1.0;
        std::cout << "baseToWall_rot = " << std::endl << baseToWall_rot << std::endl;
        O_T_EE_tmp = baseToWall_rot.inverse()*O_T_EE_rot;
        std::cout << "dot product = " << std::endl << O_T_EE_tmp << std::endl;
    }
    else {
        O_T_EE_tmp = Eigen::Matrix4d(O_T_EE_mat.data());
    }
    Eigen::Map< Eigen::Matrix4d > O_T_EE(O_T_EE_tmp.data());

    std::cout << "O_T_EE = " << std::endl << O_T_EE << std::endl;

    printFrame(O_T_EE_tmp); //display frame in gazebo
    
    boost::array<boost::array<double, 7>, 4> q_array_list = franka_IK(O_T_EE, q7, q_actual_array);

    std::chrono::time_point<std::chrono::system_clock> t_end = std::chrono::system_clock::now();
    std::chrono::duration<double> t_elaps = t_end - t_start;
    std::cout << std::endl << "Elapsed time for IK server: " << t_elaps.count() << "s" << std::endl;
    
    return q_array_list;
}



void server() {
    // Socket initialization
    int serverSocket = socket(AF_INET, SOCK_STREAM, 0);

    sockaddr_in serverAddress;
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_port = htons(8081);
    serverAddress.sin_addr.s_addr = INADDR_ANY;

    bind(serverSocket, (struct sockaddr*)&serverAddress, sizeof(serverAddress));

    while (true) {
        listen(serverSocket, 5);
        int new_socket = accept(serverSocket, nullptr, nullptr);

        std::chrono::time_point<std::chrono::system_clock> t_start = std::chrono::system_clock::now();

        // Recostructing message
        double* buffer = new double[9];
        read(new_socket, buffer, 72);

        std::cout << "buffer = " << buffer[0] << " " << buffer[1] << " " << buffer[2] << " " << buffer[3] << " " << buffer[4] << " " << buffer[5] << " " << buffer[6] << " " << buffer[7] << " " << buffer[8] << " " << std::endl;

        std::array<double, 4> quaternion;
        for (int i=0; i<4; i++) {
            quaternion[i] = buffer[i];
        }
        Eigen::Quaterniond quater(quaternion.data());

        std::cout << "quaternion = " << quater.x() << " " << quater.y() << " " << quater.z() << " " << quater.w() << " " << std::endl;

        std::array<double, 3> O_EE;
        for (int i=0; i<3; i++) {
            O_EE[i] = buffer[i+4];
        }

        std::cout << "O_EE = " << O_EE[0] << " " << O_EE[1] << " " << O_EE[2] << " " << std::endl;
        
        double q7 = buffer[7];

        bool horz = buffer[8];

        boost::array<boost::array<double, 7>, 4> q_array_list = IK_fromQuater(quater, O_EE, q7, horz);

        std::vector<boost::array<double, 7>> q_array;

        for (int i=0; i<4; i++) {
            bool corr = true;
            for (auto arr=q_array_list[i].begin(); arr<q_array_list[i].end(); arr++) {
                if (std::isnan(*arr)) {
                    corr = false;
                    break;
                }
            }

            if (corr == true) {
                q_array.push_back(q_array_list[i]);                
            }
        }

        //std::cout << "q array = " << q_array[0][0] << " " << q_array_list[0][1] << " " << q_array_list[0][2] << " " << q_array_list[0][3] << " " << q_array_list[0][4] << std::endl;

        if (q_array.size() >= 1) {
            send(new_socket, &q_array[0], sizeof(q_array[0]), 0);
        }
        else {
            send(new_socket, 0, 1, 0);
        }
        
        close(new_socket);

        std::chrono::time_point<std::chrono::system_clock> t_end = std::chrono::system_clock::now();
        std::chrono::duration<double> t_elaps = t_end - t_start;
        std::cout << std::endl << "Elapsed time for IK server: " << t_elaps.count() << "s" << std::endl;
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