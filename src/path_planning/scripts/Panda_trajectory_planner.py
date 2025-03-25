#!/usr/bin/env python3
# coding=utf-8

import rospy
import time
from copy import deepcopy
from trajectory_msgs.msg import JointTrajectoryPoint
from control_msgs.msg import FollowJointTrajectoryActionGoal, FollowJointTrajectoryActionResult
from moveit_msgs.msg import ExecuteTrajectoryActionGoal, ExecuteTrajectoryActionResult



def build_execute_trajectory(times, positions, velocities=None, accelerations=None, efforts=None):
    joint_names = ['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']

    msg = ExecuteTrajectoryActionGoal()

    msg.header.stamp = rospy.Duration(0)
    msg.header.frame_id = ''
    msg.goal.trajectory.joint_trajectory.header.stamp = rospy.Duration(0)
    msg.goal.trajectory.joint_trajectory.header.frame_id = ''
    msg.goal.trajectory.joint_trajectory.joint_names = joint_names 

    if not times.__class__.__name__ == "list":
        point = JointTrajectoryPoint()

        point.positions = positions
        if not velocities == None:
            point.velocities = velocities
        if not accelerations == None:
            point.accelerations = accelerations
        if not efforts == None:
            point.effort = efforts
        point.time_from_start = rospy.Duration(times)
        
        msg.goal.trajectory.joint_trajectory.points.append(deepcopy(point))

    else:
        for i in range(len(times)):
            point = JointTrajectoryPoint()

            point.positions = positions[i]
            if not velocities == None:
                point.velocities = velocities[i]
            if not accelerations == None:
                point.accelerations = accelerations[i]
            if not efforts == None:
                point.effort = efforts[i]
            point.time_from_start = rospy.Duration(times[i]-times[0])
            
            msg.goal.trajectory.joint_trajectory.points.append(deepcopy(point))

    time.sleep(0.4)

    return msg



def build_follow_joint_trajectory(times, positions, velocities=None, accelerations=None, efforts=None):
    joint_names = ['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']

    msg = FollowJointTrajectoryActionGoal()

    msg.header.stamp = rospy.Duration(0)
    msg.header.frame_id = ''
    msg.goal.trajectory.header.stamp = rospy.Duration(0)
    msg.goal.trajectory.header.frame_id = ''
    msg.goal.trajectory.joint_names = joint_names 

    if not times.__class__.__name__ == "list":
        point = JointTrajectoryPoint()

        point.positions = positions
        if not velocities == None:
            point.velocities = velocities
        if not accelerations == None:
            point.accelerations = accelerations
        if not efforts == None:
            point.effort = efforts
        point.time_from_start = rospy.Duration(times)
        
        msg.goal.trajectory.points.append(deepcopy(point))

    else:
        for i in range(len(times)):
            point = JointTrajectoryPoint()

            point.positions = positions[i]
            if not velocities == None:
                point.velocities = velocities[i]
            if not accelerations == None:
                point.accelerations = accelerations[i]
            if not efforts == None:
                point.effort = efforts[i]
            point.time_from_start = rospy.Duration(times[i]-times[0])
            
            msg.goal.trajectory.points.append(deepcopy(point))

    time.sleep(0.4)

    return msg




