#!/usr/bin/env python3
# coding=utf-8

#import sys
#sys.path.append('/home/lozer/franka_emika_ws/src/neural_network/scripts')
#import NN_engine as nn
import rospy
from copy import deepcopy
import numpy as np
from math import pi, nan
import control_tools as controller
import csv
import time
import socket
import struct
#from gazebo_msgs.srv import SetPhysicsProperties, GetPhysicsProperties
#from geometry_msgs.msg import Vector3
#from std_srvs.srv import Empty
import os



def IK_fromQuater_client(data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))

    client_socket.send(b"1")

    data = np.array(data, dtype=np.double)
    #print("data = ", data)
    request = data.tobytes()
    
    client_socket.send(request)

    response = []
    for i in range(4):
        res = np.frombuffer(client_socket.recv(56), dtype=np.double)
        #print(f"--- res{i} = ", res)
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



def optMove(q_array_list, q_ref):
    err = nan
    
    if not q_array_list == []:
        for array in q_array_list:
            print("array = ", array)
            print("q_ref = ", q_ref)
            n_err = np.dot((array-q_ref), (array-q_ref))

            if n_err-err < 0 or np.isnan(n_err-err):
                q_array = list(array)
                err = n_err
    else:
        q_array = []

    return q_array

    



if __name__ == '__main__':    
    rospy.init_node('controller')

    mode = 0
    gravity = [0, 0, 0]
    if not rospy.search_param('/mode') == None:
        param = rospy.get_param('/mode')
        if param == "horz":
            mode = 1
            gravity[0] = -9.8
        elif param == "horz_rev":
            mode = 2
            gravity[0] = -9.8
        elif param == "ceil":
            mode = 3
            gravity[2] = 9.8
        else:
            gravity[2] = -9.8

    msg = "rosrun dynamic_reconfigure dynparam set /gazebo \"{" + f"'gravity_x':{gravity[0]}, 'gravity_y':{gravity[1]}, 'gravity_z':{gravity[2]}" + "}\""
    os.system(msg)

    ttype = "follow_joint"
    dispFrame = False

    t = []
    q = []

    qTime = -1

    q_ref = np.array(controller.readJointStates())
    print("q_ref = ", q_ref)

    for rw in range(100, len(list(csv.reader(open('/home/lozer/franka_emika_ws/src/neural_network/data/dataset/humanPoses.csv')))), 100):
        with open('/home/lozer/franka_emika_ws/src/neural_network/data/dataset/humanPoses.csv') as file:
            reader = csv.reader(file)

            row = list(reader)[int(rw)]

            t0 = time.time()

            data = [float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), pi/4-float(row[7]), float(mode), float(dispFrame)]
            response = IK_fromQuater_client(data)

            print("\n----------------")
            t1 = time.time()
            print("Elapsed time for IK client: ", t1-t0, "s")
            print("----------------")

            q_array = optMove(response, q_ref)
            
            print("q_array = ", q_array)

            qTime += 1

            if q_array == []:
                continue

            q_ref = q_array

            t.append(qTime)
            q.append(q_array)

    print("Starting task")
    controller.launch_trajectory(t, q, ttype)

    endTransmission()
        
    
    

    







    
    


            


