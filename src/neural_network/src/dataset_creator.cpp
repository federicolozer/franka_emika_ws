#include <eigen3/Eigen/Dense>
#include <array>
#include <cmath>
#include <iostream>
#include <fstream>
#include <Python.h>



int main() {
    std::ofstream file;

    file.open("/home/lozer/franka_emika_ws/src/neural_network/data/dataset/humanPoses.csv");
    file << "x, y, z, Q0, Q1, Q2, Q3, q7" << std::endl;
    file.close();

    return 0;
}
