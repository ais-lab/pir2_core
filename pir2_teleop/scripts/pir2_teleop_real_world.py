#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
from dynamixel_workbench_msgs.srv import DynamixelCommand, DynamixelCommandRequest
import sys, select, os
if os.name == 'nt':
  import msvcrt
else:
  import tty, termios

MAX_LIN_VEL = 0.74
MAX_ANG_VEL = 2.56

MAX_PAN_POS = 4000
MIN_PAN_POS = 0

MAX_TILT_POS = 4000
MIN_TILT_POS = 1900

MAX_YAW_POS = 4000
MIN_YAW_POS = 0

LIN_VEL_STEP_SIZE = 0.01
ANG_VEL_STEP_SIZE = 0.1
POS_STEP_SIZE = 400

msg = """
---------------------------
Moving around:
        w            y   u   i
   a    s    d       h   j   k
        x                m

w/x : increase/decrease linear velocity ( ~ 0.74)
a/d : increase/decrease angular velocity ( ~ 2.84)
y/i : increase/decrease angular position (-1.3 ~ 1.3)
u/m : increase/decrease angular position (-0.34 ~ 0.17)
h/k : increase/decrease angular position (-1.3 ~ 1.3)

space key, s, j : force stop

CTRL-C to quit
"""

e = """
Communications Failed
"""

def getKey():
    if os.name == 'nt':
      return msvcrt.getch()

    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def vels(target_linear_vel, target_angular_vel, target_pan_pos, target_tilt_pos, target_yaw_pos):
    return "currently:\tlinear vel %s\t angular vel %s\t pan pos %s\t tilt pos %s\t yaw pos %s\t " % (target_linear_vel,target_angular_vel, target_pan_pos, target_tilt_pos, target_yaw_pos)

def makeSimpleProfile(output, input, slop):
    if input > output:
        output = min( input, output + slop )
    elif input < output:
        output = max( input, output - slop )
    else:
        output = input

    return output

def constrain(input, low, high):
    if input < low:
      input = low
    elif input > high:
      input = high
    else:
      input = input

    return input

def checkLinearLimitVelocity(vel):
    vel = constrain(vel, -MAX_LIN_VEL, MAX_LIN_VEL)

    return vel

def checkAngularLimitVelocity(vel):
    vel = constrain(vel, -MAX_ANG_VEL, MAX_ANG_VEL)

    return vel

def checkPanLimitPosition(pos):
    pos = constrain(pos, MIN_PAN_POS, MAX_PAN_POS)

    return pos

def checkTiltLimitPosition(pos):
    pos = constrain(pos, MIN_TILT_POS, MAX_TILT_POS)

    return pos

def checkYawLimitPosition(pos):
    pos = constrain(pos, MIN_YAW_POS, MAX_YAW_POS)

    return pos


