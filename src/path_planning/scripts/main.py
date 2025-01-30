#!/usr/bin/env python3
# coding=utf-8

#import sys
#sys.path.append('/home/lozer/franka_emika_ws/src/neural_network/scripts')
#import NN_engine as nn
import rospy
from copy import deepcopy
import numpy as np
from math import pi
#import control_tools as controller
import csv
import time
import socket
import struct

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def new_IK_fromQuater_client(data):

    print("data = ", data)
    data = np.array(data, dtype=np.float32)

    ba = data.tobytes()

    print("ba = ", ba)

    client_socket.connect(('localhost', 8085))
    client_socket.sendall(ba)
    response = np.frombuffer(client_socket.recv(1024), dtype=np.float32)
    print('Received from server:', response)


    client_socket.close()

    return response



if __name__ == '__main__':    
    rospy.init_node('controller')
    horz = rospy.get_param('/horz')

    ttype = "follow_joint"

    with open('/home/lozer/franka_emika_ws/src/neural_network/data/dataset/humanPoses.csv') as file:
        reader = csv.reader(file)

        row = list(reader)[2]

        t = []
        q = []

        quater = np.array([float(row[0]), float(row[1]), float(row[2]), float(row[3])])
        O_EE = np.array([float(row[4]), float(row[5]), float(row[6])])

        t_1 = time.time()
        
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
        
        #q7 = float(q7_tmp[0]) - pi/4
        #print("\nq7 = ", q7)
        q7 = pi/4

        t2 = time.time()

        #res = controller.IK_fromQuater_client(quater, O_EE, q7, q_actual_array, horz)

        data = [float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), q7, int(horz)]
        res = new_IK_fromQuater_client(data)

        print("\n----------------")
        t3 = time.time()
        print("time elapsed for IK: ", t3-t2, "s\n")

        print("res = ", np.frombuffer(res, dtype=np.float32))
        quit()


        q_array_list = [res.q_array_1, res.q_array_2, res.q_array_3, res.q_array_4]
        q_array = []

        for array in q_array_list:
            if not np.isnan(np.array([array])).any():
                q_array.append(array)

        if len(q_array) >= 1:
            t.append(2)
            q.append(list(q_array[0]))

            controller.launch_trajectory(t, q, ttype)

            time.sleep(5)
    
    

    







    
    


            


