#!/usr/bin/env python

import rospy
import numpy as np
import math

from sensor_msgs.msg import JointState
from std_msgs.msg import String, Bool, Float64
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

from pir2_msgs.srv import HeadCommand
from pir2_msgs.srv import HeadCommandResponse

MAX_PAN_POS = 3.14
MIN_PAN_POS = -3.14

MAX_TILT_POS = 0.30
MIN_TILT_POS = -0.34

MAX_YAW_POS = 3.14
MIN_YAW_POS = -3.14

class Publishers():

    def init_make(self):
        head_msg = JointTrajectory()
        jtp_msg = JointTrajectoryPoint()
        head_msg.joint_names = [ "pan_joint", "tilt_joint", "yaw_joint" ]
        head_msg.header.stamp = rospy.Time.now()
        # jtp_msg.points.positions = [control_pan_pos,control_tilt_pos,control_yaw_pos]

        jtp_msg.positions = [0.0,0.0,0.0]
        jtp_msg.time_from_start = rospy.Duration.from_sec(0.00000002)

        head_msg.points.append(jtp_msg)
        self.head_pub.publish(head_msg)


    def head_make(self,joint_name, rad):
        head_msg = JointTrajectory()
        jtp_msg = JointTrajectoryPoint()
        head_msg.joint_names = [joint_name]
        head_msg.header.stamp = rospy.Time.now()
        # jtp_msg.points.positions = [control_pan_pos,control_tilt_pos,control_yaw_pos]

        jtp_msg.positions = [rad]
        jtp_msg.time_from_start = rospy.Duration.from_sec(0.00000002)

        head_msg.points.append(jtp_msg)
        self.head_pub.publish(head_msg)


class Subscribe(Publishers):
    def __init__(self):
        self.pan_rad = 0.0
        self.tilt_rad = 0.0
        self.yaw_rad = 0.0

        self.offset = 0.08 #5 degree

        # Declaration Publisher
        self.head_pub = rospy.Publisher('/dynamixel_workbench_head/joint_trajectory', JointTrajectory, queue_size=100)
        # Declaration Subscriber
        self.jsp_sub = rospy.Subscriber('/dynamixel_workbench_head/joint_states', JointState, self.jsp_callback)

        # Declaration Service Server
        self.server = rospy.Service("/pir2_control/head", HeadCommand, self.service_callback)

        self.init_make()

    ### callback function for amcl node (pose) ###
    def jsp_callback(self, msg):
        self.pan_rad = msg.position[0]
        self.tilt_rad = msg.position[1]
        self.yaw_rad = msg.position[2]

    def service_callback(self, req):
        name = str(req.name.data)
        angle = float(req.angle.data)

        target_rad = math.radians(angle)
        joint_name = ""

        if name == "pan":
            joint_name = "pan_joint"
            target_rad = self.checkPanLimitPosition(target_rad)
            self.head_make(joint_name, target_rad)
            print "Pan moving .. "
            while True:
                # print "*"
                if (self.pan_rad > target_rad - self.offset) and (self.pan_rad < target_rad + self.offset):
                    break
        elif name == "tilt":
            joint_name = "tilt_joint"
            target_rad = self.checkTiltLimitPosition(target_rad)
            self.head_make(joint_name, target_rad)
            print "Tilt moving .. "
            while True:
                # print "*"
                if (self.tilt_rad > target_rad - self.offset) and (self.tilt_rad < target_rad + self.offset):
                    break
        elif name == "yaw":
            joint_name = "yaw_joint"
            target_rad = self.checkYawLimitPosition(target_rad)
            self.head_make(joint_name, target_rad)
            print "Yaw moving .. "
            while True:
                # print "*"
                if (self.yaw_rad > target_rad - self.offset) and (self.yaw_rad < target_rad + self.offset):
                    break

        elif name == "init":
            self.init()
            rospy.sleep(2)
        else:
            pass

        result = Bool()
        result.data = True
        return HeadCommandResponse(result)

    def checkPanLimitPosition(self, pos):
        pos = self.constrain(pos, MIN_PAN_POS, MAX_PAN_POS)

        return pos

    def checkTiltLimitPosition(self, pos):
        pos = self.constrain(pos, MIN_TILT_POS, MAX_TILT_POS)

        return pos

    def checkYawLimitPosition(self, pos):
        pos = self.constrain(pos, MIN_YAW_POS, MAX_YAW_POS)

        return pos

    def constrain(self, input, low, high):
        if input < low:
          input = low
        elif input > high:
          input = high
        else:
          input = input

        return input
if __name__ == '__main__':
    rospy.init_node('head_service_server')

    Subscribe = Subscribe()

    rospy.spin()
