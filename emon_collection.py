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
        self.work_dir=self.args.work_dir
        self.iteration=self.args.iteration
        self.test=self.args.test
        self.summary_name=self.args.summary_name
        self.emon=self.args.emon
        self.emon_dir=""
        self.log_dir=""
        self.command=""

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
        with open(self.test) as f:
          self.json_data = json.load(f)
          var=""
          for iteration in range(1,self.iteration+1,1):
            for index in self.json_data:
              for work in index["work"]:
                for queuedepth in index["queuedepth"]:
                  for thread in index["thread"]:
                    for cpumask in index["cpumask"]:
                      for transfer in index["transfer"]:
                        for memory in index["memory"]:
                          print("work :",work)
                          print("queuedepth :",queuedepth)
                          print("thread :",thread)
                          print("cpumask :",cpumask)
                          print("transfersize :",transfer)
                          print("memory :",memory)
                          if memory == "LLC":
                            var="-prd"
                          else:
                            var=" " 
                          self.emon_dir="software_2"+str(work)+"_"+str(queuedepth)+"_"+str(transfer)+"_"+str(cpumask)+"_"+str(thread)+"_"+str(index["time"])+"_"+str(iteration)+"_"+str(memory)
                          print("emon dir : ",self.emon_dir)
                          log_name=self.log_dir+"/"+self.emon_dir
                          self.command="-o"+str(work)+" -n"+str(queuedepth)+" -s"+str(transfer)+" -k"+str(cpumask)+" -i"+str(index["time"])+" -x100 -g3 -fc -m "+str(var)+" 2>&1 | tee "+log_name+".txt;" 
                          #print(self.command)
                          print(self.work_dir+'/./src/dsa_micro '+self.command)
                          Automation.run_session()
      

             
    def run_session(self):
        print('-'*80)       
        os.system("cd "+self.work_dir)
        #print(self.data)
        server = libtmux.Server()
        session = server.new_session(session_name="session_test", kill_session=True, attach=False)
        session = server.find_where({"session_name": "session_test"})
        window = session.new_window(attach=True, window_name="session_test")
        pane1 = window.attached_pane
        pane2 = window.split_window(vertical=True) 
        window.select_layout('tiled')
        pane1.send_keys('timeout 60 ./../master/src/dsa_micros '+self.command)
        #pane1.send_keys('./../master/src/dsa_micros '+self.command)
        pane1.send_keys('sleep 5')
        #time.sleep(3)
        #if self.emon:
        pane2.send_keys('htop')
        #pane2.send_keys('timeout 40 python2 emon.py -w '+self.emon_dir)
        pane1.send_keys('tmux kill-session -t session_test')
        server.attach_session(target_session="session_test")
        #time.sleep(3)
    def summary(self):
        print("you can find logs in :",self.log_dir)
        os.system("python3 parser.py -p "+self.log_dir+"/")

    def Activate_setup(self):
        print("Activating the Setup")
       
if __name__ == "__main__":
    print("Using Automation version :" ,VERSION)
    parser = ArgumentParser()
    parser.add_argument('--output_dir', type=str, default='./log/', help="directory to save the log")
    parser.add_argument('--work_dir', type=str, default='/root/DSA/master', help="working directory path")
    parser.add_argument('--test', type=str, default='./micro_config/emon_config.json',help="name of the configuration tests file")
    parser.add_argument('--iteration', type=int, default=1,help="number of iteration you want to run")
    parser.add_argument('--emon', type=bool, default=False,help="name for the final summary file")
    parser.add_argument('--summary_name', type=str, default="summary.csv",help="name for the final summary file")
    args = parser.parse_args()
    Automation=Automation(args)
    Automation.date_logs()
    Automation.Activate_setup()
    Automation.read_json()
    #Automation.summary()
 

 

