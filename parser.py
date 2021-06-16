import os
from argparse import ArgumentParser
import csv

VERSION=1.0

class Parser():

    def __init__(self, args):
        self.args = args
        self.output_dir=self.args.output_dir
        self.output=self.args.output

    def Parsing(self):
        filelist = os.listdir(self.output_dir)
        list_of_words=[]
        header=["operation","queue depth","transfer size","cpumask","thread/core","time","varify","iteration","instance","core","thread","BW","avg-latency","max-latency"]
        for file in filelist:
            words = file.split('.')
            word = []
            if words[1] == "txt":
              word = words[0].split('_')
              with open (self.output_dir + file, "r+") as myfile:
                for line in  myfile:
                  data=[]
                  if "MiB" in line and "Total:"  in line:
                    words = [ele for ele in line.split(" ") if ele.strip()]
                    core=words[0].strip(",")
                    data.append(core[0])
                    data.append(core[2])
                    #data.append(words[2])
                    #print(words[2])
                    bw=round(int(words[2])/954,1)
                    #print(bw)
                    data.append(bw)
                    #data.extend(words[6].strip("\n").split(","))
                    list_of_words.append(word+data)
        print("you can find the log summary at :",self.output_dir+self.output)
        with open(self.output_dir+self.output, 'w') as f:
          write = csv.writer(f)
          write.writerow(header)
          write.writerows(list_of_words)

if __name__ == "__main__":
    print("Using Parser version :" ,VERSION)
    parser = ArgumentParser()
    parser.add_argument("-p", "--output_dir", help="Specify Path of logs",default="./Automation_log/")
    parser.add_argument("-o", "--output", help="Specify name of summary",default="summary.csv")
    args = parser.parse_args()
    Automation=Parser(args)
    Automation.Parsing()
