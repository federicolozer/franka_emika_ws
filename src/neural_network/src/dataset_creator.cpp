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

    PyObject* pInt;

	Py_Initialize(); 

	PyObject* pName = PyUnicode_FromString("humanPoses_solver");
	PyObject* pModule = PyImport_Import(pName);
    PyObject* pFunc = PyObject_GetAttrString(pModule, "reader");

       

    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('/home/lozer/franka_emika_ws/src/neural_network/scripts')");
    PyRun_SimpleString("import humanPoses_solver");
    PyRun_SimpleString("humanPoses_solver.reader()");
	
	Py_Finalize();

	std::cout << "Hello World from C++!!!" << std::endl;

    return 0;
}
