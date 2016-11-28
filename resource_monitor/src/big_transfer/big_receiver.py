#!/usr/bin/env python

from resource_monitor.msg import ByteArray
import rospy

def mytopic_callback(msg):
   print "received"

rospy.init_node('receiver_node')
mysub = rospy.Subscriber('big_transfer', ByteArray, mytopic_callback)
rospy.spin()

