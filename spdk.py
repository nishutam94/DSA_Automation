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
        self.spdk_test=self.args.spdk_test
        self.test_op=self.args.test_op
        self.iteration=self.args.iteration
        self.summary_name=self.args.summary_name
        self.log_dir=""
        self.command=""
        self.instance="Multi"
        self.emon=self.args.emon
        self.spdk_top=self.args.spdk_top
        self.emon_dir=""
        self.dir=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.dsa=self.args.dsa

    def date_logs(self):
        path=os.path.join(self.output_dir,self.dir)
        self.log_dir=path       
        try:  
            os.makedirs(path) 
            print(path,"created for output logs")  
        except OSError as error:  
            print(path,"Directory already exist !!") 

    def read_json(self):
        with open(self.spdk_test) as f:
          self.json_data = json.load(f)
          if self.test_op == "all":
            for iteration in range(1,self.iteration+1,1):
                for index in self.json_data:
                  for work in index["work"]:
                    for queuedepth in index["queuedepth"]:
                      for thread in index["thread"]:
                        for cpumask in index["cpumask"]:
                          for transfer in index["transfer"]:
                            print("work :",work)
                            print("queuedepth :",queuedepth)
                            print("thread :",thread)
                            print("cpumask :",cpumask)
                            print("transfersize :",transfer)
                            print("varify:",index["varify"])
                            if cpumask =="0x01" and thread == 1:
                                self.instance="Single"
                            else:
                                self.instance="Multi"
                            print("Instance :", self.instance)
                            var=" "
                            if index["varify"]:
                                var=" -y "
                            
                            rpc=" "
                            hw="cpu"
                            if self.dsa:
                                rpc=" --wait-for-rpc "
                                hw="dsa"

                            
                            self.emon_dir=str(work)+"_"+str(queuedepth)+"_"+str(transfer)+"_"+str(cpumask)+"_"+str(thread)+"_"+str(index["time"])+"_"+str(index["varify"])+"_"+str(iteration)+"_"+self.instance+"_"+str(hw)
                            log_name=self.log_dir+"/"+self.emon_dir
                            print("dir : ",self.emon_dir)  
                            self.command="-w "+work+" -q "+str(queuedepth)+" -o "+str(transfer)+" -m "+str(cpumask)+" -t "+str(index["time"])+" -T "+str(thread)+str(var)+str(rpc)+" 2>&1 | tee "+log_name+".txt; sleep 5" 
                            
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
        if self.dsa:
            pane2 = window.split_window(vertical=True)
        if self.emon:
            pane3 = window.split_window(vertical=True) 
        if self.spdk_top:
            pane4 = window.split_window(vertical=True) 
        window.select_layout('tiled')
        pane1.send_keys(self.spdk_work_dir+'/build/examples/accel_perf '+self.command)
        time.sleep(3)
        if self.dsa:
            pane2.send_keys(self.spdk_work_dir+'/scripts/rpc.py idxd_scan_accel_engine -c 0')
            pane2.send_keys(self.spdk_work_dir+'/scripts/rpc.py framework_start_init')
        if self.emon:
            pane3.send_keys('timeout 40 python2 emon.py -w '+str(self.dir)+"/"+self.emon_dir)
        if self.spdk_top:
            pane4.send_keys(self.spdk_work_dir+'/build/bin/spdk_top')
        
        pane1.send_keys('tmux kill-session -t session_test')
        server.attach_session(target_session="session_test")
    
    def summary(self):
        print("you can find logs in :",self.log_dir)
        os.system("python3 parser.py -p "+self.log_dir+"/")
        os.system("python3 Sheet_transformer.py -p "+self.log_dir+"/")
        os.system("python3 Sheet_transformer_multi.py -p "+self.log_dir+"/")

    def Activate_setup(self):
        print("Activating the Setup")
        if self.dsa:
            os.system(self.spdk_work_dir+"/scripts/setup.sh")

if __name__ == "__main__":
    print("Using Automation version :" ,VERSION)
    parser = ArgumentParser()
    parser.add_argument('--output_dir', type=str, default='./logs/spdk/', help="directory to save the log")
    parser.add_argument('--spdk_work_dir', type=str, default='/root/DSA/spdk', help="SPDK working directory path")
    parser.add_argument('--spdk_test', type=str, default='./config.json',help="name of the configuration tests file")
    parser.add_argument('--test_op', type=str, default='all',help="select ops: fill,compare")
    parser.add_argument('--iteration', type=int, default=1,help="number of iteration you want to run")
    parser.add_argument('--summary_name', type=str, default="summary.csv",help="name for the final summary file")
    parser.add_argument('--emon', type=bool, default=False,help="name for the final summary file")
    parser.add_argument('--spdk_top', type=bool, default=False,help="name for the final summary file")
    parser.add_argument('--dsa', type=bool, default=True,help="select DSA vs CPU")
    args = parser.parse_args()
    Automation=Automation(args)
    Automation.date_logs()
    Automation.Activate_setup()
    Automation.read_json()
    Automation.summary()
 

 

