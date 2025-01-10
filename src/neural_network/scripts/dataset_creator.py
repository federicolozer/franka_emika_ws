import csv
import numpy as np

if __name__ == "__main__":
    with open('/home/lozer/franka_emika_ws/src/neural_network/data/tracking.csv') as file:
        reader = csv.reader(file)

        humanPoses = []
        pose = np.zeros((4, 3))

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
                for i in range(2, len(row)-2, 3):
                    item = np.array([row[i], row[i+1], row[i+2]])
                    pose[order[cnt2]] = item
                    cnt2 += 1

                humanPoses.append(pose)

            cnt += 1
        
        for i in range(len(humanPoses)):
            print("-------------")
            print(humanPoses[i])

            cpose = humanPoses[i]
            O_ee = (cpose[0]+cpose[1])/2
            print(O_ee)

            quit()

        
