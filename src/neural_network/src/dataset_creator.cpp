#include "cast_tools.hpp"
//#include "kinematics.hpp"
#include <eigen3/Eigen/Dense>
#include <array>
#include <cmath>
#include <iostream>
#include <fstream>
#include <Python.h>


//boost::array<double, 7> q_actual_array = {{0, -0.785398163397, 0, -2.3561944899, 0, 1.57079632679, 0.785398163397}};



/*bool IK_check(Eigen::Map< Eigen::Matrix4d > O_T_EE, double q7) {
    boost::array<boost::array<double, 7>, 4> q_array_list = IK_solver(O_T_EE, q7, q_actual_array, false);

    bool result = false;
    for (int i=0; i<4; i++) {
        bool valid = true;
        for (int j=0; j<7; j++) {
            if (std::isnan(q_array_list[i][j])) {
                valid = false;
            }
        }
        if (valid) {
            result = true;
            break;
        }
    }

    return result
}*/




int main(int argc, char** argv) {
    std::ofstream file;

    std::cout << "-----------------" << std::endl;

    file.open("/home/lozer/franka_emika_ws/src/neural_network/data/dataset/humanPoses.csv");
    file << "Qx, Qy, Qz, Qw, x, y, z, q7" << std::endl;
    
	Py_Initialize();

    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('/home/lozer/franka_emika_ws/src/neural_network/scripts')");
    PyObject* pModule = PyImport_ImportModule("humanPoses_solver");

    Eigen::Matrix4d frame;

    if (pModule) {
        // Call reader function
        PyObject* pFuncReader = PyObject_GetAttrString(pModule, "reader");
        if(pFuncReader && PyCallable_Check(pFuncReader)) {
            PyObject* pHumanPoses = PyObject_CallObject(pFuncReader, NULL);
            for (Py_ssize_t i=0; i<PyList_Size(pHumanPoses); i++) {
                frame = Eigen::Matrix4d::Identity();

                PyObject* pPose = PyList_GetItem(pHumanPoses, i);

                PyObject* pTuple = PyTuple_New(1);
                PyTuple_SetItem(pTuple, 0, pPose);

                // Call solver function
                PyObject* pFuncSolver = PyObject_GetAttrString(pModule, "solver");
                if(pFuncSolver && PyCallable_Check(pFuncSolver)) {
                    PyObject* pList = PyObject_CallObject(pFuncSolver, pTuple);
                    
                    for (int j=0; j<4; j++) {
                        PyObject* pAxis = PyList_GetItem(pList, j);
                        std::array<double, 3> axis;

                        for (int k=0; k<3; k++) {
                            axis[k] = PyFloat_AsDouble(PyList_GetItem(pAxis, k));
                        }

                        frame.block<3,1>(0,j) << axis[0], axis[1], axis[2];
                    }
                    
                    // Check if inverse kinematics is feasible
                    Eigen::Map< Eigen::Matrix4d > O_T_EE(frame.data());
                    double q7 = PyFloat_AsDouble(PyList_GetItem(pList, 4));
                    //if (!IK_check(O_T_EE, q7)) {
                    //    continue;
                    //}

                    // Write line in dataset file
                    Eigen::Quaterniond quater = frameToQuaternion(frame);
                    file << quater.x() << "," << quater.y() << "," << quater.z() << "," << quater.w() << "," << frame(0,3) << "," << frame(1,3) << "," << frame(2,3) << "," << q7 << std::endl;
                }
            }
        }
    }
	
	Py_Finalize();

    file.close();

    return 0;
}
