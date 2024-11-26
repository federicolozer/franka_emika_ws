#!/usr/bin/env python3
# coding=utf-8

import rospy
from control_msgs.msg import FollowJointTrajectoryActionGoal
from trajectory_msgs.msg import JointTrajectoryPoint
from sensor_msgs.msg import JointState
from copy import deepcopy
import time
import numpy as np
from Panda_trajectory_planner import const_trajectory
from data_IO import reader, writer
import socket
import os

# per bloccare processo: kill -9 $(lsof -ti tcp:1024)

HOST = "172.16.1.1"
PORT = 1024

path = "/home/panda/Documents/Data_Optimizer/"
folder = None
q_p_lim = np.array([2.1750, 2.1750, 2.1750, 2.1750, 2.6100, 2.6100, 2.6100])    # rad/s
t_i = None
t_exp = []
q_exp = []
q_p_exp = []
tau_exp = []


def CallbackJointStates(data):
    global t_i, t_exp, q_exp, q_p_exp, tau_exp

    t = rospy.get_time()

    t_exp.append([t - t_i])  
    q_exp.append(data.position[0:7])
    q_p_exp.append(data.velocity)
    tau_exp.append(data.effort)



def data_receiver():
    global folder 

    fileI = open(f"{path}Input.txt", "w")

    while True: 
        #TCP input
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen() 

            try:                       
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024)
                    
                    if data == b"END":
                        break
                    else:
                        if not folder == data.decode():
                            print(f"Receiving {data.decode()}")
                            fileI.write(f"{data.decode()}\n")
                            
                        folder = data.decode()

                    data = conn.recv(1024)
                    
                    if not os.path.exists(f"{path}Trajectories"):
                        os.mkdir(f"{path}Trajectories")
                    if not os.path.exists(f"{path}Trajectories/{folder}"):
                        os.mkdir(f"{path}Trajectories/{folder}")
                    file = open(f"{path}Trajectories/{folder}/{data.decode()}.txt", "wb")
                    
                    data = conn.recv(1024)
                    while data:
                        file.write(data)
                        data = conn.recv(1024)  
                    file.close()

            except:
                print("Connection error")
                quit()
            
            s.close()

    fileI.close()




def test_manager():
    global t_i, t_exp, q_exp, q_p_exp, tau_exp

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        
        try:
            while True:            
                conn, addr = s.accept()
                
                with conn:
                    data = conn.recv(1024)
                    
                    if data == b'STOP':
                        conn.close()
                        print('Disconnected')
                        s.close()

                        time.sleep(1)
                        
                        print('Test execution finished')
                        break

                    print('Moving to the starting configuration')
                    
                    # Reading data to files ------------------------
                    path_name = f'/home/panda/Documents/{data.decode()}'

                    t, q, q_p, q_pp, q_ppp, tau, tau_p = reader(path_name)
                    
                    t_i = rospy.get_time()
                    
                    # Initialization subscriber node for /joint_states
                    sub_joint_states = rospy.Subscriber('/joint_states', JointState, CallbackJointStates)
                    
                    # Initialization publisher node for /position_joint_trajectory_controller/follow_joint_trajectory/goal
                    control_publisher = rospy.Publisher('/position_joint_trajectory_controller/follow_joint_trajectory/goal', FollowJointTrajectoryActionGoal, queue_size = 10)
                    
                    t_start = [] 
                    t_exp = []
                    q_exp = []
                    q_p_exp = []
                    tau_exp = []    

                    time.sleep(0.4)

                    for i in range(len(q[0])):
                        d = abs(q_exp[-1][i]-q[0][i])
                        t_start.append(d/(0.3*q_p_lim[i])+1)

                    msg = const_trajectory(max(t_start), q[0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0])

                    # Move to start configuration
                    control_publisher.publish(msg)

                    # Wait the end of the trajectory
                    time.sleep(max(t_start))

                    msg = const_trajectory(t, q, q_p, q_pp)

                    if data:
                        conn.send(b'START')
                        conn.close()

                        time.sleep(0.2)

                        print('Trajectory execution')
                        
                        # Move to configuration
                        control_publisher.publish(msg)
                        
                        t_i = rospy.get_time()
                        t_exp = []
                        q_exp = []
                        q_p_exp = []
                        tau_exp = []

                        time.sleep(t[-1])
                        
                        sub_joint_states.unregister()
                    
                        t_exp = np.array(t_exp)
                        q_exp = np.array(q_exp)
                        q_p_exp = np.array(q_p_exp)
                        tau_exp = np.array(tau_exp)
                        
                        writer(path_name, t_exp, q_exp, q_p_exp, [], [], tau_exp, [], arg="_exp")

            s.close()
        except:
            print("Connection error")
            quit()



def data_sender():
    global folder 

    while True: 
        #TCP input
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen() 

            try:                       
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024)
                    
                    if data == b"END":
                        break
                    else:
                        if not folder == data.decode():
                            print(f"Sending {data.decode()}")
                            
                        folder = data.decode()

                    data = conn.recv(1024)
                    
                    file = open(f"{path}Trajectories/{folder}/{data.decode()}_exp.txt", "rb")

                    data = file.read(1024)
                    while data:
                        conn.send(data)
                        data = file.read(1024)
                    file.close()
                    s.close

            except:
                print("Connection error")
                quit()
            
            s.close()




if __name__ == '__main__':
    rospy.init_node('trajectory_executor')

    time.sleep(1)
    print('\n\nWaiting for connection to acquire trajectory data')
    print('\nConnection...\n')
    data_receiver()

    time.sleep(1)
    print('\n\nWaiting for external input from LabView to start the tests')
    print('\nConnection...\n')
    test_manager()

    time.sleep(1)
    print('\n\nWaiting for connection to send trajectory data')
    print('\nConnection...\n')
    data_sender()



    
            


