import rospy
import topic_statistic
import roslib.message
import roslib.scriptutil
import rostopic
import numpy as np
import matplotlib.pyplot as plt



topics_list=[];
time_instance=[];

def callback(data,ts):
    mess_size=len(data._buff)
    curr_rostime = rospy.get_rostime().to_time()
    #rospy.loginfo("%s",curr_rostime)
    if not data._has_header:
        #rospy.logerr('msg does not have header in %s',ts.real_topic)
        mess_delay=-1
    else:
        mess_delay=curr_rostime - msg.header.stamp.to_time()

    if ts.prev_mess_rec_time==0:
        mess_inter_delay=None
        ts.prev_mess_rec_time=curr_rostime
        return
    else:
        mess_inter_delay=curr_rostime-ts.prev_mess_rec_time

    ts.prev_mess_rec_time=curr_rostime
    #rospy.loginfo("%s,%s,%s",mess_size,mess_delay,mess_inter_delay)
    ts.mess_info.append((mess_size,mess_delay,mess_inter_delay))
    return


def draw_graphs():
    global time_instance,fig,ax,er_bar
    time_instance.append(len(time_instance))
    
    for topic in topics_list:
        mess_info=topic.mess_info
        topic.mess_info=[]
        mat=np.array(mess_info)
        mean_vector=mat.mean(0)
        topic.mean_size.append(mean_vector[0])
        topic.mean_delay.append(mean_vector[1])
        topic.mean_inter_delay.append(mean_vector[2])
        rospy.loginfo("topic %s:mean size=%s, mean delay=%s, mean time between packets=%s,packet count=%s",topic.real_topic,mean_vector[0],mean_vector[1],mean_vector[2],len(mess_info))    


    
def data_collector(topic_names):
    global topics_list

    
    for topic_name in topic_names:
        ts=topic_statistic.Topic_Stat(topic_name)
        topics_list.append(ts)
        _, ts.real_topic, _ = rostopic.get_topic_type(topic_name, blocking=True)
        rospy.loginfo("REZA_REAL_TOPIC:%s",ts.real_topic)  
        rospy.Subscriber(ts.real_topic, rospy.AnyMsg, callback,ts)
    while not rospy.is_shutdown():
        rospy.rostime.wallsleep(1.0)
        draw_graphs()
        

        
   
        
           
            
 
