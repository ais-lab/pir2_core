#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64, Int16, String, Header
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

MAX_LIN_VEL = 0.74
MAX_ANG_VEL = 2.56

MAX_PAN_POS = 1.3
MIN_PAN_POS = -1.3

MAX_TILT_POS = 0.17
MIN_TILT_POS = -0.34

MAX_YAW_POS = 1.3
MIN_YAW_POS = -1.3

LIN_VEL_STEP_SIZE = 0.01
ANG_VEL_STEP_SIZE = 0.1
POS_STEP_SIZE = 0.087
YAW_POS_STEP_SIZE = 0.43

class Publishsers():
    def cmd_make(self, x, ang):
        cmd_msg = Twist()
        ### make ###
        cmd_msg.linear.x = x
        cmd_msg.angular.z = ang
        ### publish ###
        self.cmd_pub.publish(cmd_msg)

    def head_make(self, control_pan_pos, control_tilt_pos, control_yaw_pos):
        head_msg = JointTrajectory()
        jtp_msg = JointTrajectoryPoint()
        head_msg.joint_names = [ "pan_joint", "tilt_joint", "yaw_joint" ]
        head_msg.header.stamp = rospy.Time.now()
        # jtp_msg.points.positions = [control_pan_pos,control_tilt_pos,control_yaw_pos]

        jtp_msg.positions = [control_pan_pos,control_tilt_pos,control_yaw_pos]
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

        self.target_linear_vel   = 0.0
        self.target_angular_vel  = 0.0
        self.control_linear_vel  = 0.0
        self.control_angular_vel = 0.0

        self.target_pan_pos   = 0.0
        self.target_pan_pos  = 0.0
        self.control_pan_pos  = 0.0
        self.control_pan_pos = 0.0

        self.target_tilt_pos   = 0.0
        self.target_tilt_pos  = 0.0
        self.control_tilt_pos  = 0.0
        self.control_tilt_pos = 0.0

        self.target_yaw_pos   = 0.0
        self.target_yaw_pos  = 0.0
        self.control_yaw_pos  = 0.0
        self.control_yaw_pos = 0.0

        self.image_num = 0

    def vels(self, target_linear_vel, target_angular_vel, target_pan_pos, target_tilt_pos, target_yaw_pos):
        return "currently:\tlinear vel %s\t angular vel %s\t pan pos %s\t tilt pos %s\t yaw pos %s\t " % (target_linear_vel,target_angular_vel, target_pan_pos, target_tilt_pos, target_yaw_pos)

    def makeSimpleProfile(self, output, input, slop):
        if input > output:
            output = min( input, output + slop )
        elif input < output:
            output = max( input, output - slop )
        else:
            output = input

        return output

    def constrain(self, input, low, high):
        if input < low:
          input = low
        elif input > high:
          input = high
        else:
          input = input

        return input

    def checkLinearLimitVelocity(self, vel):
        vel = self.constrain(vel, -MAX_LIN_VEL, MAX_LIN_VEL)

        return vel

    def checkAngularLimitVelocity(self, vel):
        vel = self.constrain(vel, -MAX_ANG_VEL, MAX_ANG_VEL)

        return vel

    def checkPanLimitPosition(self, pos):
        pos = self.constrain(pos, MIN_PAN_POS, MAX_PAN_POS)

        return pos

    def checkTiltLimitPosition(self, pos):
        pos = self.constrain(pos, MIN_TILT_POS, MAX_TILT_POS)

        return pos

    def checkYawLimitPosition(self, pos):
        pos = self.constrain(pos, MIN_YAW_POS, MAX_YAW_POS)

        return pos


    def callback(self, msg):
        print msg

        ### /cmd_vel ###
        if msg.axes[7] == 1.0:
            self.target_linear_vel = self.checkLinearLimitVelocity(self.target_linear_vel + LIN_VEL_STEP_SIZE)
        elif msg.axes[7] == -1.0:
            self.target_linear_vel = self.checkLinearLimitVelocity(self.target_linear_vel - LIN_VEL_STEP_SIZE)
        elif msg.axes[6] == 1.0:
            self.target_angular_vel = self.checkAngularLimitVelocity(self.target_angular_vel + ANG_VEL_STEP_SIZE)
        elif msg.axes[6] == -1.0:
            self.target_angular_vel = self.checkAngularLimitVelocity(self.target_angular_vel - ANG_VEL_STEP_SIZE)
        else:
            pass

        ### /cmd_vel = stop ###
        if msg.buttons[9] == 1.0:
            self.target_linear_vel   = 0.0
            self.control_linear_vel  = 0.0
            self.target_angular_vel  = 0.0
            self.control_angular_vel = 0.0

        if msg.buttons[10] == 1.0:
            self.target_pan_pos = 0.0
            self.control_pan_pos = 0.0
            self.target_tilt_pos = 0.0
            self.control_tilt_pos = 0.0
            self.target_yaw_pos = 0.0
            self.control_yaw_pos = 0.0


        if msg.axes[4] > 0.5:
            self.target_tilt_pos = self.checkTiltLimitPosition(self.target_tilt_pos - (POS_STEP_SIZE))
        elif msg.axes[4] <  -0.5:
            self.target_tilt_pos = self.checkTiltLimitPosition(self.target_tilt_pos + (POS_STEP_SIZE))
        else:
            pass

        if msg.axes[3] > 0.5:
            self.target_pan_pos = self.checkPanLimitPosition(self.target_pan_pos + (POS_STEP_SIZE))
        elif msg.axes[3] <  -0.5:
            self.target_pan_pos = self.checkPanLimitPosition(self.target_pan_pos - (POS_STEP_SIZE))
        else:
            pass

        if msg.buttons[4] == 1.0:
            self.target_yaw_pos = self.checkYawLimitPosition(self.target_yaw_pos + YAW_POS_STEP_SIZE)
        elif msg.buttons[5] == 1.0:
            self.target_yaw_pos = self.checkYawLimitPosition(self.target_yaw_pos - YAW_POS_STEP_SIZE)
        else:
            pass

        ### display show  ###
        if msg.buttons[0] == 1.0:
            self.image_num = 1
        elif msg.buttons[1] == 1.0:
            self.image_num = 2
        elif msg.buttons[2] == 1.0:
            self.image_num = 3
        elif msg.buttons[3] == 1.0:
            self.image_num = 4
        else:
            pass


        self.image_make(self.image_num)

        self.control_linear_vel = self.makeSimpleProfile(self.control_linear_vel, self.target_linear_vel, (LIN_VEL_STEP_SIZE/2.0))
        self.control_angular_vel = self.makeSimpleProfile(self.control_angular_vel, self.target_angular_vel, (ANG_VEL_STEP_SIZE/2.0))

        self.cmd_make(self.control_linear_vel, self.control_angular_vel)

        self.control_pan_pos = self.makeSimpleProfile(self.control_pan_pos, self.target_pan_pos, (POS_STEP_SIZE/2.0))
        self.control_tilt_pos = self.makeSimpleProfile(self.control_tilt_pos, self.target_tilt_pos, (POS_STEP_SIZE/2.0))
        self.control_yaw_pos = self.makeSimpleProfile(self.control_yaw_pos, self.target_yaw_pos, (YAW_POS_STEP_SIZE/2.0))

        self.head_make(self.control_pan_pos, self.control_tilt_pos, self.control_yaw_pos)

        # print self.vels(self.target_linear_vel, self.target_angular_vel, self.target_pan_pos, self.target_tilt_pos, self.target_yaw_pos)


if __name__ == '__main__':
    rospy.init_node('joy_control_frame')

    Subscribe = Subscribe()

    rospy.spin()
