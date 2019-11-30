#include <ros/ros.h>
#include <tf/transform_broadcaster.h>
#include <geometry_msgs/Pose.h>
#include <geometry_msgs/PoseStamped.h>
#include<iostream>
#include<string>
using namespace std;

float pos_x = 0.0;
float pos_y = 0.0;
float pos_z = 0.0;
string frame_id = "";

int main(int argc, char** argv)
{
  ros::init(argc, argv, "goal_tf_publisher");

	ros::NodeHandle n("~");

	ros::Rate rate(10.0);

	static tf::TransformBroadcaster br;
  tf::Transform transform;

	n.getParam("pos_x", pos_x);
	n.getParam("pos_y", pos_y);
	n.getParam("pos_z", pos_z);
	n.getParam("frame_name", frame_id);

	while(ros::ok())
	{

		transform.setOrigin( tf::Vector3(pos_x, pos_y, pos_z) );
	  transform.setRotation( tf::Quaternion(0.0, 0.0, 0.0, 1.0));
	  br.sendTransform(tf::StampedTransform(transform, ros::Time::now(), "map", frame_id));

		rate.sleep();
	}
}
