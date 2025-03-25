#!/usr/bin/env python3
# coding=utf-8

import sys
sys.path.append('/home/lozer/franka_emika_ws/src/neural_network/scripts')

import NN_engine as nn
import rospy
from copy import deepcopy
import numpy as np
from math import pi, nan
import control_tools as controller
import json
import time
import socket



def IK_fromQuater_client(data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))

    client_socket.send(b"1")

    data = np.array(data, dtype=np.double)
    print("data = ", data)
    request = data.tobytes()
    
    client_socket.send(request)

    response = []
    for i in range(4):
        res = np.frombuffer(client_socket.recv(56), dtype=np.double)
        print(f"--- res{i} = ", res)
        if np.isnan(res).any() == False:
            response.append(res)
    print("Response = ", response)
    client_socket.close()

    return response



def endTransmission():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))

    client_socket.send(b"0")

    client_socket.close()



def optMove(q_array_list, q_ref):
    err = nan

    print(q_array_list)
    
    if not q_array_list == []:
        for array in q_array_list:
            n_err = np.dot((array-q_ref), (array-q_ref))

            if n_err-err < 0 or np.isnan(n_err-err):
                q_array = list(array)
                err = n_err
    else:
        q_array = []

    return q_array



def sel_mode():
    if not rospy.search_param('/mode') == None:
        param = rospy.get_param('/mode')
        if param == "vert":
            mode = 0
        elif param == "horz":
            mode = 1
        elif param == "ceil":
            mode = 2    

    return mode

    


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "--cls":
            endTransmission()
        else:
            raise ValueError("wrong argument")
        quit()

    rospy.init_node('controller')

    mode = sel_mode()
    ttype = "follow_joint"
    dispFrame = False
    q_ref = np.array(controller.readJointStates())

    model = nn.createModel()

    t = []
    q = []

    with open('/home/lozer/franka_emika_ws/src/path_planning/data/trajectory/waypoints.json', "r") as file:
        trajectory = json.load(file)

        for waypoint in trajectory["waypoints"]:
            if waypoint["type"] == "EE_pose":
                quater = np.array([float(waypoint["Qx"]), float(waypoint["Qy"]), float(waypoint["Qz"]), float(waypoint["Qw"])])
                O_EE = np.array([float(waypoint["x"]), float(waypoint["y"]), float(waypoint["z"])])

                print(quater)
                print(O_EE)

                # Neural network ---------------------------------------------------------------------

                t0 = time.time()
                inputData = np.matrix(np.concatenate((quater, O_EE), axis=0))
                q7 = float(nn.neuralNetwork(model, inputData)[0]) 
                print("\n----------------")
                t1 = time.time()
                print("Elapsed time for having a solution from NN: ", t1-t0, "s")
                print("----------------")

                # Inverse kinematics -----------------------------------------------------------------


                print("q7 = ", q7)
                print("expected q7 = ", -0.238573)

                #q7 = -0.238573




                t0 = time.time()
                data = [float(inputData[0, 0]), float(inputData[0, 1]), float(inputData[0, 2]), float(inputData[0, 3]), float(inputData[0, 4]), float(inputData[0, 5]), float(inputData[0, 6]), q7, float(mode), float(dispFrame)]
                response = IK_fromQuater_client(data)
                print("\n----------------")
                t1 = time.time()
                print("Elapsed time for IK client: ", t1-t0, "s")
                print("----------------")

                # Trajectory planning ----------------------------------------------------------------

                q_array = optMove(response, q_ref)
                print("q_array = ", q_array)

                if not len(q_array) == 0:
                    t.append(waypoint["t"])
                    q.append(q_array)
                    q_ref = q_array
                else:
                    t.append(None)
                    q.append(None)
                    print("No response found")

            else:
                if waypoint["type"] == "close_gripper":
                    q_array = [0]
                    q_array.append(waypoint["width"])
                elif waypoint["type"] == "open_gripper":
                    q_array = [1]
                    q_array.append(waypoint["width"])
                q.append(q_array)

    print("t = ", t)
    print("q = ", q)

    controller.launch_trajectory(t, q, ttype)

    time.sleep(5)