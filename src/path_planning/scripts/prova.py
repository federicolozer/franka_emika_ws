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



def optMove(q_array_list):
    q_curr = controller.readJointStates()
    print("actual configuration = ", q_curr)

    if not q_array_list == []:
        q_array = list(q_array_list[0])
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

    #msg = "rosrun dynamic_reconfigure dynparam set /gazebo \"{" + f"'gravity_x':{gravity[0]}, 'gravity_y':{gravity[1]}, 'gravity_z':{gravity[2]}" + "}\""
    #os.system(msg)

    ttype = "follow_joint"
    dispFrame = True

    while True:

        q7 = input("Select q7...\n")
        if q7 == "quit":
            endTransmission()
            break


        t = []
        q = []


        q7 = pi/4 - float(q7)
        print("q7 = ", q7)

        t0 = time.time()
        data = [1, 0, 0, 0, 0.4, 0, 0.2, q7, float(mode), True]
        response = IK_fromQuater_client(data)

        print("\n----------------")
        t1 = time.time()
        print("Elapsed time for IK client: ", t1-t0, "s")
        print("----------------")
#
        if response == []:
            print("No response found")
            continue

        q_array = optMove(response)
        print("q_array = ", q_array)
        
        if not len(q_array) == 0:
            t.append(2)
            q.append(q_array)

            controller.launch_trajectory(t, q, ttype)

            time.sleep(3)

        q_curr = controller.readJointStates()
        print("q_curr = ", q_curr)

    















        


