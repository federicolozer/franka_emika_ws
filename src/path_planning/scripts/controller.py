#!/usr/bin/env python3
# coding=utf-8

import rospy
from copy import deepcopy
import numpy as np
from tqdm import tqdm
from math import pi
from sensor_msgs.msg import JointState
from control_msgs.msg import FollowJointTrajectoryActionGoal, FollowJointTrajectoryActionResult
from moveit_msgs.msg import ExecuteTrajectoryActionGoal, ExecuteTrajectoryActionResult
from path_planning.srv import IK
import Panda_trajectory_planner as planner


status = None
error_log = None
q_reg = []
q_p_lim = np.array([2.1750, 2.1750, 2.1750, 2.1750, 2.6100, 2.6100, 2.6100])


def CallbackJointStates(data):
    global q_reg

    q_reg = list(data.position[0:7])



def CallbackResult(data):
    global status, error_log
    
    status = data.status.status
    error_log = data.result.error_code



def IK_client(O_T_EE_array, q7, q_actual_array):
    rospy.wait_for_service('IK_service')
    try:
        IK_solver = rospy.ServiceProxy('IK_service', IK)
        resp = IK_solver(O_T_EE_array, q7, q_actual_array)
        return resp
    except rospy.ServiceException as e:
        print(f"Service call failed: {e}")



def wait_execution(t_tot):
    global status

    t0 = rospy.get_time()

    for i in tqdm (range(100), desc="Execution", ascii=False, ncols=100, bar_format="{l_bar}{bar}"):
        t = rospy.get_time()
        while (t - t0)/t_tot*100 < i:
            t = rospy.get_time()
            continue

    while status == None:
        continue
    


def homing(q_last, ttype):
    global status, error_log, q_reg, q_p_lim
    
    joint_states_subscriber = rospy.Subscriber('/joint_states', JointState, CallbackJointStates) 

    while q_reg == []:
        pass

    q_diff = deepcopy(q_reg)
    for i in range(len(q_diff)):
        q_diff[i] -= q_last[i]
        q_diff[i] = q_diff[i]/(0.2*q_p_lim[i]) + 0.1
    
    t = [0, max(q_diff)]
    q = [q_reg, q_last]

    if ttype == "follow_joint":
        result_subscriber = rospy.Subscriber('/position_joint_trajectory_controller/follow_joint_trajectory/result', FollowJointTrajectoryActionResult, CallbackResult)
        control_publisher = rospy.Publisher('/position_joint_trajectory_controller/follow_joint_trajectory/goal', FollowJointTrajectoryActionGoal, queue_size = 10)

        msg = planner.build_follow_joint_trajectory(t, q)

    elif ttype == "execute":
        result_subscriber = rospy.Subscriber('/execute_trajectory/result', ExecuteTrajectoryActionResult, CallbackResult)
        control_publisher = rospy.Publisher('/execute_trajectory/goal', ExecuteTrajectoryActionGoal, queue_size = 10)

        msg = planner.build_execute_trajectory(t, q)

    control_publisher.publish(msg)

    print("Homing\n")
    while status == None:
        pass
    
    if not status == 3:
        print(f"Homing ended with an error:\n{error_log}")

    joint_states_subscriber.unregister()
    result_subscriber.unregister()




def launch_trajectory(t, q, ttype):
    global status, error_log

    joint_states_subscriber = rospy.Subscriber('/joint_states', JointState, CallbackJointStates)

    if ttype == "follow_joint":
        result_subscriber = rospy.Subscriber('/position_joint_trajectory_controller/follow_joint_trajectory/result', FollowJointTrajectoryActionResult, CallbackResult)
        control_publisher = rospy.Publisher('/position_joint_trajectory_controller/follow_joint_trajectory/goal', FollowJointTrajectoryActionGoal, queue_size = 10)

        msg = planner.build_follow_joint_trajectory(t, q)

    elif ttype == "execute":
        result_subscriber = rospy.Subscriber('/execute_trajectory/result', ExecuteTrajectoryActionResult, CallbackResult)
        control_publisher = rospy.Publisher('/execute_trajectory/goal', ExecuteTrajectoryActionGoal, queue_size = 10)

        msg = planner.build_execute_trajectory(t, q)
    
    control_publisher.publish(msg)

    print("Starting trajectory\n")
    wait_execution(t[-1])

    if status == 3:
        print("\nTrajectory executed correctly")
    else:
        print(f"\nTrajectory ended with an error:\n{error_log}")

    joint_states_subscriber.unregister()
    result_subscriber.unregister()




if __name__ == '__main__':
    #if len(sys.argv) > 0:
    #    print(sys.argv[1])
    #    if sys.argv[1] == "ext":
    #        print("si")
#
    #quit()

    rospy.init_node('controller')

    ttype = "follow_joint"

    t = []
    q = []

    # 0.281895,  -0.927236, 0.246513, 0, -0.741623, -0.37359, -0.557158, 0, 0.608712, -0.0257594, -0.792973, 0, -0.144822, 0.114741, 0.17244, 1 

    
    


    while True:
        t = []
        q = []

        O_T_EE_array = np.array([1.0, 0.0, 0.0, 0.0, 
                                 0.0, -1.0, 0.0, 0.0, 
                                 0.0, 0.0, -1.0, 0.0, 
                                 0.7, 0.0, 0.4, 1.0])
        #O_T_EE_array = np.array([0.281895,  -0.927236, 0.246513, 0, -0.741623, -0.37359, -0.557158, 0, 0.608712, -0.0257594, -0.792973, 0, -0.144822, 0.114741, 0.17244, 1])
        q7 = pi/4
        q_actual_array = np.array([0, -0.785398163397, 0, -2.3561944899, 0, 1.57079632679, 0.785398163397])
        #q_actual_array = np.array([0.5157262388785411,  1.2140897359597562,  1.5346381355065786, -3.0398301021734246, -1.2930720893855998, 1.332867311125138, -1.5554459725458225])

        #x = float(input("\nEnter x value: "))
        #O_T_EE_array[12] = x
        #y = float(input("\nEnter y value: "))
        #O_T_EE_array[13] = y
        #z = float(input("\nEnter z value: "))
        #O_T_EE_array[14] = z
        q7 = float(input("\nEnter q7 value: ")) + pi/4

        res = IK_client(O_T_EE_array, q7, q_actual_array)

        t.append(1)
        q.append(list(res.q_array))
        print("q = ", q)
        
        """with open("/home/lozer/franka_emika_ws/src/path_planning/data/q_robot.xml", 'r') as traj:
            data = traj.read()
            traj_data = BeautifulSoup(data, features="xml")
            traj_list = traj_data.find_all('point')        

            for point in traj_list:
                t.append(float(point.get('time')))

                keypoint = []
                for jnt in point.text.split():
                    keypoint.append(float(jnt))
                
                q.append(keypoint)"""

        if len(q) > 0:
            homing(q[0], ttype)
            if not len(q) == 1:
                launch_trajectory(t, q, ttype)
        
        

    







    
    


            


