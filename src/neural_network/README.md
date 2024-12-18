# Instructions to get ready with minimum time-jerk trajectory tests

## Setup
* **Windows PC** with orange label (password written on it)
* **This PC** with pink label (password written on it)
* **National Instruments sensors and modules** all inside the box
* **Panda Robot**

## Initialize the robot
Switch on the robot controller manually.
Set Ethernet(enp4s0) on the top-right corner of the screen to "Right robot".
On Chrome, search the Desk page by digiting ip "172.16.0.2" in the URL search bar.
Click the "Unlock" icon under the section "Joints" in the right side of the page.
If the robot light is blue, robot is ready to work.
If the robot light is white, robot is in free-ride mode, and you got to unlock the change mode button on the desk.
To move robot in free-ride mode you got to grab the end effector and press at the same time the two buttons placed on it.
Then you can move the robot as yuo want by pulling and pushing it.


## Connection between PCs
Connect one side of the ethernet cable to the port on the Windows PC and the other side to the lower port on this PC.
On this PC, set Ethernet(enp3s0) on the top-right corner of the screen to "UDP connection".
On this PC, to check the connection, write on terminal:
```shell script
ping 172.16.1.10
```

# Minimum time-jerk trajectories tests

Make sure that the National Instrument modules are connected to the Windows PC through the USB cable and to the electric line.
On Windows PC, add a folder with trajectory files (q.txt, q_p.txt, q_pp.txt and t.txt) in the "Documents/Data_Optimizer/Trajectories" folder.
Then in "Documents/Data_Optimizer" path, you got to add the names of the folders you added previously in the "Input.txt" file, one in each row.
On this PC, to launch the control program, write on terminal:
```shell script
roslaunch path_planning start_test.launch
```
On Windows PC, to start the whole process, double click "Exec_Tests.cmd" executable from desktop.
This file will execute 4 actions:
* Launch "data_sender.py", which will automatically pass to this PC all the trajectory data needed from Windows PC
* Launch LabVIEW program for data acquisition. Action required, described below
* Launch "data_receiver_.py", which will automatically pass to Windows PC all the joint states data acquired from this PC
* Launch Matlab to process and plot all the signal acquired automatically

On Windows PC, to start the tests when LabVIEW is on, press Run button (the white arrow) on the top-left corner of the Front Panel.
