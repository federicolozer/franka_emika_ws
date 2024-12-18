#pragma once

#ifndef UTILS
#define UTILS

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

Eigen::Matrix4d eulerToFrame(const float Rx, const float Ry, const float Rz, const float x, const float y, const float z) {
    Eigen::Matrix4d frame;
    frame << 0, 0, 0, 0,
             0, 0, 0, 0,
             0, 0, 0, 0,
             0, 0, 0, 1;

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

#endif
