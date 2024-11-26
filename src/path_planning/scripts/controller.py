#!/usr/bin/env python3
# coding=utf-8

import rospy
from copy import deepcopy
import time
import numpy as np
from trajectory_msgs.msg import JointTrajectoryPoint
from sensor_msgs.msg import JointState
from control_msgs.msg import FollowJointTrajectoryActionGoal
from moveit_msgs.msg import ExecuteTrajectoryActionGoal




def CallbackJointStates(data):
    print(data.position[0:7])



def CallbackDesiredJointStates(data):
    print(data.position[0:7])



if __name__ == '__main__':
    rospy.init_node('controller')

    t = [0, 3]
    q = [[0, -0.785, 0, -2.356, 0, 1.571, 0.785], [1, -0.785, 0, -2.356, 0, 1.571, 0.785]]

    sub_joint_states = rospy.Subscriber('/joint_states', JointState, CallbackJointStates)
    #sub_desired_joint_states = rospy.Subscriber('/joint_states_desired', JointState, CallbackDesiredJointStates)

    control_publisher = rospy.Publisher('/position_joint_trajectory_controller/follow_joint_trajectory/goal', FollowJointTrajectoryActionGoal, queue_size = 10)
    
    const_trajectory(t, q)
    control_publisher.publish(msg)

    print("trajectory published")
    time.sleep(t[-1])
    


            


