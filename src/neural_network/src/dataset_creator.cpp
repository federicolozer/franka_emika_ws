#include "cast_tools.hpp"
#include <eigen3/Eigen/Dense>
#include <array>
#include <cmath>
#include <iostream>
#include <fstream>
#include <Python.h>



int main(int argc, char** argv) {
    std::ofstream file;

    std::cout << "-----------------" << std::endl;

    file.open("/home/lozer/franka_emika_ws/src/neural_network/data/dataset/humanPoses.csv");
    file << "Qx, Qy, Qz, Qw, x, y, z, q7" << std::endl;

	Py_Initialize(); 

    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('/home/lozer/franka_emika_ws/src/neural_network/scripts')");
    PyObject* pName = PyUnicode_FromString("humanPoses_solver");
    std::cout << "pname = " << pName << std::endl;
	PyObject* pModule = PyImport_Import(pName);


    
    Eigen::Matrix4d frame;
    std::cout << "pmodule = " << pModule << std::endl;

    if (pModule) {
        std::cout << "pmodule ok" << std::endl;
        PyObject* pFuncReader = PyObject_GetAttrString(pModule, "reader");
        std::cout << "reader object" << std::endl;
        if(pFuncReader && PyCallable_Check(pFuncReader)) {
            std::cout << "launching reader" << std::endl;
            PyObject* pHumanPoses = PyObject_CallObject(pFuncReader, NULL);
            std::cout << "reader executed" << std::endl;
            for (Py_ssize_t i=0; i<PyList_Size(pHumanPoses); i++) {
                frame = Eigen::Matrix4d::Identity();
                std::cout << "frame = " << frame << std::endl;

                PyObject* pPose = PyList_GetItem(pHumanPoses, i);
                PyObject* pTuple = PyTuple_New(1);
                PyTuple_SetItem(pTuple, 0, pPose);

                PyObject* pFuncCheck = PyObject_GetAttrString(pModule, "check");
                PyObject* pResult = PyObject_CallObject(pFuncCheck, pTuple);
                bool result = PyObject_IsTrue(pResult);

                if (result == false) {
                    continue;
                }

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
                    PyObject* pq7 = PyList_GetItem(pList, 4);
                    double q7 = PyFloat_AsDouble(pq7) - M_PI_2;

                    std::cout << "q7 = " << q7 << std::endl;

                    std::cout << "frame = " << std::endl << frame << std::endl;

                    Eigen::Quaterniond quater = frameToQuaternion(frame);

                    std::cout << "quaternion = " << quater.x() << " " << quater.y() << " " << quater.z() << " " << quater.w()  << std::endl;

                    file << quater.x() << "," << quater.y() << "," << quater.z() << "," << quater.w() << "," << frame(0,3) << "," << frame(1,3) << "," << frame(2,3) << "," << q7 << std::endl;
                }
            }
        }
    }
	
	Py_Finalize();

    file.close();

    return 0;
}
