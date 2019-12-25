#!/usr/bin/env python
import sys
import os
import rospy
from std_msgs.msg import Int64, Float64, Int16
import time
import numpy as np
import serial
import math
from subprocess import call, Popen
from time import sleep
import rospkg

from pir2_msgs.srv import *
from geometry_msgs.msg import Twist



class TextfileController(object):
    def __init__(self):
        self.rate = rospy.Rate(100) # 100hz
        self.rate_time = 0.01
        self.scan_flag = 0
        self.result = True
        self.motor = rospy.ServiceProxy('/pir2_control/motor', MotorCommand)
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.head = rospy.ServiceProxy('/pir2_control/head', HeadCommand)
        self.nav = rospy.ServiceProxy('/pir2_control/nav', NavCommand)
        self.img_pub = rospy.Publisher('/pir2_image', Int16, queue_size=10)


    def executive_file(self):
        file = rospy.get_param("/textfile_controller/file_name")
        if file != "":
            ### start main controller ###
            instance_name = TextfileController()
            instance_name.textfile_controller()
        else:
            self.shutdown()

    def file_open(self, file_name):
        if file_name is not None:
            path = os.path.join(rospkg.RosPack().get_path('pir2_control')+ '/motion', file_name)
            filepath = os.path.splitext(path)[0] + '.mts'
            file_content = open(filepath)
            print("\n")
            print("*** "+ file_name + ".mts ***")
            print("\n")
            return file_content
        else:
            print("Done")
            self.shutdown()


    def extract_commands(self, text):
        text = text.replace('\n'," ")
        text = text.split(" ")
        return text

    def make_head(self, name, angle, speed):
        req = HeadCommandRequest()
        req.name.data = name
        req.angle.data = angle
        req.speed.data = speed
        result = self.head(req)
        self.result = result.result.data
        return self.result

    def shutdown(self):
        self.cmd_pub.publish(Twist())
        rospy.signal_shutdown("Done")

    def textfile_controller(self):

        file_name = rospy.get_param("/textfile_controller/file_name")
        file_content = self.file_open(file_name)

        ### initial params ###
        rospy.set_param("/textfile_controller/distance", 0.0)
        rospy.set_param("/textfile_controller/file_name", "")
        rospy.set_param("/textfile_controller/detect/file_name", "")

        for texts in file_content:

            command_param_set = self.extract_commands(texts)
            command = command_param_set[0]


            req = MotorCommandRequest()
            if command == "acceleration":
                acc = float(command_param_set[1])
                # acc = acc / 1000

                target_speed = float(command_param_set[2])
                # target_speed = target_speed / 1000

                req.order.data = "a"
                req.acceleration.data = acc
                req.target_speed.data = target_speed

                result = self.motor(req)
                self.result = result.result.data


            #forward
            elif command == "forward":
                speed = float(command_param_set[1])
                # speed = speed / 1000  # convert from mm to m

                distance = float(command_param_set[2])
                # distance = distance / 1000  # convert from mm to m

                req.order.data = "f"
                req.speed.data = speed
                req.distance.data = distance

                result = self.motor(req)
                self.result = result.result.data


            elif command == "rotation":

                omega = float(command_param_set[1])
                angle = float(command_param_set[2])

                relative_angle = angle * 2 * math.pi / 360  # convert from degree to radian

                req.order.data = "r"
                req.omega.data = omega
                req.angle.data = angle

                result = self.motor(req)
                self.result = result.result.data


            elif command == "turning":

                speed = float(command_param_set[1])
                # speed = speed / 1000  #convert from mm/s to m/s

                radius = float(command_param_set[2])
                # radius = radius / 1000   #convert from mm to m

                distance = float(command_param_set[3])
                # distance = distance / 1000  #convert from mm to m

                direction = command_param_set[4]  #'left' is left, 'right' is right

                req.order.data = "t"
                req.speed.data = speed
                req.radius.data = radius
                req.distance.data = distance
                req.direction.data = direction

                result = self.motor(req)
                self.result = result.result.data

            elif command == "pause":
                pause_time = float(command_param_set[1])
                # pause_time = pause_time / 1000  #convert ms to s

                req.order.data = "p"
                req.time.data = pause_time

                result = self.motor(req)
                self.result = result.result.data
                # print("_____ pause ______")


            elif command == "stop":

                req.order.data = "s"

                result = self.motor(req)
                self.result = result.result.data
                # print("===== stop ======")

            elif command == 'slowstop':

                down_acc = float(command_param_set[1])
                # down_acc = down_acc / 1000
                req.order.data = "ss"
                req.acceleration.data = down_acc

                result = self.motor(req)
                self.result = result.result.data
                # print("===== stop =====")



            elif command == 'detect':
                #  distance [m] is from robot to obstacle.
                distance = float(command_param_set[1])
                rospy.set_param("/textfile_controller/distance", distance)
                file = command_param_set[2]
                rospy.set_param("/textfile_controller/detect/file_name", file)

                print ("searching someone within {:.3f}(m)".format(distance))

            elif command == "e":
                file = command_param_set[1]
                rospy.set_param("/textfile_controller/file_name", file)
                break

            elif command == "pan" or command == "tilt" or command == "yaw" or command == "init":
                result = self.make_head(command, float(command_param_set[1]), 0.3)

            elif command == "trace":
                frame = command_param_set[1]
                if frame == "off" or frame == "none":
                    rospy.set_param("/head_trace_server/flag", "none")
                else:
                    rospy.set_param("/head_trace_server/flag", frame)



            elif command == "navigation":
                x = float(command_param_set[1])
                y = float(command_param_set[2])
                req = NavCommandRequest()
                req.goal_position.position.x = x
                req.goal_position.position.y = y
                result = self.nav(req)
                self.result = result.result.data

            elif command == "image":
                image_num = int(command_param_set[1])
                img_msg = Int16()
                img_msg.data = image_num
                self.img_pub.publish(img_msg)


            elif command == "end":
                result = self.make_head("pan", 0.0 ,0.3)
                result = self.make_head("tilt", 0.0, 0.3)
                result = self.make_head("yaw", 0.0, 0.3)
                self.file_open(None)

            elif command == "" or command == "#":
                pass

            else:
                print "" + command + " : type error"

            # print self.result
            if (self.scan_flag == 1 or self.result == False):
                detect_file = rospy.get_param("/textfile_controller/detect/file_name")
                if detect_file != "":
                    rospy.set_param("/textfile_controller/file_name", detect_file)
                    break

            else:
                self.result = True

        self.executive_file()




class Move(TextfileController):
    def __init__(self):
        super(Move, self).__init__()
        self.result_obs_sub = rospy.Subscriber("/search/result", Int64, self.search_callback)
        move2 = TextfileController()
        move2.textfile_controller()

    def search_callback(self, scan_result):
        if scan_result.data == 1:
            self.scan_flag = 1
        else:
            self.scan_flag = 0



def main():
    print "***** Please wait (7 seconds) *****"
    rospy.sleep(7.)
    rospy.init_node('frame_controller', anonymous=True)
    rospy.set_param("/textfile_controller/distance", 0)
    move = Move()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("ShutDown")

if __name__ == '__main__':
    main()
