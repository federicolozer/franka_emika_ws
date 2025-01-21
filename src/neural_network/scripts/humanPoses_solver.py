#!/usr/bin/env python3
# coding=utf-8
 
import csv
import numpy as np



def reader():
    humanPoses = []

    arm = ["thumb", "finger", "hand", "inside_elbow", "outside_elbow"]
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
                pose = [None, None, None, None, None]

                for i in range(2, len(row)-2, 3):
                    item = [float(row[i]), float(row[i+1]), float(row[i+2])]
                    pose[order[cnt2]] = item
                    cnt2 += 1

                humanPoses.append(pose)

            cnt += 1

    return humanPoses



def solver(cPose):    
    #for i in range(len(humanPoses)):
    #frame_ee = np.identity(4)
    #frame_q7 = np.identity(4)

    #print("-------------")
    #print(humanPoses[i])
    

    #cPose = humanPoses[i]

    
    
    O_ee = (np.array(cPose[0])+np.array(cPose[1]))/2
    elbow = (np.array(cPose[3])+np.array(cPose[4]))/2

    segm_ee_finger = np.array(cPose[1])-O_ee
    segm_hand_ee = O_ee-np.array(cPose[2])
    segm_hand_elbow = elbow-np.array(cPose[2])



    

    #yAxis = (segm_ee_finger)/np.linalg.norm(segm_ee_finger)
    zAxis = (segm_hand_ee)/np.linalg.norm(segm_hand_ee)
    yAxis_tmp = np.array(cPose[1])-(O_ee+np.dot(segm_ee_finger, zAxis)*zAxis)
    yAxis = (yAxis_tmp)/np.linalg.norm(yAxis_tmp)
    xAxis = np.cross(yAxis, zAxis)

    #frame_ee[0:3, 0] = xAxis
    #frame_ee[0:3, 1] = yAxis
    #frame_ee[0:3, 2] = zAxis
    #frame_ee[0:3, 3] = O_ee

    O_q7 = cPose[2]+(np.dot(segm_hand_elbow, segm_hand_ee)/np.linalg.norm(segm_hand_ee))*zAxis
    segm_q7_elbow = elbow-O_q7

    #frame_q7[0:3, 0] = xAxis
    #frame_q7[0:3, 1] = yAxis
    #frame_q7[0:3, 2] = zAxis
    #frame_q7[0:3, 3] = O_q7

    #print("-------------")
    #print(frame_ee)
    #print("-------------")
    #print(frame_q7)

    q7 = np.arccos(np.dot(segm_q7_elbow/np.linalg.norm(segm_q7_elbow), xAxis))
    res = [list(xAxis), list(yAxis), list(zAxis), list(O_ee), q7]

    return res
            





        
