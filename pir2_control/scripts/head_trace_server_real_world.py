#!/usr/bin/env python

import rospy
import numpy as np
from math import radians, copysign, sqrt, pow, pi, atan2, degrees
import tf
import PyKDL

from std_msgs.msg import Float64
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from geometry_msgs.msg import Quaternion

MAX_PAN_POS = 3.4
MIN_PAN_POS = -3.4

MAX_TILT_POS = 0.30
MIN_TILT_POS = -0.34

def constrain(input, low, high):
    if input < low:
      input = low
    elif input > high:
      input = high
    else:
      input = input

    return input

def checkPanLimitPosition(pos):
    pos = constrain(pos, MIN_PAN_POS, MAX_PAN_POS)

    return pos

def checkTiltLimitPosition(pos):
    pos = constrain(pos, MIN_TILT_POS, MAX_TILT_POS)

    return pos

def head_make(pan,tilt):
    head_pub = rospy.Publisher('/dynamixel_workbench_head/joint_trajectory', JointTrajectory, queue_size=100)
    head_msg = JointTrajectory()
    jtp_msg = JointTrajectoryPoint()
    head_msg.joint_names = [ "pan_joint", "tilt_joint", "yaw_joint" ]
    head_msg.header.stamp = rospy.Time.now()
    # jtp_msg.points.positions = [control_pan_pos,control_tilt_pos,control_yaw_pos]

    jtp_msg.positions = [pan,tilt,0.0]
    jtp_msg.time_from_start = rospy.Duration.from_sec(0.00000002)

    head_msg.points.append(jtp_msg)
    head_pub.publish(head_msg)

def get_distance(x, y):
    d = sqrt((x) ** 2 + (y) ** 2)
    return d


def cal(x, y, z):
    rad90 = radians(90)
    rad30 = radians(30)
    pan = 0.0
    tilt = 0.0
    theta = atan2(y, x)
    pan = theta

    distance = get_distance(x, y)

    # print z - 0.673
    # print distance

    tilt = atan2(z - 0.673, distance)
    # print degrees(tilt)
    tilt = (tilt - rad30)


    pan = checkPanLimitPosition(pan)
    tilt = checkTiltLimitPosition(tilt)

    return pan, -tilt

if __name__ == '__main__':
    rospy.init_node('detect_person_server_real_world')

    rospy.set_param("/head_trace_server/flag", "none")

    rate = rospy.Rate(10.0)

    listener = tf.TransformListener()


    while not rospy.is_shutdown():
        flag = rospy.get_param("/head_trace_server/flag")

        if flag == "human":
            try:
                (trans,rot) = listener.lookupTransform('/base_link', flag, rospy.Time(0))
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                continue

            pan, tilt = cal(trans[0], trans[1], trans[2])
            # print pan, tilt
            head_make(pan, tilt)

        elif flag == "none":
            pass

        else:
            pass

        rate.sleep()
