#!/usr/bin/env python3
# coding=utf-8
 
import csv
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


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
    arm = ["thumb", "finger", "hand", "inside_elbow", "outside_elbow", "right_shoulder", "left_shoulder"]
    
    order = dict()
    for i in range(len(arm)):
        #order[f"{prefix}_{i}"] = None
        order[prefix + "_" + arm[i]] = None
        arm[i] = prefix + "_" + arm[i]

    
    with open('/home/lozer/franka_emika_ws/src/neural_network/data/Take 2025-01-31 10.32.23 AM.csv') as file:
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
                pose = [None, None, None, None, None, None, None]

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



def solver(cPose):
    base_frame = np.identity(4)
    ee_frame = np.identity(4)

    ref = deepcopy([cPose[5][0], -cPose[5][2], cPose[5][1]])


    for i in range(len(cPose)):
        cPose[i] = deepcopy([cPose[i][0]-ref[0], -cPose[i][2]-ref[1], cPose[i][1]-ref[2]+0.333])
        rMat = np.array([[-1, 0, 0],
                            [0, -1, 0],
                            [0, 0, 1]])

        cPose[i] = deepcopy(np.dot(rMat, np.array(cPose[i])))

    O_ee = (np.array(cPose[0])+np.array(cPose[1]))/2
    elbow = (np.array(cPose[3])+np.array(cPose[4]))/2

    segm_ee_finger = np.array(cPose[1])-O_ee
    segm_hand_ee = O_ee-np.array(cPose[2])
    segm_hand_elbow = elbow-np.array(cPose[2])
    segm_shoulder_shoulder = np.array(cPose[5])-np.array(cPose[6])

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
    q7 = np.arccos(np.dot(segm_q7_elbow/np.linalg.norm(segm_q7_elbow), xAxis))

    zAxis = np.array([0, 0, 1])
    xAxis_tmp = np.array(cPose[5])-(cPose[6]+np.dot(segm_shoulder_shoulder, zAxis)*zAxis)
    xAxis = (xAxis_tmp)/np.linalg.norm(xAxis_tmp)
    yAxis = -np.cross(xAxis, zAxis)

    #plotter(cPose, frames=[base_frame, ee_frame])
    res = [list(ee_frame[0:3, 0]), list(ee_frame[0:3, 1]), list(ee_frame[0:3, 2]), list(ee_frame[0:3, 3]), q7]

    return res


if __name__ == "__main__":
    h = reader()  
    solver(h[0])    





        
