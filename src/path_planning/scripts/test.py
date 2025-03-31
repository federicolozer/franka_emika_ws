#!/usr/bin/env python3
# coding=utf-8

import sys
sys.path.append('/home/lozer/franka_emika_ws/src/neural_network/scripts')

import NN_engine as nn
import rospy
from copy import deepcopy
import numpy as np
from math import pi, nan
import path_planning.scripts.controller as controller
import csv
import time
import socket



def IK_fromQuater_client(data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))

    client_socket.send(b"1")

    data = np.array(data, dtype=np.double)
    request = data.tobytes()
    
    client_socket.send(request)

    response = []
    for i in range(4):
        res = np.frombuffer(client_socket.recv(56), dtype=np.double)
        if np.isnan(res).any() == False:
            response.append(res)
    
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



    


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "--cls":
            endTransmission()
        else:
            raise ValueError("wrong argument")
        quit()


    mode = 2
    ttype = "follow_joint"
    dispFrame = False

    model = nn.createModel()


    while True:
        with open('/home/lozer/franka_emika_ws/src/neural_network/data/dataset/test.csv') as file:
            reader = csv.reader(file)

            rw = input("Select row...\n")
            if rw == "quit":
                endTransmission()
                break

            row = list(reader)[int(rw)]

            q7_real = float(row[7])

            t0 = time.time()
            quater =  np.array([float(row[0]), float(row[1]), float(row[2]), float(row[3])])
            O_EE =  np.array([float(row[4]), float(row[5]), float(row[6])])

            print(quater)
            print(O_EE)

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
            print("Expected solution:")
            print(q7_real)
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

  