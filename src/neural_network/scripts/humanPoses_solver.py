#!/usr/bin/env python3
# coding=utf-8
 
import csv
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import sin, cos, asin, acos
import os

path = "/home/lozer/franka_emika_ws/src/neural_network/data/tracking_data"
base_height = 0.7



def plotter(markers, segments= None, frames=None):
    x = []
    y = []
    z = []

    for lst in markers:
        x.append(lst[0])
        y.append(lst[1])
        z.append(lst[2])

    # Create a figure and a 3D axis
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the data
    ax.scatter3D(x, y, z, color='black')

    # Set plot title and labels
    plt.title("Simple 3D Scatter Plot")
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_xlim(-0.2, 0.8)
    ax.set_ylim(-0.5, 0.5)
    ax.set_zlim(0, 1)

    if not segments == None:
        for segment in segments:
            ax.plot3D([segment[0][0], segment[1][0]], [segment[0][1], segment[1][1]], [segment[0][2], segment[1][2]], color='green')

    if not frames == None:
        for frame in frames:
            O = frame[0:3, 3]
            x_dir = np.dot(frame, [0.1, 0, 0, 1])
            y_dir = np.dot(frame, [0, 0.1, 0, 1])
            z_dir = np.dot(frame, [0, 0, 0.1, 1])

            ax.plot3D([x_dir[0], O[0]], [x_dir[1], O[1]], [x_dir[2], O[2]], color='red')
            ax.plot3D([y_dir[0], O[0]], [y_dir[1], O[1]], [y_dir[2], O[2]], color='green')
            ax.plot3D([z_dir[0], O[0]], [z_dir[1], O[1]], [z_dir[2], O[2]], color='blue')

    # Show the plot
    #plt.pause(5)
    plt.show()



def reader():
    humanPoses = []

    prefix = "Arm"
    arm = ["thumb", "finger", "hand", "inside_elbow", "outside_elbow", "shoulder"]
    
    order = dict()
    for i in range(len(arm)):
        #order[f"{prefix}_{i}"] = None
        order[prefix + "_" + arm[i]] = None
        arm[i] = prefix + "_" + arm[i]

    for folder in os.walk(path):
        for file in folder[2]:
            with open(path+"/"+file) as file:
                reader = csv.reader(file)
                
                cnt = 0
                for row in reader:
                    if cnt == 3:
                        for i in range(2, len(row)-2, 3):
                            if row[i] in order:
                                order[row[i]] = i
                            else:
                                continue
                    
                    elif cnt >=7:
                        pose = [None, None, None, None, None, None]

                        for i in range(2, len(row)-2, 3):
                            if row[i] == "" or row[i+1] == "" or row[i+2] == "":
                                continue

                            item = [float(row[i]), float(row[i+1]), float(row[i+2])]
                            pos = arm.index(list(order.keys())[list(order.values()).index(i)])
                            pose[pos] = item

                        humanPoses.append(pose)
                    else:
                        pass

                    cnt += 1
    
    return humanPoses



def check(cPose):
    result = all(cPose)

    return result



def adjust(ee_frame, q7, ah, bh):
    #ah = 0.345
    #bh = 0.302
    ar = 0.594
    br = 0.316
    ratio = (ar+br)/(ah+bh)
    ratio = 1.4

    #print(cos(q7)*ah) 
    #print(acos(ee_frame[0, 3] - cos(q7)*ah)/bh)
    #print(cos(asin((-sin(acos((ee_frame[0, 3] - cos(q7)*ah)/bh))*bh + sin(q7)*(ah + ar))/br)))
    #q7 = acos((ee_frame[0, 3] - cos(asin((-sin(acos((ee_frame[0, 3] - cos(q7)*ah)/bh))*bh + sin(q7)*(ah + ar))/br))*br)/ar) 
    
    ee_frame[0:2, 3] *= ratio
    ee_frame[2, 3] = ((ee_frame[2, 3]-base_height)*ratio)+base_height

    return ee_frame, q7



def solver(cPose):
    base_frame = np.identity(4)
    ee_frame = np.identity(4)
    rMat = np.array([[1, 0, 0],
                    [0, 0, -1],
                    [0, 1, 0]])

    ref = deepcopy([cPose[5][0], cPose[5][1], cPose[5][2]])
    #ref = deepcopy(np.dot(rMat, np.array(ref)))

    for i in range(len(cPose)):
        cPose[i] = deepcopy([cPose[i][0]-ref[0], cPose[i][1]-ref[1], cPose[i][2]-ref[2]])
        cPose[i] = deepcopy(np.dot(rMat, np.array(cPose[i])))
        cPose[i][2] += base_height

    O_ee = (np.array(cPose[0])+np.array(cPose[1]))/2
    elbow = (np.array(cPose[3])+np.array(cPose[4]))/2

    segm_ee_finger = np.array(cPose[1])-O_ee
    segm_hand_ee = O_ee-np.array(cPose[2])
    segm_hand_elbow = elbow-np.array(cPose[2])
    segm_elbow_shoulder = np.array(cPose[5])-elbow

    zAxis = (segm_hand_ee)/np.linalg.norm(segm_hand_ee)
    yAxis_tmp = np.array(cPose[1])-(O_ee+np.dot(segm_ee_finger, zAxis)*zAxis)
    yAxis = (yAxis_tmp)/np.linalg.norm(yAxis_tmp)
    xAxis = np.cross(yAxis, zAxis)

    ee_frame[0:3, 0] = deepcopy(xAxis)
    ee_frame[0:3, 1] = deepcopy(yAxis)
    ee_frame[0:3, 2] = deepcopy(zAxis)
    ee_frame[0:3, 3] = O_ee

    O_q7 = cPose[2]+(np.dot(segm_hand_elbow, segm_hand_ee)/np.linalg.norm(segm_hand_ee))*zAxis
    segm_q7_elbow = elbow-O_q7
    q7 = np.arccos(np.dot(segm_q7_elbow/np.linalg.norm(segm_q7_elbow), -xAxis))

    #zAxis = np.array([0, 0, 1])
    #xAxis_tmp = np.array(cPose[5])-(cPose[6]+np.dot(segm_shoulder_shoulder, zAxis)*zAxis)
    #xAxis = (xAxis_tmp)/np.linalg.norm(xAxis_tmp)
    #yAxis = -np.cross(xAxis, zAxis)

    #plotter(cPose, frames=[base_frame, ee_frame])

    ee_frame, q7 = adjust(ee_frame, q7, np.linalg.norm(segm_hand_elbow)+np.linalg.norm(segm_hand_ee), np.linalg.norm(segm_elbow_shoulder))

    res = [list(ee_frame[0:3, 0]), list(ee_frame[0:3, 1]), list(ee_frame[0:3, 2]), list(ee_frame[0:3, 3]), q7]

    return res


if __name__ == "__main__":
    h = reader()  
    solver(h[0])    





        
