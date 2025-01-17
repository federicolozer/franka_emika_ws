#include <eigen3/Eigen/Dense>
#include <array>
#include <cmath>
#include <iostream>
#include <fstream>
#include <Python.h>
#include "tools.hpp"



int main() {
    std::ofstream file;

    //file.open("/home/lozer/franka_emika_ws/src/neural_network/data/dataset/humanPoses.csv");
    //file << "x, y, z, Q0, Q1, Q2, Q3, q7" << std::endl;
    //file.close();

    PyObject* pInt;

	Py_Initialize(); 

    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('/home/lozer/franka_emika_ws/src/neural_network/scripts')");
	PyObject* pName = PyUnicode_FromString("humanPoses_solver");
	PyObject* pModule = PyImport_Import(pName);

    Eigen::Matrix4d frame;

    if (pModule) {
        PyObject* pFuncReader = PyObject_GetAttrString(pModule, "reader");
        if(pFuncReader && PyCallable_Check(pFuncReader)) {
            PyObject* pHumanPoses = PyObject_CallObject(pFuncReader, NULL);

            for (Py_ssize_t i=0; i<PyList_Size(pHumanPoses); i++) {
                frame.setZero();

                PyObject* pPose = PyList_GetItem(pHumanPoses, i);
                PyObject* pTuple = PyTuple_New(1);
                PyTuple_SetItem(pTuple, 0, pPose);

                PyObject* pFuncSolver = PyObject_GetAttrString(pModule, "solver");
                if(pFuncSolver && PyCallable_Check(pFuncSolver)) {
                    PyObject* pList = PyObject_CallObject(pFuncSolver, pTuple);

                    for (int j=0; j<4; j++) {
                        PyObject* pAxis = PyList_GetItem(pList, j);
                        std::array<double, 3> axis;

                        for (int k=0; k<3; k++) {
                            axis[k] = PyFloat_AsDouble(PyList_GetItem(pAxis, k));
                        }

                        frame.block<3,1>(0,i) << axis[0], axis[1], axis[2];
                    }
                    PyObject* pq7 = PyList_GetItem(pList, 4);
                    double q7 = PyFloat_AsDouble(pq7);

                    std::cout << "q7 = " << q7 << std::endl;

                    std::cout << "frame = " << frame << std::endl;
                    
                }
            }
        }
    }
        

    //PyRun_SimpleString("import sys");
    //PyRun_SimpleString("sys.path.append('/home/lozer/franka_emika_ws/src/neural_network/scripts')");
    //PyRun_SimpleString("import humanPoses_solver");
    //PyRun_SimpleString("humanPoses_solver.reader()");
	
	Py_Finalize();

    return 0;
}
