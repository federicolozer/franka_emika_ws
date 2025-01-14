import csv
import numpy as np
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

if __name__ == "__main__":
    with open('/home/lozer/franka_emika_ws/src/neural_network/data/tracking.csv') as file:
        reader = csv.reader(file)

        humanPoses = []

        arm = ["thumb", "finger", "hand", "inside_elbow", "outside_elbow"]
        order = []

        cnt = 0
        for row in reader:
            if cnt < 2:
                pass
            elif cnt == 2:
                for i in range(2, len(row)-2, 3):
                    order.append(arm.index(row[i]))
            else:
                cnt2 = 0
                pose = np.zeros((5, 3))

                for i in range(2, len(row)-2, 3):
                    item = np.array([row[i], row[i+1], row[i+2]])
                    pose[order[cnt2]] = item
                    cnt2 += 1

                humanPoses.append(pose)

            cnt += 1
        
        for i in range(len(humanPoses)):
            t0 = time.time()
            #frame_ee = np.identity(4)
            #frame_q7 = np.identity(4)

            #print("-------------")
            #print(humanPoses[i])
            

            cpose = humanPoses[i]
            
            O_ee = (cpose[0]+cpose[1])/2
            elbow = (cpose[3]+cpose[4])/2

            segm_ee_finger = cpose[1]-O_ee
            segm_hand_ee = O_ee-cpose[2]
            segm_hand_elbow = elbow-cpose[2]

            #yAxis = (segm_ee_finger)/np.linalg.norm(segm_ee_finger)
            zAxis = (segm_hand_ee)/np.linalg.norm(segm_hand_ee)
            yAxis = cpose[1]-(O_ee+np.dot(segm_ee_finger, zAxis)*zAxis)
            xAxis = np.cross(yAxis, zAxis)

            #frame_ee[0:3, 0] = xAxis
            #frame_ee[0:3, 1] = yAxis
            #frame_ee[0:3, 2] = zAxis
            #frame_ee[0:3, 3] = O_ee

            O_q7 = cpose[2]+(np.dot(segm_hand_elbow, segm_hand_ee)/np.linalg.norm(segm_hand_ee))*zAxis

            #frame_q7[0:3, 0] = xAxis
            #frame_q7[0:3, 1] = yAxis
            #frame_q7[0:3, 2] = zAxis
            #frame_q7[0:3, 3] = O_q7

            #print("-------------")
            #print(frame_ee)
            #print("-------------")
            #print(frame_q7)

            q7 = np.arccos(np.dot(segm_hand_elbow/np.linalg.norm(segm_hand_elbow), xAxis))
            print("-------------")
            print(q7)
            
            te = time.time()
            print("Elapsed time: ", te-t0, "s")

            # Plot
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

            aa = np.array((1,1,1))

            
            ax.scatter(cpose[0, 0], cpose[0, 1], cpose[0, 2], c=np.array([0, 0.5, 0.8]))
            ax.scatter(cpose[1, 0], cpose[1, 1], cpose[1, 2], c=np.array([0, 0.5, 0.8]))
            ax.scatter(cpose[2, 0], cpose[2, 1], cpose[2, 2], c=np.array([0, 0.5, 0.8]))
            ax.scatter(O_ee[0], O_ee[1], O_ee[2], c=np.array([0, 0.5, 0.8]))
            ax.scatter(O_q7[0], O_q7[1], O_q7[2], c=np.array([0, 0.5, 0.8]))
            ax.scatter(elbow[0], elbow[1], elbow[2], c=np.array([0, 0.5, 0.8]))

            ax.plot([cpose[0, 0], cpose[1, 0]], [cpose[0, 1], cpose[1, 1]], [cpose[0, 2], cpose[1, 2]], linestyle="--", c=np.array([0.8, 0.5, 0.8]))
            ax.plot([O_ee[0], O_q7[0], elbow[0]], [O_ee[1], O_q7[1], elbow[1]], [O_ee[2], O_q7[2], elbow[2]], linestyle="--", c=np.array([0.8, 0.5, 0.8]))

            ax.set(xticklabels=[], yticklabels=[], zticklabels=[])

            plt.show()

            quit()

        
