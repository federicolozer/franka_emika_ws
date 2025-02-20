#!/usr/bin/env python3
# coding=utf-8

import rospy
from gazebo_msgs.srv import SetPhysicsProperties
from geometry_msgs.msg import Vector3
from std_srvs.srv import Empty




if __name__ == '__main__':    
    rospy.init_node('change_gravity')
    set_physics = rospy.ServiceProxy("/gazebo/set_physics_properties", SetPhysicsProperties)
    unpause_physics = rospy.ServiceProxy("/gazebo/unpause_physics", Empty)

    gravity = Vector3()
    mode = 0
    if not rospy.search_param('/mode') == None:
        param = rospy.get_param('/mode')
        if param == "horz":
            mode = 1
            gravity.x = -9.8
        elif param == "horz_rev":
            mode = 2
            gravity.x = -9.8
        elif param == "ceil":
            mode = 3
            gravity.z = 9.8

    print("########################################")
    print(set_physics.call(gravity=gravity))
    print("########################################")
    
    unpause_physics.call()

    reset = rospy.ServiceProxy("/gazebo/reset_world", Empty)
    print(reset.call())
   