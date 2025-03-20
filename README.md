<div align="center">
    <img src="media/LogoUniud.png" width="150">
</div>

# Franka Emika workspace

This workspace contains all the packages used for tests and simulations regarding Franka Emika Panda Robot.

<p align="center">
    <img src="media/Panda.png"  width="400">
</p>

## Installation

### ROS environment

Firts of all, you need to install the ROS environment.
For this project, ROS Melodic Morenia distro is needed.
You can find the whole procedure [**here**](https://wiki.ros.org/melodic/Installation)

Then you are ready to install this project repository.
```shell script
git clone https://github.com/federicolozer/franka_emika_ws.git
```

Once installed, you need to build the project
```shell script
cd franka_emika_ws/src
catkin_make -D
```
