import os
import argparse
from argparse import ArgumentParser
import time
import datetime
import json
import libtmux


VERSION=1.0

class Automation():

    def __init__(self, args):
        self.args = args
        self.output_dir=self.args.output_dir
        self.spdk_work_dir=self.args.spdk_work_dir
        self.test_op=self.args.test_op
        self.iteration=self.args.iteration
        self.summary_name=self.args.summary_name
        self.log_dir=""
        self.command=""
        self.instance="Multi"
        self.spdk_top=self.args.spdk_top

        self.thread=self.args.thread
        self.time=self.args.time
        self.size=self.args.size
        self.cpumask=self.args.cpumask
        self.queuedepth=self.args.queuedepth

    def date_logs(self):
        x = datetime.datetime.now()       
        path=os.path.join(self.output_dir, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        self.log_dir=path       
        try:  
            os.makedirs(path) 
            print(path,"created for output logs")  
        except OSError as error:  
            print(path,"Directory already exist !!") 

    def read_json(self):
        for iteration in range(1,self.iteration+1,1):            
            log_name=self.log_dir+"/"+str(self.test_op)+"_"+str(self.queuedepth)+"_"+str(self.size)+"_"+str(self.cpumask)+"_"+str(self.thread)+"_"+str(self.time)+"_"+str(iteration)
            self.command="-w "+str(self.test_op)+" -q "+str(self.queuedepth)+" -o "+str(self.size)+" -m "+str(self.cpumask)+" -t "+str(self.time)+" -T "+str(self.thread)+" --wait-for-rpc 2>&1 | tee "+log_name+".txt; sleep 5" 
            Automation.run_session()
        
             
    def run_session(self):
        print('-'*80)       
        os.system("cd "+self.spdk_work_dir)
        #print(self.data)
        server = libtmux.Server()
        session = server.new_session(session_name="session_test", kill_session=True, attach=False)
        session = server.find_where({"session_name": "session_test"})
        window = session.new_window(attach=True, window_name="session_test")
        pane1 = window.attached_pane
        pane2 = window.split_window(vertical=True)
        if self.spdk_top:
            pane4 = window.split_window(vertical=True) 
        window.select_layout('tiled')
        pane1.send_keys(self.spdk_work_dir+'/build/examples/accel_perf '+self.command)
        time.sleep(3)
        pane2.send_keys(self.spdk_work_dir+'/scripts/rpc.py idxd_scan_accel_engine -c 0')
        pane2.send_keys(self.spdk_work_dir+'/scripts/rpc.py framework_start_init')

        if self.spdk_top:
            pane4.send_keys(self.spdk_work_dir+'/build/bin/spdk_top')
        
        pane1.send_keys('tmux kill-session -t session_test')
        server.attach_session(target_session="session_test")
    
    def summary(self):
        print("you can find logs in :",self.log_dir)
        filelist = os.listdir(self.log_dir)
        for file in filelist:
            words = file.split('.')
            word = []
            if words[1] == "txt":
              word = words[0].split('_')
              with open (self.log_dir+ "/" + file, "r+") as myfile:
                for line in  myfile:
                  data=[]
                  if "MiB" in line and "Total:" in line:
                    words = [ele for ele in line.split(" ") if ele.strip()]
                    
                    print("=========== summary ===============")
                    print("work: ", str(self.test_op))
                    print("queue depth: ",str(self.queuedepth))
                    print("transfer size: ",str(self.size))
                    print("cpumask: ",str(self.cpumask))
                    print("thread: ",str(self.thread))
                    print("time: ",str(self.time))
                    print("bandwidth: ",words[2])
                    print("log: ",self.log_dir)
                    print("===================================")
                    #print("DSA "Compare 1stream per core (1 instance) Queue Depth 256)
                    #data.extend(words[6].strip("\n").split(","))


    def Activate_setup(self):
        print("Activating the Setup")
        os.system(self.spdk_work_dir+'/scripts/setup.sh')

if __name__ == "__main__":
    print("Using Automation version :" ,VERSION)
    parser = ArgumentParser()
    parser.add_argument('-d','--output_dir', type=str, default='./logs/spdk/', help="directory to save the log")
    parser.add_argument('-o','--spdk_work_dir', type=str, default='/root/DSA/spdk', help="SPDK working directory path")
    parser.add_argument('-t','--thread', type=int, default=1,help="no of thread")
    parser.add_argument('-q','--queuedepth', type=int, default=16,help="no of queue")
    parser.add_argument('-s','--size', type=int, default=131072,help="no of queue")
    parser.add_argument('-c','--cpumask', type=str, default='0x01',help="set cpumask ")
    parser.add_argument('-w','--test_op', type=str, default='fill',help="select ops: fill,compare,crc32c,copy,dualcast")
    parser.add_argument('-i','--iteration', type=int, default=1,help="number of iteration you want to run")
    parser.add_argument('-n','--summary_name', type=str, default="summary.csv",help="name for the final summary file")
    parser.add_argument('-T','--time', type=int, default=5,help="name for the final summary file")
    parser.add_argument('--spdk_top', type=bool, default=False,help="name for the final summary file")
    args = parser.parse_args()
    Automation=Automation(args)
    Automation.date_logs()
    Automation.Activate_setup()
    Automation.read_json()
    Automation.summary()
 

 

