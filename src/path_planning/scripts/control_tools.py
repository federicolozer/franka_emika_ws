#!/usr/bin/env python3
# coding=utf-8

import rospy
from copy import deepcopy
import numpy as np
from tqdm import tqdm
from sensor_msgs.msg import JointState
from control_msgs.msg import FollowJointTrajectoryActionGoal, FollowJointTrajectoryActionResult
from moveit_msgs.msg import ExecuteTrajectoryActionGoal, ExecuteTrajectoryActionResult
from path_planning.srv import IK_fromFrame, IK_fromQuater
import Panda_trajectory_planner as planner
from progress.bar import IncrementalBar as Bar


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



def readJointStates():
    joint_states_subscriber = rospy.Subscriber('/joint_states', JointState, CallbackJointStates) 

    while q_reg == []:
        pass

    joint_states_subscriber.unregister()

    return q_reg
    


def IK_fromFrame_client(O_T_EE_array, q7, q_actual_array, horz):
    rospy.wait_for_service('IK_service')
    try:
        IK_solver = rospy.ServiceProxy('IK_service', IK_fromFrame)
        resp = IK_solver(O_T_EE_array, q7, q_actual_array, horz)
        return resp
    except rospy.ServiceException as e:
        print(f"Service call failed: {e}")



def IK_fromQuater_client(quater, O_EE, q7, q_actual_array, horz):
    rospy.wait_for_service('IK_service')
    try:
        IK_solver = rospy.ServiceProxy('IK_service', IK_fromQuater)
        resp = IK_solver(quater, O_EE, q7, q_actual_array, horz)
        return resp
    except rospy.ServiceException as e:
        print(f"Service call failed: {e}")



def wait_execution(t_tot):
    global status

    t0 = rospy.get_time()

    bar = Bar('Execution', max=100)
    for i in range(100):
        t = rospy.get_time()
        while (t - t0)/t_tot*100 < i:
            t = rospy.get_time()
            pass
        bar.next()
        
    bar.finish()

    while status == None:
        continue
    


def homing(q_last, ttype):
    global status, error_log, q_reg, q_p_lim
    
    q_diff = readJointStates()
    for i in range(len(q_diff)):
        q_diff[i] -= q_last[i]
        q_diff[i] = q_diff[i]/(0.2*q_p_lim[i]) + 0.1
    
    t = [0, min([3, max(q_diff)])]
    print(t)
    t = [0, 2]
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

    result_subscriber.unregister()




def exec_trajectory(t, q, ttype):
    global status, error_log

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

    result_subscriber.unregister()



def launch_trajectory(t, q, ttype):
    if len(q) > 0:
            homing(q[0], ttype)
            if not len(q) == 1:
                exec_trajectory(t, q, ttype)



    







    
    


            


