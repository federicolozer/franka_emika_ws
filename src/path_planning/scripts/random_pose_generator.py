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
    print("data = ", data)
    request = data.tobytes()
    
    client_socket.send(request)

    response = []
    for i in range(4):
        res = np.frombuffer(client_socket.recv(56), dtype=np.double)
        print(f"--- res{i} = ", res)
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
    
    if not q_array_list == []:
        for array in q_array_list:
            n_err = np.dot((array-q_ref), (array-q_ref))

            if n_err-err < 0 or np.isnan(n_err-err):
                q_array = list(array)
                err = n_err
    else:
        q_array = []

    return q_array

    

def random_quaternion():
    # Generate four random numbers from a normal distribution
    rand = np.random.normal(size=4)
    # Normalize the quaternion
    norm = np.linalg.norm(rand)
    quaternion = rand / norm

    return quaternion



def random_position():
    x = 0.2 + np.random.random()*0.5
    y = -0.7 + np.random.random()*1.4
    z = 0.2 + np.random.random()*0.8

    position = [x, y, z]

    return position




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
    dispFrame = True
    q_ref = np.array(controller.readJointStates())

    model = nn.NN()

    while True:
        rw = input("Generate new random pose...\n")
        if rw == "quit":
            endTransmission()
            break

        t = []
        q = []

        quater = random_quaternion()
        O_EE = random_position()

        # Neural network
        # ------------------------------------------------------------------------------------

        t0 = time.time()
        inputData = np.matrix(np.concatenate((quater, O_EE), axis=0))
        q7 = float(nn.neural_network(model, inputData)[0]) 
        print("\n----------------")
        t1 = time.time()
        print("Elapsed time for having a solution from NN: ", t1-t0, "s")
        print("----------------")

        # Inverse kinematics
        # ------------------------------------------------------------------------------------

        t0 = time.time()
        print(inputData[0])
        print(inputData[0][0])
        print(inputData[0, 0])
        data = [float(inputData[0, 0]), float(inputData[0, 1]), float(inputData[0, 2]), float(inputData[0, 3]), float(inputData[0, 4]), float(inputData[0, 5]), float(inputData[0, 6]), pi/4-q7, float(mode), float(dispFrame)]
        response = IK_fromQuater_client(data)
        print("\n----------------")
        t1 = time.time()
        print("Elapsed time for IK client: ", t1-t0, "s")
        print("----------------")

        # Trajectory planning
        # ------------------------------------------------------------------------------------

        if response == []:
            print("No response found")
            continue

        q_array = optMove(response, q_ref)
        print("q_array = ", q_array)
        
        if not len(q_array) == 0:
            t.append(2)
            q.append(q_array)
            q_ref = q_array

            controller.launch_trajectory(t, q, ttype)

            time.sleep(5)

    















        


