import rospy
import psutil
from std_msgs.msg import String
import sys
from subprocess import PIPE, Popen
from threading  import Thread
from os.path import expanduser

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x
ON_POSIX = 'posix' in sys.builtin_module_names

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()
    
def data_collector(process_name, write_to_file, sample_interval, net_interface, machine_name):
    
    if write_to_file:
        home = expanduser("~")
        log_file=open(home+'/chatter.log','w')
    pid_list = psutil.pids();
    my_process = [];
    for p in pid_list:
        try:
            if psutil.Process(p).name() in  process_name:
                my_process.append(psutil.Process(p))
        except psutil.NoSuchProcess:
            pass        
            
            
    if not len(my_process):
        rospy.logerr("no process can be found in the process list")
        self.finish();
    
    pub = rospy.Publisher('chatter', String, queue_size=100)
    
    
    p = Popen(['sudo', 'nethogs', '-t','-d',str(sample_interval), net_interface], stdout=PIPE, bufsize=1000, close_fds=ON_POSIX)
    q = Queue()
    t = Thread(target=enqueue_output, args=(p.stdout, q))
    t.daemon = True  # thread dies with the program
    t.start()    

    while not rospy.is_shutdown():
        try:
        
            bw_lines = []
            queue_size = q.qsize();
            for i in range(queue_size):
                line = q.get_nowait();
                bw_lines.append(line.strip())
        
            for m in my_process:        
                cpu_usage = m.cpu_percent();
            
                rss = m.memory_info().rss;
            
                sent_rate=0;
                rec_rate=0;
                occurance=0;
                for bw in bw_lines:
                    if m.name()in bw:
                        splitted_line=bw.split('\t',3);
                        if((str(m.pid)+"/") in splitted_line[0]):
                            occurance=occurance+1;
                            sent_rate=sent_rate+float(splitted_line[1])
                            rec_rate=rec_rate+float(splitted_line[2]);
                if(occurance!=0):
                    sent_rate=sent_rate/occurance;
                    rec_rate=rec_rate/occurance;         
                          
                to_send_str = " %s %s %s %s %s %s %s" % (rospy.get_time(), m.name(), m.pid, cpu_usage, rss, sent_rate, rec_rate)  
                if(not sample_interval):
                    pub.publish(to_send_str)
                else:
                    log_file.write(to_send_str+"\n")
            
            
            rospy.sleep(sample_interval)
        except:
            pass
        
           
            
 
