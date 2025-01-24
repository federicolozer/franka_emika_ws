#!/usr/bin/env python3
# coding=utf-8

import rospy
from copy import deepcopy
import numpy as np
from math import pi
import control_tools as controller
import csv
import time





if __name__ == '__main__':
    rospy.init_node('controller')
    horz = rospy.get_param('/horz')

    ttype = "follow_joint"

    t = []
    q = []


    O_T_EE_array = np.array([1.0, 0.0, 0.0, 0.0, 
                            0.0, -1.0, 0.0, 0.0, 
                            0.0, 0.0, -1.0, 0.0, 
                            0.5, 0.0, 0.1, 1.0])
    q7 = pi/4 + 0.8
    q_actual_array = np.array([0, -0.785398163397, 0, -2.3561944899, 0, 1.57079632679, 0.785398163397])
    quater = np.array([1, 0, 0, 0])
    O_EE = np.array([0.5, 0.0, 0.2])

    #res = controller.IK_fromQuater_client(quater, O_EE, q7, q_actual_array, horz)

    res = controller.IK_fromFrame_client(O_T_EE_array, q7, q_actual_array, horz)

    q_array_list = [res.q_array_1, res.q_array_2, res.q_array_3, res.q_array_4]
    q_array = []

    for array in q_array_list:
        if not np.isnan(np.array([array])).any():
            q_array.append(array)
    
    print("q_array_list = ", q_array_list)
    print("q_array = ", q_array)

    t.append(2)
    q.append(list(q_array[0]))

    controller.launch_trajectory(t, q, ttype)


    

    







    
    


            


