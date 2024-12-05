#pragma once

#ifndef IK_solver
#define IK_solver

#define _USE_MATH_DEFINES

#include "ros/ros.h"
#include <array>
#include <eigen3/Eigen/Dense>



void error();

void error(int n, double val);

boost::array<double, 7> franka_IK(Eigen::Map< Eigen::Matrix<double, 4, 4> > O_T_EE, double q7, boost::array<double, 7> q_actual_array);

#endif
