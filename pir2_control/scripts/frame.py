#!/usr/bin/env python
import sys
import rospy
import tf
from std_msgs.msg import Float64, Int16
import time
from pir2_msgs.srv import *
from geometry_msgs.msg import Twist

class Control():
    def __init__(self):

        rospy.init_node('new_exp_control', anonymous=True)

        self.motor = rospy.ServiceProxy('/pir2_control/motor', MotorCommand)
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.head = rospy.ServiceProxy('/pir2_control/head', HeadCommand)
        self.nav = rospy.ServiceProxy('/pir2_control/nav', NavCommand)
        self.img_pub = rospy.Publisher('/pir2_image', Int16, queue_size=10)


        self.tf_listener = tf.TransformListener()
        self.odom_frame = '/odom'

        self.rate = rospy.Rate(10)

        try:
            self.tf_listener.waitForTransform(self.odom_frame, '/base_footprint', rospy.Time(), rospy.Duration(5.0))
            self.base_frame = 'base_footprint'
        except (tf.Exception, tf.ConnectivityException, tf.LookupException):
            try:
                self.tf_listener.waitForTransform(self.odom_frame, 'base_link', rospy.Time(), rospy.Duration(1.0))
                self.base_frame = 'base_link'
            except(tf.Exception, tf.ConnectivityException, tf.LookupException):
                rospy.loginfo("Cannot find transform between /odom and /base_link or /base_footprint")
                rospy.signal_shutdown("tf Exception")

        while True:
            a = input("Input exp_num: >>")

            if a == 52:
                self.img_pub.publish(1)
                rospy.set_param("/head_trace_server/flag", "obstacle")
                relative_angle = 170 * 2 * self.PI / 360

                result.data = self.rotation(omega, relative_angle, 5)
                self.motor_server("a",300,0,0,500)
                self.motor_server("f",0,300,600,0)
                self.motor_server("ss",200,0,0,0)

            elif a == 53:
                self.img_pub.publish(1)
                rospy.set_param("/head_trace_server/flag", "obstacle")
                relative_angle = 170 * 2 * self.PI / 360

                result.data = self.rotation(omega, relative_angle, 5)
                self.motor_server("a",300,0,0,500)
                self.motor_server("f",0,300,600,0)
                self.motor_server("ss",200,0,0,0)

            else:
                pass

    def get_odom(self):
        try:
            (trans, rot) = self.tf_listener.lookupTransform(self.odom_frame, self.base_frame, rospy.Time(0))
        except (tf.Exception, tf.ConnectivityException, tf.LookupException):
            rospy.loginfo("TF Exception")
            return
        return (Point(*trans), self.quat_to_angle(Quaternion(*rot)))

    def quat_to_angle(self, quat):
        rot = PyKDL.Rotation.Quaternion(quat.x, quat.y, quat.z, quat.w)
        return rot.GetRPY()[2]

    def normalize_angle(self, angle):
        res = angle
        while res > pi:
            res -= 2.0 * pi
        while res < -pi:
            res += 2.0 * pi
        return res

    def rotation(self, omega, relative_angle, delay_time):
        angular_tolerance = radians(2.5)

        (prev_position, prev_rotation) = self.get_odom()
        last_angle = prev_rotation
        turn_angle = 0.0

        if omega > 0:
            target_left = - (omega * self.HALF_WHEEL_SEPARATION)
            target_right = omega * self.HALF_WHEEL_SEPARATION
        else:
            target_left = - (omega * self.HALF_WHEEL_SEPARATION)
            target_right = omega * self.HALF_WHEEL_SEPARATION

        target_left, target_right = self.constrain(target_left, target_right, self.MIN_WHEEL_VELOCITY, self.MAX_WHEEL_VELOCITY)
        self.spt_pub(target_left, target_right)

        while( abs(turn_angle + angular_tolerance) < abs(relative_angle)):
            (position, rotation) = self.get_odom()
            delta_angle = self.normalize_angle(rotation - last_angle)
            turn_angle += delta_angle
            last_angle = rotation
            time += 0.1
            if time > delay_time:
                rospy.set_param("/head_trace_server/flag", "none")
                self.head_make("pan_joint", 0.0)

            self.rate.sleep()

        self.spt_pub(0.0, 0.0)

        print ("finish: rotation {0}(rad/s) {1}(radian)".format(omega,relative_angle))
        return True

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

    def motor_server(self, order, acceleration, speed, distance, target_speed):
        rospy.wait_for_service('/pir2_control/motor')
        try:
            req = MotorCommandRequest()
            call = rospy.ServiceProxy('/pir2_control/motor', MotorCommand)
            req.order.data = order
            req.acceleration.data = acceleration
            req.speed.data = speed
            req.distance.data = distance
            req.target_speed.data = target_speed
            resp1 = call(req)
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e




if __name__ == '__main__':
    Control()
