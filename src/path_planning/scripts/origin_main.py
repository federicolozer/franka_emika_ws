#!/usr/bin/env python3
# coding=utf-8

import sys
sys.path.append('/home/lozer/franka_emika_ws/src/neural_network/scripts')

import rospy
import NN_engine as nn
from copy import deepcopy
import numpy as np
from math import pi, nan
import controller
import json
import time
import socket
import yaml
import rospkg
import os

dispFrame = False
ttype = "follow_joint"
traj = "pick_and_place_1"
t_arm = []
q_arm = []
t_gripper = []
q_gripper = []
q_actual_array = np.array([0, -0.785398163397, 0, -2.3561944899, 0, 1.57079632679, 0.785398163397])
yaml_path = rospkg.RosPack().get_path("path_planning") + "/config/mode.yaml"



def IK_fromQuater_client(data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))

    client_socket.send(b"1")

    request = np.array(data, dtype=np.double).tobytes()
    client_socket.send(request)

    response = []
    for i in range(4):
        res = np.frombuffer(client_socket.recv(56), dtype=np.double)
        if np.isnan(res).any() == False:
            response.append(res)
    
    client_socket.close()

    return response



def controller_client(data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8081))

    client_socket.send(b"1")

    request = np.array(data[0], dtype=np.double).tobytes()
    client_socket.send(request)

    #request = np.array(data[1], dtype=np.double).tobytes()
    #client_socket.send(request)
#
    #request = data[2]
    #client_socket.send(request)
    
    client_socket.close()



def endTransmission(port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', port))

    client_socket.send(b"0")

    client_socket.close()



def optMove(q_array_list, q_actual_array):
    err = nan
    
    if not q_array_list == []:
        for array in q_array_list:
            n_err = np.dot((array-q_actual_array), (array-q_actual_array))

            if n_err-err < 0 or np.isnan(n_err-err):
                q_array = list(array)
                err = n_err
    else:
        q_array = []

    return q_array



def sel_mode():
    with open(yaml_path, 'r') as file:
        param = yaml.safe_load(file)["mode"]
        if param == "vert":
            mode = 0
        elif param == "horz":
            mode = 1
        elif param == "ceil":
            mode = 2    

    return mode

    


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "--close":
            endTransmission(8080)
            #endTransmission(8081)
        else:
            raise ValueError("wrong argument")
        quit()

    rospy.init_node("main")

    mode = sel_mode()

    model = nn.createModel()

    try:
        with open(f'/home/lozer/franka_emika_ws/src/path_planning/data/trajectory/{traj}/gripper.json', "r") as file:
            trajectory = json.load(file)

            for waypoint in trajectory["waypoints"]:
                if waypoint["action"] == "close":
                    q_array = 0
                elif waypoint["action"] == "open":
                    q_array = 1
                t_gripper.append(waypoint["t"]*3)
                q_gripper.append(q_array)
            
        with open(f'/home/lozer/franka_emika_ws/src/path_planning/data/trajectory/{traj}/arm.json', "r") as file:
            trajectory = json.load(file)

            cnt = 0
            for waypoint in trajectory["waypoints"]:
                quater = np.array([float(waypoint["Qx"]), float(waypoint["Qy"]), float(waypoint["Qz"]), float(waypoint["Qw"])])
                O_EE = np.array([float(waypoint["x"]), float(waypoint["y"]), float(waypoint["z"])])

                # Neural network ---------------------------------------------------------------------

                print("\n===============================================================")
                print("\tNeural network")
                print("===============================================================")
                t0 = time.time()
                inputData = np.matrix(np.concatenate((quater, O_EE), axis=0))
                q7 = float(nn.neuralNetwork(model, inputData)[0]) 
                t1 = time.time()
                print(f"Elapsed time for having a solution from NN: {(t1-t0):>4f} s")
                print("Found solution:")
                print(q7)
                print("---------------------------------------------------------------")

                # Inverse kinematics -----------------------------------------------------------------

                print("\n===============================================================")
                print("\tInverse kinematics")
                print("===============================================================")
                t0 = time.time()
                data = [float(inputData[0, 0]), float(inputData[0, 1]), float(inputData[0, 2]), float(inputData[0, 3]), float(inputData[0, 4]), float(inputData[0, 5]), float(inputData[0, 6]), q7, float(mode), float(dispFrame)]
                response = IK_fromQuater_client(data)
                t1 = time.time()
                print(f"Elapsed time for having a solution from IK client: {(t1-t0):>4f} s")
                print("Found solution:")
                print(response)
                print("---------------------------------------------------------------")

                q_array = optMove(response, q_actual_array)

                if not len(q_array) == 0:
                    t_arm.append(waypoint["t"]*3)
                    q_arm.append(q_array)
                    q_actual_array = q_array
                    print("\nq_array = ", q_array)
                    cnt += 1
                else:
                    #t.append(None)     iot ce fa di chescj
                    #q.append(None)
                    print("\nNo response found")

            # Trajectory planning ----------------------------------------------------------------

            print("\n===============================================================")
            print("\tTrajectory planning")
            print("===============================================================")

            print(f"Solutions found: {cnt}/{len(trajectory['waypoints'])}")

            #controller_client((t, q, ttype))
            while True:
                input("Go")
                controller.launch_trajectory(t_arm, q_arm, t_gripper, q_gripper, ttype)

    except:
        raise ValueError("selected trajectory does not exist")