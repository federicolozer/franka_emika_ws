#!/usr/bin/env python3
# coding=utf-8

import sys
sys.path.append('/home/lozer/franka_emika_ws/src/neural_network/scripts')
import NN_engine as nn
import rospy
from copy import deepcopy
import numpy as np
from math import pi
import control_tools as controller
import csv
import time





if __name__ == '__main__':
    rospy.init_node('controller')

    ttype = "follow_joint"

    q_actual_array = np.array([0, -0.785398163397, 0, -2.3561944899, 0, 1.57079632679, 0.785398163397])

    

    with open('/home/lozer/franka_emika_ws/src/neural_network/data/dataset/humanPoses.csv') as file:
        reader = csv.reader(file)

        row = list(reader)[3]

        t = []
        q = []

        quater = np.array([float(row[0]), float(row[1]), float(row[2]), float(row[3])])
        O_EE = np.array([float(row[4]), float(row[5]), float(row[6])])
        #q7 = float(row[7]) - pi/4

        print("---------------")
        print("quater = ", quater)
        print("O_EE = ", O_EE)

        inputData = np.matrix(np.concatenate((quater, O_EE), axis=0))
        q7_tmp = nn.neural_network(inputData)
        
        q7 = float(q7_tmp[0]) - pi/4
        print("q7 = ", q7)

        res = controller.IK_fromQuater_client(quater, O_EE, q7, q_actual_array)

        q_array_list = [res.q_array_1, res.q_array_2, res.q_array_3, res.q_array_4]
        q_array = []

        for array in q_array_list:
            if not np.isnan(np.array([array])).any():
                q_array.append(array)
        
        print("q_array_list = ", q_array_list)
        print("q_array = ", q_array)

        if len(q_array) >= 1:
            t.append(2)
            q.append(list(q_array[0]))

            controller.launch_trajectory(t, q, ttype)

            time.sleep(5)
    
    

    







    
    


            


