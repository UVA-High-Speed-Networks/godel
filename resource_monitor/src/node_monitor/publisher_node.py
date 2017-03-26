import rospy
import psutil
from std_msgs.msg import String
import sys
from subprocess import PIPE, Popen
from threading  import Thread
from os.path import expanduser
import os

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x
ON_POSIX = 'posix' in sys.builtin_module_names

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    
    out.close()

def reinitialize_process_list(process_name):
    my_process = [];
    pid_list = psutil.pids();
    for p in pid_list:
        try:
            if psutil.Process(p).name() in  process_name:
                my_process.append(psutil.Process(p))
        except psutil.NoSuchProcess:
            pass
    return my_process
def data_collector(process_name, write_to_file, sample_interval, net_interface, machine_name):
    #os.nice(-20)
    process_name=process_name.split(',')
    print process_name
    if write_to_file:
        home = expanduser("~")
        log_file=open(home+'/chatter.log','w')
    my_process=reinitialize_process_list(process_name)
    while(len(my_process)<len(process_name)):
       print "%d Process counts are not equal. Try again later %d"%(len(my_process),len(process_name))
       rospy.sleep(1)
       reinitialize_process_list(process_name)
    
    print "ALL PROCESSES ARE FOUND"   
            
            
    if not len(my_process):
        rospy.logerr("no process can be found in the process list")
        self.finish();
    
    pub = rospy.Publisher('chatter', String, queue_size=100)
    
    
    #p = Popen(['sudo', 'nethogs', '-t','-d',str(sample_interval), net_interface], stdout=PIPE, bufsize=1, close_fds=ON_POSIX)
    #q = Queue()
    #t = Thread(target=enqueue_output, args=(p.stdout, q))
    #t.daemon = True  # thread dies with the program
    #t.start()    

    while not rospy.is_shutdown():
        try:
        
           # bw_lines = []
           # queue_size = q.qsize();
           # for i in range(queue_size):
           #     line = q.get_nowait();
           #     bw_lines.append(line.strip())
                    
            for m in my_process:        
                #print "**%d**%d**%d"%(m.name(),m.pid,len(my_process))
                cpu_usage = m.cpu_percent();
            
                rss = m.memory_info().rss;
            
            #    sent_rate=0;
            #    rec_rate=0;
            #    occurance=0;
                
            #    for bw in bw_lines:
            #        if m.name()in bw:
                        
            #            splitted_line=bw.split('\t',3);
            #            if((str(m.pid)+"/") in splitted_line[0]):
            #                occurance=occurance+1;
            #                sent_rate=sent_rate+float(splitted_line[1])
            #                rec_rate=rec_rate+float(splitted_line[2]);
            #    if(occurance!=0):
            #        sent_rate=sent_rate/occurance;
            #        rec_rate=rec_rate/occurance;         
                          
                to_send_str = " %s %s %s %s %s" % (rospy.get_time(), m.name(), m.pid, cpu_usage, rss)  
                
                if(not write_to_file):
                    pub.publish(to_send_str)
                else:
                    log_file.write(to_send_str+"\n")
            
            
            rospy.sleep(sample_interval)
        except :
            print sys.exc_info()
            my_process=reinitialize_process_list(process_name)
            pass
        
           
            
 
