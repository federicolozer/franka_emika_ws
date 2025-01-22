#!/usr/bin/env python3
# coding=utf-8
 
import csv
import numpy as np
from copy import deepcopy



def reader():
    humanPoses = []

    arm = ["thumb", "finger", "hand", "inside_elbow", "outside_elbow", "right_shoulder", "left_shoulder"]
    order = []
    
    with open('/home/lozer/franka_emika_ws/src/neural_network/data/tracking.csv') as file:
        reader = csv.reader(file)
        
        cnt = 0
        for row in reader:
            if cnt < 2:
                pass
            elif cnt == 2:
                for i in range(2, len(row)-2, 3):
                    order.append(arm.index(row[i]))
            else:
                cnt2 = 0
                pose = [None, None, None, None, None, None, None]

                for i in range(2, len(row)-2, 3):
                    if row[i] == "" or row[i+1] == "" or row[i+2] == "":
                        cnt2 += 1
                        continue

                    item = [float(row[i]), float(row[i+1]), float(row[i+2])]
                    pose[order[cnt2]] = item
                    cnt2 += 1

                humanPoses.append(pose)

            cnt += 1
    
    return humanPoses



def check(cPose):
    result = all(cPose)

    return result



def solver(cPose):
    base_frame = np.identity(4)
    ee_frame = np.identity(4)
    
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
    
    base_frame[0:3, 0] = deepcopy(xAxis)
    base_frame[0:3, 1] = deepcopy(yAxis)
    base_frame[0:3, 2] = deepcopy(zAxis)
    base_frame[0:3, 3] = cPose[5]

    eeToBase_frame = np.dot(np.linalg.inv(base_frame), ee_frame)

    print("--------------")
    print(ee_frame)
    print("--------------")
    print(base_frame)
    print("--------------")
    print(eeToBase_frame)

    
    res = [list(eeToBase_frame[0:3, 0]), list(eeToBase_frame[0:3, 1]), list(eeToBase_frame[0:3, 2]), list(eeToBase_frame[0:3, 3]), q7]

    return res
            





        
