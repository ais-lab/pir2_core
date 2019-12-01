#!/usr/bin/env python

import rospy, math
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64, Int16, String, Header
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint


class Publishsers():
    def cmd_make(self, x, ang):
        cmd_msg = Twist()
        ### make ###
        cmd_msg.linear.x = x
        cmd_msg.angular.z = ang
        ### publish ###
        self.cmd_pub.publish(cmd_msg)

    def head_make(self, control_pan_pos):
        head_msg = JointTrajectory()
        jtp_msg = JointTrajectoryPoint()
        head_msg.joint_names = [ "pan_joint", "tilt_joint", "yaw_joint" ]
        head_msg.header.stamp = rospy.Time.now()
        # jtp_msg.points.positions = [control_pan_pos,control_tilt_pos,control_yaw_pos]

        jtp_msg.positions = [control_pan_pos, math.radians(18), 0.0]
        jtp_msg.time_from_start = rospy.Duration.from_sec(0.00000002)

        head_msg.points.append(jtp_msg)
        self.head_pub.publish(head_msg)

    def image_make(self, data):
        image_msg = Int16()
        image_msg.data = data
        self.image_pub.publish(image_msg)

class Subscribe(Publishsers):
    def __init__(self):

        self.cmd_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        self.head_pub = rospy.Publisher('/dynamixel_workbench_head/joint_trajectory', JointTrajectory, queue_size=100)
        self.image_pub = rospy.Publisher('/pir2_image', Int16, queue_size=10)

        self.ptm_sub = rospy.Subscriber('joy', Joy, self.callback)

        self.image_num = 0


    def callback(self, msg):
        # print msg


        ### display show  ###
        if msg.buttons[0] == 1.0:
            self.image_num = 6
        elif msg.buttons[1] == 1.0:
            self.image_num = 1
        else:
            pass

        if msg.buttons[2] == 1.0:
            self.target_pan_pos = 0.0
            self.head_make(self.target_pan_pos)
        elif msg.buttons[3] == 1.0:
            self.target_pan_pos = math.radians(30)
            self.head_make(self.target_pan_pos)
        else:
            pass

        if msg.axes[6] == 1.0:
            self.image_num = 2
        elif msg.axes[6] == -1.0:
            self.image_num = 3
        else:
            pass

        if msg.axes[7] == 1.0:
            self.image_num = 5
        elif msg.axes[7] == -1.0:
            self.image_num = 4
        else:
            pass

        if msg.buttons[7] == 1.0:
            self.cmd_make(0.0, 0.0)
        else:
            pass


        self.image_make(self.image_num)



        # print self.vels(self.target_linear_vel, self.target_angular_vel, self.target_pan_pos, self.target_tilt_pos, self.target_yaw_pos)


if __name__ == '__main__':
    rospy.init_node('joy_control_frame_for_experiment')

    Subscribe = Subscribe()

    rospy.spin()