#!/bin/bash
date="$(date +"%Y_%m_%d")"
time="$(date +"%H_%M_%S")"

logs=./logs/$date/$1
mkdir -p $logs

sudo ./setup_dsa.sh /root/DSA/dsa_micros/configs/4e1w-4d.conf
sudo ./setup_dsa.sh /root/DSA/dsa_micros/configs/4e1w-d.conf 
sudo ./setup_dsa.sh /root/DSA/dsa_micros/configs/4e1w-2d.conf
sudo ./setup_dsa.sh /root/DSA/dsa_micros/configs/4e1w-3d.conf

#for flag in "-j" "-jf" "-jfc" "-f" "-fc" "-jc" "-c" ;
for flag in  "-jfc" ;
do
for o in 3 4 6;
do
for k in "0" "0,1" "0,1,2" "0,1,2,3" ;
#for k in "0"  ;
do	
for i in 1 2 3;
do 
#b=`./src/dsa_micros  -s1g -n1 ${flag} -k${k} -g3 -o${o} -i100 | grep GB | cut -f 5 -d ' ' `
b=`./src/dsa_micros  -s16k -n32 ${flag} -k${k} -g3 -o${o} -i1000 | grep GB | cut -f 5 -d ' ' `
echo  $i ":" "./src/dsa_micros -s1g -n1 ${flag} -k${k} -g3 -o${o} -i100" " : " $b >>  $logs/${time}.txt 
sleep 1
done
done
done 
done
