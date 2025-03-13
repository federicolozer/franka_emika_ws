#include "kinematics.hpp"
#include "cast_tools.hpp"




int main(int argc, char** argv) {
    //ros::init(argc, argv, "computeWorkspace");
    //ros::NodeHandle n;
//
    //std::string mode;
    //n.getParam("/mode", mode);

    //std::cout << "Mode = " << mode << std::endl;

    boost::array<double, 7> q_actual_array = {{0, -0.785398163397, 0, -2.3561944899, 0, 1.57079632679, 0.785398163397}};
    std::array<double, 4> quaternion = {{0.573172, 0.709486, 0.35312, 0.208349}};
    Eigen::Quaterniond quater(quaternion.data());
    double q7 = -0.238573;

    Eigen::Matrix4d O_T_EE_mat = quaternionToFrame(quater, 0.439546, 0.108194, 0.418348);
    Eigen::Map< Eigen::Matrix4d > O_T_EE(O_T_EE_mat.data());

    std::cout << "INPUT -----------" << std::endl;
    std::cout << O_T_EE << std::endl;

    boost::array<boost::array<double, 7>, 4> q_array_list = IK_solver(O_T_EE, q7, q_actual_array, false);

    for (int i=0; i<4; i++) {
        std::cout << std::endl << "Array = ";
        for (int j=0; j<7; j++) {
            std::cout << q_array_list[i][j] << " ";
        }
        Eigen::Matrix4d res = FK_solver(q_array_list[i], true);

        std::cout << "OUTPUT -----------" << std::endl;
        std::cout << res << std::endl;
    }
}