#!/usr/bin/env python3
# coding=utf-8

import rospy
from copy import deepcopy
import numpy as np
from tqdm import tqdm
from math import pi
#from sensor_msgs.msg import JointState
#from control_msgs.msg import FollowJointTrajectoryActionGoal, FollowJointTrajectoryActionResult
#from moveit_msgs.msg import ExecuteTrajectoryActionGoal, ExecuteTrajectoryActionResult
from path_planning.srv import IK_fromFrame
from path_planning.srv import IK_fromQuater
import controller
import csv
import time



def IK_fromFrame_client(O_T_EE_array, q7, q_actual_array):
    rospy.wait_for_service('IK_service')
    try:
        IK_solver = rospy.ServiceProxy('IK_service', IK_fromFrame)
        resp = IK_solver(O_T_EE_array, q7, q_actual_array)
        return resp
    except rospy.ServiceException as e:
        print(f"Service call failed: {e}")



def IK_fromQuater_client(quater, O_EE, q7, q_actual_array):
    rospy.wait_for_service('IK_service')
    try:
        IK_solver = rospy.ServiceProxy('IK_service', IK_fromQuater)
        resp = IK_solver(quater, O_EE, q7, q_actual_array)
        return resp
    except rospy.ServiceException as e:
        print(f"Service call failed: {e}")





if __name__ == '__main__':
    rospy.init_node('controller')

    ttype = "follow_joint"

    t = []
    q = []
    #quater = np.array([0.79, 0.17, 0.57, 0.17])
    #O_EE = np.array([0.1, 0.1, 0.1])
    #q7 = pi/4
    q_actual_array = np.array([0, -0.785398163397, 0, -2.3561944899, 0, 1.57079632679, 0.785398163397])

    with open('/home/lozer/franka_emika_ws/src/neural_network/data/dataset/humanPoses.csv') as file:
        reader = csv.reader(file)

        doOnce = True
        for row in reader:
            if doOnce:
                doOnce = False
                continue

            quater = np.array([float(row[0]), float(row[1]), float(row[2]), float(row[3])])
            O_EE = np.array([float(row[4]), float(row[5]), float(row[6])])
            q7 = -pi/4 -pi/2 + float(row[7])

            res = IK_fromQuater_client(quater, O_EE, q7, q_actual_array)

            q_array_list = [res.q_array_1, res.q_array_2, res.q_array_3, res.q_array_4]
            q_array = []

            for array in q_array_list:
                if not np.isnan(np.array([array])).any():
                    q_array.append(array)

            
            print(q_array)

            if len(q_array) >= 1:
                t.append(2)
                q.append(list(q_array[0]))

                if len(q) > 0:
                    controller.homing(q[0], ttype)
                    if not len(q) == 1:
                        controller.launch_trajectory(t, q, ttype)

                time.sleep(5)
    
    

    







    
    


            


