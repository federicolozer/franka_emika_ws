#!/usr/bin/env python3
# coding=utf-8
 
import csv
import numpy as np
from copy import deepcopy
from math import pi
import os

path = "/home/lozer/franka_emika_ws/src/neural_network/data/tracking_data"
base_height = 0.7



def reader(target=None):
    humanPoses = []

    prefix = "arm"
    arm = ["EE", "finger", "hand", "elbow", "shoulder"]
    
    order = dict()
    for i in range(len(arm)):
        order[f"{prefix}_{arm[i]}"] = None
        arm[i] = prefix + "_" + arm[i]
    
    if target == None:
        tracking_data = list(os.walk(path))[0][2]
    else:
        tracking_data = list(target)
    
    for data in tracking_data:
        with open(path + "/" + data) as file:
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
                    pose = [None, None, None, None, None]
                    for i in range(2, len(row)-2, 3):
                        if row[i] == "" or row[i+1] == "" or row[i+2] == "":
                            continue
                        
                        item = [float(row[i]), float(row[i+1]), float(row[i+2])]
                        try:
                            pos = arm.index(list(order.keys())[list(order.values()).index(i)])
                        except:
                            continue
                        pose[pos] = item
                    if all(pose):
                        humanPoses.append(pose)
                else:
                    pass
                cnt += 1

    return humanPoses



def adjust(ee_frame, ah, bh):
    ar = 0.594
    br = 0.316
    ratio = (ar+br)/(ah+bh)

    ee_frame[0:2, 3] *= ratio
    ee_frame[2, 3] = ((ee_frame[2, 3]-base_height)*ratio)+base_height

    return ee_frame



def solver(cPose):
    ee_frame = np.identity(4)
    rMat = np.array([[1, 0, 0],
                    [0, 0, -1],
                    [0, 1, 0]])

    ref = deepcopy([cPose[4][0], cPose[4][1], cPose[4][2]])
    
    for i in range(len(cPose)):
        cPose[i] = deepcopy([cPose[i][0]-ref[0], cPose[i][1]-ref[1], cPose[i][2]-ref[2]])
        cPose[i] = deepcopy(np.dot(rMat, np.array(cPose[i])))
        cPose[i][2] += base_height

    O_ee = np.array(cPose[0])
    hand = np.array(cPose[2])
    elbow = np.array(cPose[3])
    shoulder = np.array(cPose[4])

    segm_ee_finger = np.array(cPose[1])-O_ee
    segm_hand_ee = O_ee-hand
    segm_hand_elbow = elbow-hand
    segm_elbow_shoulder = shoulder-elbow

    zAxis = (segm_hand_ee)/np.linalg.norm(segm_hand_ee)
    yAxis_tmp = np.array(cPose[1])-(O_ee+np.dot(segm_ee_finger, zAxis)*zAxis)
    yAxis = (yAxis_tmp)/np.linalg.norm(yAxis_tmp)
    xAxis = np.cross(yAxis, zAxis)

    ee_frame[0:3, 0] = deepcopy(xAxis)
    ee_frame[0:3, 1] = deepcopy(yAxis)
    ee_frame[0:3, 2] = deepcopy(zAxis)
    ee_frame[0:3, 3] = O_ee

    O_q7 = hand+(np.dot(segm_hand_elbow, segm_hand_ee)/np.linalg.norm(segm_hand_ee))*zAxis
    segm_q7_elbow = elbow-O_q7
    q7 = pi/4 - np.arccos(np.dot(segm_q7_elbow/np.linalg.norm(segm_q7_elbow), -xAxis))

    ee_frame = adjust(ee_frame, np.linalg.norm(segm_hand_elbow)+np.linalg.norm(segm_hand_ee), np.linalg.norm(segm_elbow_shoulder))

    res = [list(ee_frame[0:3, 0]), list(ee_frame[0:3, 1]), list(ee_frame[0:3, 2]), list(ee_frame[0:3, 3]), q7]

    return res