# DSA Automation:

Dependencies :
--------------
 > pip3 install pandas <br>
 > pip3 install openpyxl <br>
 > pip3 install libtmux <br>
 > Git clone https://github.com/nishutam94/DSA_Automation.git <br>
  


Running the Scripts:
---------------------


Note:	Configure through json or use existing configuration.

1.	 Fill_1DSA_1CORE.json  

> {    "work": ["fill"],
	    "queuedepth": [16],
	    "thread": [1],
	    "cpumask":["0x01"],
	    "time":60,
	    "transfer":[131072],
	    "varify":false
	    }
>	]

Config available parameters:
----------------------------
"work": set the operation you want to test from the available ops.<br>
Example: ["compare", "fill", "dualcast", "copy"],<br>
"queuedepth": set the queue depth of the work queue.        
Example: [1,2,4,8,16,32,128,256]<br>
"thread": set the no of thread you want to run per core.  
Example: [1,2,4,8]<br>
"cpumask": set cpumask (bind the no of cores to run the ops)
Example: ["0x01","0x03","0x0f","0xff]    <br>
"time": -> time in sec to run each ops. default is 60 sec 
"transfer": transfer size of the operation. Eg 1K,4K,128K<br>
Example: [1024,4096,131072]<br>
"verify" set verification flag
Example: true or false <br>

Run workload:
-------------
To run the single instance data for all ops: 
Python3 spdk.py –spdk_test config/single_instance.json 
To run the multiple instance data for all ops: 
Python3 spdk.py –spdk_test multi_instance.json 