if __name__=="__main__":
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('pir2_teleop')
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    dxl_srv = rospy.ServiceProxy('/dynamixel_workbench/dynamixel_command', DynamixelCommand)


    status = 0
    target_linear_vel   = 0.0
    target_angular_vel  = 0.0
    control_linear_vel  = 0.0
    control_angular_vel = 0.0

    target_pan_pos   = 2000
    target_pan_pos  = 2000
    control_pan_pos  = 2000
    control_pan_pos = 2000

    target_tilt_pos   = 2000
    target_tilt_pos  = 2000
    control_tilt_pos  = 2000
    control_tilt_pos = 2000

    target_yaw_pos   = 2000
    target_yaw_pos  = 2000
    control_yaw_pos  = 2000
    control_yaw_pos = 2000

    try:
        print msg
        while(1):
            key = getKey()
            if key == 'w' :
                target_linear_vel = checkLinearLimitVelocity(target_linear_vel + LIN_VEL_STEP_SIZE)
                status = status + 1
                print vels(target_linear_vel,target_angular_vel, target_pan_pos, target_tilt_pos, target_yaw_pos)
            elif key == 'x' :
                target_linear_vel = checkLinearLimitVelocity(target_linear_vel - LIN_VEL_STEP_SIZE)
                status = status + 1
                print vels(target_linear_vel,target_angular_vel, target_pan_pos, target_tilt_pos, target_yaw_pos)
            elif key == 'a' :
                target_angular_vel = checkAngularLimitVelocity(target_angular_vel + ANG_VEL_STEP_SIZE)
                status = status + 1
                print vels(target_linear_vel,target_angular_vel, target_pan_pos, target_tilt_pos, target_yaw_pos)
            elif key == 'd' :
                target_angular_vel = checkAngularLimitVelocity(target_angular_vel - ANG_VEL_STEP_SIZE)
                status = status + 1
                print vels(target_linear_vel,target_angular_vel, target_pan_pos, target_tilt_pos, target_yaw_pos)
            elif key == 'y' :
                target_yaw_pos = checkYawLimitPosition(target_yaw_pos - POS_STEP_SIZE)
                status = status + 1
                print vels(target_linear_vel,target_angular_vel, target_pan_pos, target_tilt_pos, target_yaw_pos)
            elif key == 'i' :
                target_yaw_pos = checkYawLimitPosition(target_yaw_pos + POS_STEP_SIZE)
                status = status + 1
                print vels(target_linear_vel,target_angular_vel, target_pan_pos, target_tilt_pos, target_yaw_pos)
            elif key == 'u' :
                target_tilt_pos = checkTiltLimitPosition(target_tilt_pos - POS_STEP_SIZE)
                status = status + 1
                print vels(target_linear_vel,target_angular_vel, target_pan_pos, target_tilt_pos, target_yaw_pos)
            elif key == 'm' :
                target_tilt_pos = checkTiltLimitPosition(target_tilt_pos + POS_STEP_SIZE)
                status = status + 1
                print vels(target_linear_vel,target_angular_vel, target_pan_pos, target_tilt_pos, target_yaw_pos)
            elif key == 'h' :
                target_pan_pos = checkYawLimitPosition(target_pan_pos - POS_STEP_SIZE)
                status = status + 1
                print vels(target_linear_vel,target_angular_vel, target_pan_pos, target_tilt_pos, target_yaw_pos)
            elif key == 'k' :
                target_pan_pos = checkYawLimitPosition(target_pan_pos + POS_STEP_SIZE)
                status = status + 1
                print vels(target_linear_vel,target_angular_vel, target_pan_pos, target_tilt_pos, target_yaw_pos)
            elif key == 'j':
                target_linear_vel   = 0.0
                control_linear_vel  = 0.0
                target_angular_vel  = 0.0
                control_angular_vel = 0.0
                target_pan_pos = 2000
                control_pan_pos = 2000
                target_tilt_pos = 2000
                control_tilt_pos = 2000
                target_yaw_pos = 2000
                control_yaw_pos = 2000
                print vels(target_linear_vel,target_angular_vel, target_pan_pos, target_tilt_pos, target_yaw_pos)
            elif key == ' ' or key == 's' :
                target_linear_vel   = 0.0
                control_linear_vel  = 0.0
                target_angular_vel  = 0.0
                control_angular_vel = 0.0
                target_pan_pos = 2000
                control_pan_pos = 2000
                target_tilt_pos = 2000
                control_tilt_pos = 2000
                target_yaw_pos = 2000
                control_yaw_pos = 2000
                print vels(target_linear_vel,target_angular_vel, target_pan_pos, target_tilt_pos, target_yaw_pos)
            else:
                if (key == '\x03'):
                    break

            if status == 20 :
                print msg
                status = 0

            twist = Twist()

            pan_req = DynamixelCommandRequest()
            tilt_req = DynamixelCommandRequest()
            yaw_req = DynamixelCommandRequest()

            pan_req.id = 3
            tilt_req.id = 4
            yaw_req.id = 5

            pan_req.addr_name = "Goal_Position"
            tilt_req.addr_name = "Goal_Position"
            yaw_req.addr_name = "Goal_Position"

            control_linear_vel = makeSimpleProfile(control_linear_vel, target_linear_vel, (LIN_VEL_STEP_SIZE/2.0))
            twist.linear.x = control_linear_vel; twist.linear.y = 0.0; twist.linear.z = 0.0

            control_angular_vel = makeSimpleProfile(control_angular_vel, target_angular_vel, (ANG_VEL_STEP_SIZE/2.0))
            twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = control_angular_vel

            control_pan_pos = makeSimpleProfile(control_pan_pos, target_pan_pos, (POS_STEP_SIZE/2.0))
            pan_req.value = control_pan_pos

            control_tilt_pos = makeSimpleProfile(control_tilt_pos, target_tilt_pos, (POS_STEP_SIZE/2.0))
            tilt_req.value = control_tilt_pos

            control_yaw_pos = makeSimpleProfile(control_yaw_pos, target_yaw_pos, (POS_STEP_SIZE/2.0))
            yaw_req.value = control_yaw_pos

            pub.publish(twist)
            result = dxl_srv(pan_req)
            result = dxl_srv(tilt_req)
            result = dxl_srv(yaw_req)



    except:
        print e

    finally:
        twist = Twist()
        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        pub.publish(twist)

    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
