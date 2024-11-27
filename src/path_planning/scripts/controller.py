#!/usr/bin/env python3
# coding=utf-8

import rospy
from copy import deepcopy
import time
import numpy as np
from tqdm import tqdm
from sensor_msgs.msg import JointState
from control_msgs.msg import FollowJointTrajectoryActionGoal, FollowJointTrajectoryActionResult
from moveit_msgs.msg import ExecuteTrajectoryActionGoal, ExecuteTrajectoryActionResult
import Panda_trajectory_planner as planner


status = None
error_log = None
q_reg = []


def CallbackJointStates(data):
    global q_reg

    q_reg = data.position[0:7]



def CallbackResult(data):
    global status, error_log
    
    status = data.status.status
    error_log = data.result.error_code



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
    


def launch_execute_trajectory(t, q):
    global status, error_log

    joint_states_subscriber = rospy.Subscriber('/joint_states', JointState, CallbackJointStates)    
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



def launch_follow_joint_trajectory(t, q):
    global status, error_log

    joint_states_subscriber = rospy.Subscriber('/joint_states', JointState, CallbackJointStates)
    result_subscriber = rospy.Subscriber('/position_joint_trajectory_controller/follow_joint_trajectory/result', FollowJointTrajectoryActionResult, CallbackResult)
    control_publisher = rospy.Publisher('/position_joint_trajectory_controller/follow_joint_trajectory/goal', FollowJointTrajectoryActionGoal, queue_size = 10)
    
    msg = planner.build_follow_joint_trajectory(t, q)
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
    rospy.init_node('controller')

    t = [0, 3, 6]
    q = [[0, -0.785, 0, -2.356, 0, 1.571, 0.785], 
        [1, -0.785, 0, -2.356, 0, 1.571, 0.785], 
        [0, -0.785, 0, -2.356, 0, 1.571, 0.785]]

    launch_execute_trajectory(t, q)

    







    
    


            


