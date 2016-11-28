
class Topic_Stat:

    def __init__(self,topic_name):
        self.topic_name=topic_name
        self.mess_info=[]
        self.prev_mess_rec_time=0
        self.mean_size=[]
        self.mean_delay=[]
        self.mean_inter_delay=[]
