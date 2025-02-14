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

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def IK_fromQuater_client(data):

    print("data = ", data)
    data = np.array(data, dtype=np.double)

    request = data.tobytes()

    client_socket.connect(('localhost', 8081))
    client_socket.sendall(request)
     
    response = np.frombuffer(client_socket.recv(1024), dtype=np.double)
    
    client_socket.close()

    return response



if __name__ == '__main__':    
    rospy.init_node('controller')
    horz = False
    if not rospy.search_param('/horz') == None:
        horz = rospy.get_param('/horz')

    ttype = "follow_joint"

    with open('/home/lozer/franka_emika_ws/src/neural_network/data/dataset/humanPoses.csv') as file:
        reader = csv.reader(file)

        row = list(reader)[200]

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
        print(row)

        t2 = time.time()

        #res = controller.IK_fromQuater_client(quater, O_EE, q7, q_actual_array, horz)

        data = [float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), pi/4-float(row[7]), int(horz)]
        response = IK_fromQuater_client(data)

        print("\n----------------")
        t3 = time.time()
        print("time elapsed for IK: ", t3-t2, "s\n")

        print("res = ", response)
        


        q_array = list(response)
        #q_array = [-1.7623606392141309, 1.0066890508374107, 0.9714105572606898, -1.9972501746915912, -0.5232118417432983, 2.2464632219400054, -0.40214716339744827]
        print("q_array = ", q_array)
        print("len q_array = ", len(q_array))

        if not len(q_array) == 0:
            t.append(2)
            q.append(q_array)

            controller.launch_trajectory(t, q, ttype)

            time.sleep(5)
    
    

    







    
    


            


