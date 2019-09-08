#!/bin/bash
 
#source ~/.bashrc &
#gedit
export ROS_IP=192.168.101.91
export ROS_MASTER_URI=http://192.168.101.91:11311
export ROS_HOSTNAME=192.168.101.91
source /opt/ros/melodic/setup.bash
source ~/catkin_ws/devel/setup.bash
roslaunch pir2_app frame.launch
