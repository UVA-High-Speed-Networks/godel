#include<ros/ros.h>
#include""

bool offset_polygons_cb(OffsetPolygonRequest& req, OffsetPolygonResponse& res)
{

}

int main(int argc, char** argv)
{
  ros::init(argc, argv, "single_frame_publisher_node");
  ros::NodeHandle nh;
  ros::ServiceServer service = nh.advertiseService("single_frame_publisher", offset_polygons_cb);
  ROS_INFO("%s ready to service requests.", service.getService().c_str());
  ros::spin();
  return 0;
}



