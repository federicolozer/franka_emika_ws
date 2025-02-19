#!/usr/bin/env python3
# coding=utf-8

#import sys
#sys.path.append('/home/lozer/franka_emika_ws/src/neural_network/scripts')
#import NN_engine as nn
import rospy
from copy import deepcopy
import numpy as np
from math import pi
import control_tools as controller
import csv
import time
import socket
import struct



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

    """res1 = np.frombuffer(client_socket.recv(56), dtype=np.double)
    res2 = np.frombuffer(client_socket.recv(56), dtype=np.double)
    res3 = np.frombuffer(client_socket.recv(56), dtype=np.double)
    res4 = np.frombuffer(client_socket.recv(56), dtype=np.double)

    print("--- res1 = ", res1)
    print("--- res2 = ", res2)
    print("--- res3 = ", res3)
    print("--- res4 = ", res4)

    response = []

    if np.isnan(res1).any() == False:
        response.append(res1)
    elif np.isnan(res2).any() == False:
        response.append(res2)
    elif np.isnan(res3).any() == False:
        response.append(res3)
    elif np.isnan(res4).any() == False:
        response.append(res4)"""
        
    client_socket.close()

    return response



def endTransmission():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))

    client_socket.send(b"0")

    client_socket.close()



def optMove(q_array_list):
    q_array = list(q_array_list[0])
    do_once = True
    for array in q_array_list:
        if do_once:
            do_once = False
            continue
        
        if array[0] < q_array[0]:
            q_array = list(array)
    
    return q_array

    



if __name__ == '__main__':    
    rospy.init_node('controller')
    mode = 0
    if not rospy.search_param('/mode') == None:
        param = rospy.get_param('/mode')
        if param == "horz":
            mode = 1
        elif param == "horz_rev":
            mode = 2
        elif param == "ceil":
            mode = 3

    ttype = "follow_joint"

    while True:
        with open('/home/lozer/franka_emika_ws/src/neural_network/data/dataset/humanPoses.csv') as file:
            reader = csv.reader(file)

            rw = input("Select row...\n")
            if rw == "quit":
                endTransmission()
                break

            row = list(reader)[int(rw)]

            t = []
            q = []

            #quater = np.array([float(row[0]), float(row[1]), float(row[2]), float(row[3])])
            #O_EE = np.array([float(row[4]), float(row[5]), float(row[6])])
    #
            #t_1 = time.time()
            #
            #model = nn.NN()
            #t0 = time.time()
            #print("time elapsed for initialize NN: ", t0-t_1, "s")
    #
            #inputData = np.matrix(np.concatenate((quater, O_EE), axis=0))
            #q7_tmp = nn.neural_network(model, inputData)
    #
            #print("\n----------------")
            #t1 = time.time()
            #print("time elapsed for having a solution: ", t1-t0, "s")
        #

            t2 = time.time()

            #res = controller.IK_fromQuater_client(quater, O_EE, q7, q_actual_array, horz)

            data = [float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), pi/4-float(row[7]), float(mode)]
            response = IK_fromQuater_client(data)

            print("\n----------------")
            t3 = time.time()
            print("time elapsed for IK: ", t3-t2, "s")
            print("\n----------------")

            if response == []:
                print("No response found")
                quit()

            q_array =  optMove(response)
            print("q_array = ", q_array)
            q_curr = controller.readJointStates()
            print("q_curr = ", q_curr)
            if not len(q_array) == 0:
                t.append(2)
                q.append(q_array)

                controller.launch_trajectory(t, q, ttype)

                time.sleep(5)

        
    
    

    







    
    


            


