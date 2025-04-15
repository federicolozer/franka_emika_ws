#!/usr/bin/env python3
# coding=utf-8

import sys
sys.path.append('/home/lozer/franka_emika_ws/src/neural_network/scripts')
sys.path.append('/home/lozer/franka_emika_ws/src/user_interface/scripts')

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
import csv
from scipy.signal import savgol_filter

dispFrame = False
ttype = "follow_joint"
t_arm = []
q_arm = []
t_gripper = []
q_gripper = []
inputData_array = []
q7_array = []
q_actual_array = np.array([0, -0.785398163397, 0, -2.3561944899, 0, 1.57079632679, 0.785398163397])
yaml_path = rospkg.RosPack().get_path("path_planning") + "/config/mode.yaml"

rospy.init_node("main")
model = nn.createModel()




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



def UI_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client_socket.sendto(b"1", ('localhost', 8081))

    client_socket.connect(('localhost', 8081))

    client_socket.send(b"1")

    client_socket.close()



def UI_server():
    global server_socket, new_socket

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.settimeout(None)
    server_socket.bind(('localhost', 8082))

    server_socket.listen(5)

    new_socket, addr = server_socket.accept()

    msg = new_socket.recv(1024)

    new_socket.close()
    server_socket.close()

    return msg.decode()



def endTransmission(port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', port))

    client_socket.send(b"0")

    client_socket.close()



def optMove(q_array_list, q_actual_array):
    err = nan
    
    if not q_array_list == []:
        for array in q_array_list:
            n_err = np.dot((array[2]-q_actual_array[2]), (array[2]-q_actual_array[2]))

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


 
def main(traj):
    mode = sel_mode()
    t_arm = []
    q_arm = []
    t_gripper = []
    q_gripper = []
    inputData_array = []
    q7_array = []
    q7_real_array = []
    q_actual_array = controller.readJointStates()
    
    try:
        with open(f'/home/lozer/franka_emika_ws/src/neural_network/data/dataset/{traj}.csv') as file:
            doOnce = True
            for line in csv.reader(file):
                if doOnce:
                    doOnce = False
                    continue

                q7_real_array.append(float(line[7]))
    except:
        print("Selected trajectory does not exist..")
        
    with open(f'/home/lozer/franka_emika_ws/src/path_planning/data/trajectory/{traj}/gripper.json', "r") as file:
        trajectory = json.load(file)

        for waypoint in trajectory["waypoints"]:
            if waypoint["action"] == "close":
                q_array = 0
            elif waypoint["action"] == "open":
                q_array = 1
            t_gripper.append(waypoint["t"]*4)
            q_gripper.append(q_array)
    
    with open(f'/home/lozer/franka_emika_ws/src/path_planning/data/trajectory/{traj}/arm.json', "r") as file:
        trajectory = json.load(file)

        t_array = []

        # Neural network ---------------------------------------------------------------------

        print("\n===============================================================")
        print("\tNeural network")
        print("===============================================================")
        t0 = time.time()
        for waypoint in trajectory["waypoints"]:
            quater = np.array([float(waypoint["Qx"]), float(waypoint["Qy"]), float(waypoint["Qz"]), float(waypoint["Qw"])])
            O_EE = np.array([float(waypoint["x"]), float(waypoint["y"]), float(waypoint["z"])])

            inputData = np.matrix(np.concatenate((quater, O_EE), axis=0))
            q7 = float(nn.neuralNetwork(model, inputData)[0]) 

            inputData_array.append(deepcopy(inputData))
            q7_array.append(deepcopy(q7))

            t_array.append(waypoint["t"])

        tn = time.time()
        print(f"Elapsed time for having a solution from NN: {(tn-t0):>4f} s")
        print("---------------------------------------------------------------")

        # Savitzky-Golay filter -----------------------------------------------------------------

        q7_array = savgol_filter(q7_array, window_length=int(0.15*len(q7_array)), polyorder=3)

        # Inverse kinematics -----------------------------------------------------------------

        print("\n===============================================================")
        print("\tInverse kinematics")
        print("===============================================================")
        t0 = time.time()
        cnt = 0
        for i in range(len(inputData_array)):
            inputData = inputData_array[i]
            q7 = q7_array[i]
            
            data = [float(inputData[0, 0]), float(inputData[0, 1]), float(inputData[0, 2]), float(inputData[0, 3]), float(inputData[0, 4]), float(inputData[0, 5]), float(inputData[0, 6]), q7, float(mode), float(dispFrame)]
            response = IK_fromQuater_client(data)

            q_array = optMove(response, q_actual_array)

            if not len(q_array) == 0:
                t_arm.append(t_array[i]*4)
                q_arm.append(q_array)
                q_actual_array = q_array
                cnt += 1
            else:
                pass
                #t.append(None)     iot ce fa di chescj
                #q.append(None)
        
        tn = time.time()
        print(f"Elapsed time for having a solution from IK client: {(tn-t0):>4f} s")
        print("---------------------------------------------------------------")

        # Test evaluation ----------------------------------------------------------------

        diff = 0
        for i in range(len(q7_array)):
            comp = (q7_array[i]-q7_real_array[i])**2
            diff += comp

        diff /= len(q7_array)
        rmse = np.sqrt(diff)

        print(f"RMSE: {(rmse):>0.4f}rad - {(rmse/(2*2.8973)*100):>0.1f}%")

        # Trajectory planning ----------------------------------------------------------------

        print("\n===============================================================")
        print("\tTrajectory planning")
        print("===============================================================")

        print(f"Solutions found: {cnt}/{len(trajectory['waypoints'])}")

        #controller_client((t_arm, q_arm, t_gripper, q_gripper, ttype))
        controller.launch_trajectory(t_arm, q_arm, t_gripper, q_gripper, ttype)
    
    return 1








if __name__ == '__main__':
    while True:
        print("\n===============================================================")
        traj = input("Type the trajectory to perform or quit to exit:\n")

        if traj == "quit":
            #endTransmission(8080)
            break

        main(traj)
