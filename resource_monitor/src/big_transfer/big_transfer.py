#!/usr/bin/env python

from resource_monitor.msg import ByteArray
import rospy

rospy.init_node('transfer_node')
mypub = rospy.Publisher('big_transfer', ByteArray,queue_size=10)
msg_to_send = ByteArray()
msg_to_send.some_floats=range(100000000)


while True:
    mypub.publish(msg_to_send)
    print "sent"
    rospy.sleep(2)

