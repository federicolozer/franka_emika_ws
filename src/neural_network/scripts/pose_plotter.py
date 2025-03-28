#!/usr/bin/env python3
# coding=utf-8
 
import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
from neural_network.scripts.humanPoses import reader, solver

path = "/home/lozer/franka_emika_ws/src/neural_network/data/dataset/main.csv"



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

    plt.show()




if __name__ == "__main__":
    base_frame = np.identity(4)
    ee_frame = np.identity(4)
    
    humanPoses = reader()

    while True:
        n = input("Select frame to plot... \n")
        if n == "quit":
            break
        cPose = humanPoses[int(n)]
        res = solver(cPose)

        ee_frame[0:3, 0] = res[0]
        ee_frame[0:3, 1] = res[1]
        ee_frame[0:3, 2] = res[2]
        ee_frame[0:3, 3] = res[3]

        plotter(cPose, frames=[base_frame, ee_frame])

    





        
