#!/usr/bin/env python3
# coding=utf-8

import rospy
import os

if __name__ == '__main__':
    rospy.init_node('controller')

    gravity = [0, 0, 0]
    if not rospy.search_param('/mode') == None:
        param = rospy.get_param('/mode')
        if param == "vert":
            gravity[2] = -9.8
        elif param == "horz":
            gravity[0] = -9.8
        elif param == "ceil":
            gravity[2] = 9.8            

    msg = "rosrun dynamic_reconfigure dynparam set /gazebo \"{" + f"'gravity_x':{gravity[0]}, 'gravity_y':{gravity[1]}, 'gravity_z':{gravity[2]}" + "}\""
    os.system(msg)
