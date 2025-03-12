#pragma once

#ifndef CAST_TOOLS
#define CAST_TOOLS

#include <eigen3/Eigen/Dense>
#include <array>
#include <cmath>
#include <iostream>



std::array<float, 3> frameToEuler(const Eigen::Matrix4d frame) {
    float Rx;
    float Ry;
    float Rz;

    if (abs(frame(2, 0)) != 1) {
        Ry = - std::asin(frame(2, 0));
        Rx = std::atan2(frame(2, 1)/std::cos(Ry), frame(2, 2)/std::cos(Ry));
        Rz = std::atan2(frame(1, 0)/std::cos(Ry), frame(0, 0)/std::cos(Ry));
    }

    std::array<float, 3> euler = {{Rx, Ry, Rz}};
    return euler;
}



Eigen::Matrix4d eulerToFrame(const std::array<float, 3> euler, const float x, const float y, const float z) {
    Eigen::Matrix4d frame;
    frame << 0, 0, 0, 0,
             0, 0, 0, 0,
             0, 0, 0, 0,
             0, 0, 0, 1;

    float Rx = euler[0];
    float Ry = euler[1];
    float Rz = euler[2];

    frame(0, 0) = std::cos(Ry)*std::cos(Rz);
    frame(1, 0) = std::cos(Ry)*std::sin(Rz);
    frame(2, 0) = -std::sin(Ry);

    frame(0, 1) = std::sin(Rx)*std::sin(Ry)*std::cos(Rz) - std::cos(Rx)*std::sin(Rz);
    frame(1, 1) = std::sin(Rx)*std::sin(Ry)*std::sin(Rz) + std::cos(Rx)*std::cos(Rz);
    frame(2, 1) = std::sin(Rx)*std::cos(Ry);

    frame(0, 2) = std::cos(Rx)*std::sin(Ry)*std::cos(Rz) + std::sin(Rx)*std::sin(Rz);
    frame(1, 2) = std::cos(Rx)*std::sin(Ry)*std::sin(Rz) - std::sin(Rx)*std::cos(Rz);
    frame(2, 2) = std::cos(Rx)*std::cos(Ry);

    frame(0, 3) = x;
    frame(1, 3) = y;
    frame(2, 3) = z;

    return frame;
}




Eigen::Quaterniond frameToQuaternion(const Eigen::Matrix4d frame) {
    Eigen::AngleAxisd aa(frame.block<3, 3>(0, 0));
    Eigen::Quaterniond quater(aa);

    return quater;
}



Eigen::Matrix4d quaternionToFrame(Eigen::Quaterniond quater, const double x, const double y, const double z) {
    Eigen::Matrix4d frame;
    frame << 0, 0, 0, 0,
             0, 0, 0, 0,
             0, 0, 0, 0,
             0, 0, 0, 1;

    double q0 = quater.w();
    double q1 = quater.x();
    double q2 = quater.y();
    double q3 = quater.z();

    frame(0, 0) = pow(q0, 2) + pow(q1, 2) - pow(q2, 2) - pow(q3, 2);
    frame(1, 0) = 2*q1*q2 + 2*q0*q3;
    frame(2, 0) = 2*q1*q3 - 2*q0*q2;

    frame(0, 1) = 2*q1*q2 - 2*q0*q3;
    frame(1, 1) = pow(q0, 2) - pow(q1, 2) + pow(q2, 2) - pow(q3, 2);
    frame(2, 1) = 2*q2*q3 + 2*q0*q1;

    frame(0, 2) = 2*q1*q3 + 2*q0*q2;
    frame(1, 2) = 2*q2*q3 - 2*q0*q1;
    frame(2, 2) = pow(q0, 2) - pow(q1, 2) - pow(q2, 2) + pow(q3, 2);

    frame(0, 3) = x;
    frame(1, 3) = y;
    frame(2, 3) = z;

    return frame;
}

#endif
