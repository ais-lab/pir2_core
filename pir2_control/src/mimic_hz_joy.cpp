#include <ros/ros.h>
#include <std_msgs/String.h>
#include <sensor_msgs/Joy.h>

ros::Publisher filtered_pub;

int number = 0;
float HZ = 1;

sensor_msgs::Joy joy_msg;
void chatterCallback(const sensor_msgs::Joy::ConstPtr& msg)
{
  // filtered_pub.publish(msg);
  joy_msg = *msg;
}

int main(int argc, char** argv)
{
  ros::init(argc, argv, "mimic_hz_joy_node");
  ros::NodeHandle n;
  ros::NodeHandle pn("~");
  pn.getParam("number", number);
  pn.getParam("HZ", HZ);
  filtered_pub = n.advertise<sensor_msgs::Joy>("/filtered_joy", 1000);
  ros::Subscriber chatter_sub = n.subscribe("/joy", 1000, chatterCallback);
  joy_msg = sensor_msgs::Joy();

  if (HZ > 0)
  {
    ros::Rate loop_rate(10);
    while (ros::ok())
    {
      filtered_pub.publish(joy_msg);
      ros::spinOnce();
      loop_rate.sleep();
    }
  }
  else
    ros::spin();
  return 0;
}
