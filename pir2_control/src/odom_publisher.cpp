#include "nav_msgs/Odometry.h"
#include "sensor_msgs/JointState.h"
#include "tf/transform_broadcaster.h"
#include "ros/ros.h"
#include "math.h"


double delta_x = 0;
double delta_y = 0;
double delta_left = 0;
double delta_right = 0;
double fi = 0;
double current_fi = 0;
double last_x = 0;
double last_y = 0;
double current_left, current_right;
double last_left = 0;
double last_right = 0;

// double delta_s = 0;
// double theta = 0;
// double delta_theta = 0;
double last_theta = 0;


void OdomCallback(const sensor_msgs::JointState::ConstPtr& msg)
{

  current_left = msg->position[0];  //wheel_left_joint
  current_right = msg->position[1];  //wheel_right_joint

}


int main (int argc, char** argv)
{
    ros::init(argc, argv, "odom_publisher");

    ros::NodeHandle n;
    ros::Publisher odom_pub;
    ros::Subscriber odom_sub;

    odom_sub = n.subscribe("/joint_states",1000,OdomCallback);



    odom_pub = n.advertise<nav_msgs::Odometry>("odom",100);
    tf::TransformBroadcaster odom_broadcaster;

    ros::Rate r(50.0);

    ros::Time current_time, last_time;
    current_time = ros::Time::now();
    last_time = ros::Time::now();

    double WHEEL_RADIUS = 0.105;
    double WHEELS_DISTANCE = 0.53;
    double x = 0;
    double y = 0;
    double th = 0;
    // double vx = 0;
    // double vy = 0;
    // double vth = 0;

    int count = 0;
    while(n.ok())
    {
          ros::spinOnce();  //sub joint_states
          current_time = ros::Time::now();
          double delta_left = delta_right = 0.0;
          double delta_s = 0.0;
          double delta_theta = 0.0;
          double theta = 0.0;
          double vx = 0.0;
          double vth = 0.0;

          delta_left = current_left - last_left;
          delta_right = current_right - last_right;
          last_left = current_left;
          last_right = current_right;
          if (std::isnan(delta_left))
            delta_left = 0.0;

          if (std::isnan(delta_right))
            delta_right = 0.0;


          delta_s = WHEEL_RADIUS * (delta_right + delta_left) / 2.0;
          theta = WHEEL_RADIUS * (delta_right - delta_left) / WHEELS_DISTANCE;
          // ROS_INFO("theta %f", theta);

          delta_theta = theta;
          // ROS_INFO("theta %f", delta_theta);

          double dt = (current_time - last_time).toSec();
          if (dt == 0)
            return false;
          // if (dt < 0.00001)
          //   return false; // Interval too small to integrate with

          x += delta_s * cos(th + (delta_theta / 2.0));
          y += delta_s * sin(th + (delta_theta / 2.0));
          th += delta_theta;
          // ROS_INFO("yaw %f", th);

          ///////////////////////////////////////////////
          // double dt = (current_time - last_time).toSec();
          // if (dt == 0)
          //   return false;
          // x += (vx * cos(th)) * dt;
          // y += (vx * sin(th)) * dt;
          // th += vth * dt;
          ///////////////////////////////////////////////


          vx = delta_s / dt;
          vth = delta_theta / dt;

          //since all odometry is 6DOF we'll need a quaternion created from yaw
          geometry_msgs::Quaternion odom_quat = tf::createQuaternionMsgFromYaw(th);

          geometry_msgs::TransformStamped odom_trans;
          odom_trans.header.stamp = current_time;
          odom_trans.header.frame_id = "odom";
          odom_trans.child_frame_id = "base_footprint";

          odom_trans.transform.translation.x = x;
          odom_trans.transform.translation.y = y;
          odom_trans.transform.translation.z = 0.0;
          odom_trans.transform.rotation = odom_quat;

          //send the transform
          odom_broadcaster.sendTransform(odom_trans);

          //next, we'll publish the odometry message over ROS
          nav_msgs::Odometry odom;
          odom.header.stamp = current_time;
          odom.header.frame_id = "odom";

          //set the position
          odom.pose.pose.position.x = x;
          odom.pose.pose.position.y = y;
          odom.pose.pose.position.z = 0.0;
          odom.pose.pose.orientation = odom_quat;

          //set the velocity
          odom.child_frame_id = "base_footprint";
          odom.twist.twist.linear.x = vx;
          odom.twist.twist.linear.y = 0.0;
          odom.twist.twist.angular.z = vth;

          //publish the message
          odom_pub.publish(odom);

          last_time = current_time;
          last_theta = theta;

          r.sleep();
          count++;
    }

 return 0;
}
