#!/usr/bin/env python

import rospy
import numpy as np
import math

from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String, Bool

from actionlib_msgs.msg import GoalStatusArray

from pir2_msgs.srv import NavCommand
from pir2_msgs.srv import NavCommandResponse


class Publishers():

    def make_goal_pub(self, x, y):
        goal_msg = PoseStamped()
        goal_msg.pose.position.x = x
        goal_msg.pose.position.y = y
        goal_msg.pose.orientation.w = 1.0
        goal_msg.header.frame_id = "base_footprint"
        self.goal_pub.publish(goal_msg)



class Subscribe(Publishers):
    def __init__(self):
        self.exit = 0

        # Declaration Publisher
        self.goal_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=100)

        # Declaration Subscriber
        self.nav_sub = rospy.Subscriber('/move_base/status', GoalStatusArray, self.nav_callback)

        # Declaration Service Server
        self.server = rospy.Service("/pir2_control/nav", NavCommand, self.service_callback)

    ### callback function for amcl node (pose) ###
    def nav_callback(self, msg):
        if msg.status_list:
            status_id = msg.status_list[0].status

            if status_id == 0 or status_id == 3:
                self.exit = 1




    def service_callback(self, req):
        x = req.goal_position.position.x
        y = req.goal_position.position.y
        self.make_goal_pub(x,y)
        self.exit = 0

        print "Navigation .. "
        while True:
            print "*"
            if self.exit == 1:
                break
        print ("finish: navigation {0:4.0f}(m) {1:4.0f}(m)".format(x,y))

        result = Bool()
        result.data = True
        return NavCommandResponse(result)

if __name__ == '__main__':
    rospy.init_node('navigation_service_server')

    Subscribe = Subscribe()

    rospy.spin()
