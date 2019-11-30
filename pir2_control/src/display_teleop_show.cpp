#include <stdio.h>
#include <string>
#include <iostream>
#include <ros/ros.h>
#include <ros/package.h>
#include <std_msgs/Int16.h>
#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <chrono>
#include <thread>

int image_num = 0;

void Callback(const std_msgs::Int16& msg)
{
  // std::cout << msg.data << std::endl;
  image_num = msg.data;

}
int main(int argc, char **argv)
{

  ros::init(argc, argv, "display_teleop_show_node");

  ros::NodeHandle n;

  ros::Subscriber sub = n.subscribe("/pir2_image", 1000, &Callback);

  ros::Rate rate(20);

  std::string file_dir = ros::package::getPath("pir2_control") + "/images/";
  int ColumnOfNewImage = 1024;
  int RowsOfNewImage = 768;
  std::string file_name = "0";

  cv::Mat source_img = cv::Mat::zeros(ColumnOfNewImage, RowsOfNewImage, CV_8UC3);

  while(ros::ok()){
    ros::spinOnce();

    if (image_num > 0 && image_num < 10) {
      // std::cout << image_num << std::endl;
      ///// get image and resize projectr size
      file_name = std::to_string(image_num);
      std::string input_file_path = file_dir + file_name + ".png";
      // std::cout << input_file_path << std::endl;

      source_img = cv::imread(input_file_path, cv::IMREAD_UNCHANGED);

    } else {

      source_img = cv::Mat::zeros(RowsOfNewImage, ColumnOfNewImage, CV_8UC3);

    }

    resize(source_img, source_img, cv::Size(1366,768));


    cv::namedWindow( "image_screen" ,CV_WINDOW_NORMAL);
    cv::setWindowProperty("image_screen",CV_WND_PROP_FULLSCREEN,CV_WINDOW_FULLSCREEN);

    cv::imshow("image_screen", source_img);
    cv::waitKey(1);

    rate.sleep();
    }


  return 0;
}
