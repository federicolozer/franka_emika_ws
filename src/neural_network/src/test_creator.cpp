#include "cast_tools.hpp"
#include "kinematics.hpp"
#include "utils.hpp"
#include "progressbar.hpp"
#include <eigen3/Eigen/Dense>
#include <array>
#include <cmath>
#include <fstream>
#include <Python.h>
#include <ros/package.h>

int skip = 4;
boost::array<double, 7> q_actual_array = {{0, -0.785398163397, 0, -2.3561944899, 0, 1.57079632679, 0.785398163397}};
std::string yaml_path = ros::package::getPath("path_planning") + "/config/mode.yaml";


bool IK_check(Eigen::Map< Eigen::Matrix4d > O_T_EE, double q7, int mode) {
    Eigen::Matrix4d O_T_EE_tmp = baseCoordTransf(O_T_EE, mode);
    Eigen::Map<Eigen::Matrix4d> O_T_EE_new(O_T_EE_tmp.data());

    boost::array<boost::array<double, 7>, 4> q_array_list = IK_solver(O_T_EE_new, q7, q_actual_array, false);

    bool result = false;
    bool valid;
    for (int i=0; i<4; i++) {
        valid = true;
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

    return result;
}



int createTest(PyObject* pModule, PyObject* pHumanPoses, Eigen::Matrix4d frame, std::ofstream* file1, std::ofstream* file2, std::ofstream* file3) {
    progressbar bar(PyList_Size(pHumanPoses));
    bar.set_niter(PyList_Size(pHumanPoses));
    bar.reset();
    bar.set_done_char("█");

    // Read mode from yaml
    std::ifstream yaml;

    yaml.open(yaml_path);
    std::string param;
    yaml >> param >> param;

    int mode;
    if (param == "vert") {
        mode = 0;
    }
    else if (param == "horz") {
        mode = 1;
    }
    else if (param == "ceil") {
        mode = 2;
    }           

    double t0;
    int doOnce = 1;
    int cnt = 0;
    double grip_sum = 0;
    std::vector<std::array<double, 2>> grip_wid_array;
    for (Py_ssize_t i=0; i<PyList_Size(pHumanPoses); i+=skip) {
        frame = Eigen::Matrix4d::Identity();

        PyObject* pPose = PyList_GetItem(pHumanPoses, i);

        PyObject* pTuple = PyTuple_New(1);
        PyTuple_SetItem(pTuple, 0, pPose);

        for (int j=0; j<skip; j++) {
            bar.update();
        }
        
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
            double t = PyFloat_AsDouble(PyList_GetItem(pList, 5));

            if (doOnce) {
                t0 = t;
                doOnce--;
            }

            double grip_wid = PyFloat_AsDouble(PyList_GetItem(pList, 6));
            grip_wid_array.push_back({grip_wid, t-t0});
            grip_sum += grip_wid;
            if (!IK_check(O_T_EE, q7, mode)) {
                cnt++;
                continue;
            }

            // Write line in dataset file
            Eigen::Quaterniond quater = frameToQuaternion(frame);
            *file1 << quater.x() << "," << quater.y() << "," << quater.z() << "," << quater.w() << "," << frame(0,3) << "," << frame(1,3) << "," << frame(2,3) << "," << q7 << std::endl;
            *file2 << "\n\t\t{\n\t\t\t\"t\": " << t-t0 << ",\n\t\t\t\"Qx\": " << quater.x() << ",\n\t\t\t\"Qy\": " << quater.y() << ",\n\t\t\t\"Qz\": " << quater.z() << ",\n\t\t\t\"Qw\": " << quater.w() << ",\n\t\t\t\"x\": " << frame(0,3) << ",\n\t\t\t\"y\": " << frame(1,3) << ",\n\t\t\t\"z\": " << frame(2,3) << "\n\t\t},";
        }
    }

    // Write gripper file
    double mean = grip_sum/grip_wid_array.size();

    //auto minmax = std::minmax_element(grip_wid_array.begin(), grip_wid_array.end());
    //double mean = ((*minmax.first)[0]+(*minmax.second)[0])/2;

    int grip_status = 1;
    for (auto pnt=grip_wid_array.begin(); pnt<grip_wid_array.end(); pnt++) {
        if (grip_status == 1 && (*pnt)[0] < mean) {
            *file3 << "\n\t\t{\n\t\t\t\"t\": " << (*pnt)[1] << ",\n\t\t\t\"action\": \"close\"\n\t\t},";
            grip_status = 0;
        }
        else if (grip_status == 0 && (*pnt)[0] > mean) {
            *file3 << "\n\t\t{\n\t\t\t\"t\": " << (*pnt)[1] << ",\n\t\t\t\"action\": \"open\"\n\t\t},";
            grip_status = 1;
        }
    }

    std::cout << std::endl << "Discarded data due to IK inconsistency: " << cnt*100/PyList_Size(pHumanPoses) << "%" << std::endl;
}



int execPython(PyObject* pModule, Eigen::Matrix4d frame, std::ofstream* file1, std::ofstream* file2, std::ofstream* file3, std::string tracking_data) {
    PyObject* pFuncReader = PyObject_GetAttrString(pModule, "reader");
    if(pFuncReader && PyCallable_Check(pFuncReader)) {
        PyObject* pTuple = PyTuple_New(1);
        PyObject* pList = PyList_New(0);
        PyList_Append(pList, PyUnicode_FromString(tracking_data.c_str()));

        PyTuple_SetItem(pTuple, 0, pList);

        PyObject* pHumanPoses = PyObject_CallObject(pFuncReader, pTuple);
        createTest(pModule, pHumanPoses, frame, file1, file2, file3);
    }
}




int main(int argc, char** argv) {
    std::ofstream file1;
    std::ofstream file2;
    std::ofstream file3;

    Py_Initialize();
    
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('/home/lozer/franka_emika_ws/src/neural_network/scripts')");
    PyObject* pModule = PyImport_ImportModule("human_poses_test");

    Eigen::Matrix4d frame;

    if (pModule) {
        if (argc = 2) {
            std::string tracking_data = argv[1];
            file1.open("/home/lozer/franka_emika_ws/src/neural_network/data/dataset/"+tracking_data.substr(5,tracking_data.length()-9)+".csv");
            file1 << "Qx, Qy, Qz, Qw, x, y, z, q7" << std::endl;
            file2.open("/home/lozer/franka_emika_ws/src/path_planning/data/trajectory/"+tracking_data.substr(5,tracking_data.length()-9)+"/arm.json");
            file2 << "{\n\t\"waypoints\":[" << std::endl;
            file3.open("/home/lozer/franka_emika_ws/src/path_planning/data/trajectory/"+tracking_data.substr(5,tracking_data.length()-9)+"/gripper.json");
            file3 << "{\n\t\"waypoints\":[\n\t\t{\n\t\t\t\"t\": 0,\n\t\t\t\"action\": \"open\"\n\t\t},";

            execPython(pModule, frame, &file1, &file2, &file3, tracking_data);
        }
        else if (argc > 2) {
            std::cout << "Error: only one argument required" << std::endl;
        }
        else {
            std::cout << "Error: missing argument" << std::endl;
        }
    }
    else {
        std::cout << "Error: failed loading python module 'human_poses_test'" << std::endl;
    }
	
	Py_Finalize();

    int pos2 = file2.tellp();
    file2.seekp(pos2 - 1);
    file2 << "\n\t]\n}" << std::endl;
    int pos3 = file3.tellp();
    file3.seekp(pos3 - 1);
    file3 << "\n\t]\n}" << std::endl;

    file1.close();
    file2.close();
    file3.close();

    return 0;
}
