#!/usr/bin/env python

import rospy
import numpy as np
import math

from sensor_msgs.msg import JointState
from std_msgs.msg import String, Bool, Float64

from pir2_msgs.srv import HeadCommand
from pir2_msgs.srv import HeadCommandResponse


class Publishers():

    def pan_make(self, rad):
        pan_msg = Float64()
        pan_msg = rad
        self.pan_pub.publish(pan_msg)
    def tilt_make(self, rad):
        tilt_msg = Float64()
        tilt_msg = rad
        self.tilt_pub.publish(tilt_msg)
    def yaw_make(self, rad):
        yaw_msg = Float64()
        yaw_msg = rad
        self.yaw_pub.publish(yaw_msg)

class Subscribe(Publishers):
    def __init__(self):
        self.pan_rad = 0.0
        self.tilt_rad = 0.0
        self.yaw_rad = 0.0

        self.offset = 0.052 #3 degree

        # Declaration Publisher
        self.pan_pub = rospy.Publisher('/pir2/pan_controller/command', Float64, queue_size=100)
        self.tilt_pub = rospy.Publisher('/pir2/tilt_controller/command', Float64, queue_size=100)
        self.yaw_pub = rospy.Publisher('/pir2/yaw_controller/command', Float64, queue_size=100)

        # Declaration Subscriber
        self.jsp_sub = rospy.Subscriber('/pir2/joint_states', JointState, self.jsp_callback)

        # Declaration Service Server
        self.server = rospy.Service("/pir2_control/head", HeadCommand, self.service_callback)

    ### callback function for amcl node (pose) ###
    def jsp_callback(self, msg):
        self.pan_rad = msg.position[0]
        self.tilt_rad = msg.position[1]
        self.yaw_rad = msg.position[2]

    def service_callback(self, req):
        name = str(req.name.data)
        angle = float(req.angle.data)

        target_rad = math.radians(angle)

        if name == "pan":
            self.pan_make(target_rad)
            print "Pan moving .. "
            while True:
                # print "*"
                if (self.pan_rad > target_rad - self.offset) and (self.pan_rad < target_rad + self.offset):
                    break
        elif name == "tilt":
            self.tilt_make(target_rad)
            print "Tilt moving .. "
            while True:
                # print "*"
                if (self.tilt_rad > target_rad - self.offset) and (self.tilt_rad < target_rad + self.offset):
                    break
        elif name == "yaw":
            self.yaw_make(target_rad)
            print "Yaw moving .. "
            while True:
                # print "*"
                if (self.yaw_rad > target_rad - self.offset) and (self.yaw_rad < target_rad + self.offset):
                    break
        else:
            pass

        result = Bool()
        result.data = True
        return HeadCommandResponse(result)

if __name__ == '__main__':
    rospy.init_node('head_service_server')

    Subscribe = Subscribe()

    rospy.spin()
