#!/bin/bash
date="$(date +"%Y_%m_%d")"
time="$(date +"%H_%M_%S")"

#for flag in "-j" "-jf" "-jfc" "-f" "-fc" "-jc" "-c" ;
for uncore in  12 14 16 18; 
do
logs=./logs/$date/$uncore
mkdir -p $logs
wrmsr -a 0x620 0x${uncore}${uncore}
echo "uncore freq : " $uncore >>  $logs/${time}.txt


for corefreq in 14 18 1c 1e 20 24 26 ;
do
wrmsr -a 0x1ad 0x${corefreq}${corefreq}${corefreq}${corefreq}${corefreq}${corefreq}${corefreq}${corefreq}
echo "core freq : " $corefreq >>  $logs/${time}.txt
for o in 3 ;
do
for k in 1 2 4 8 16 32 64 128 256 ;
do	
for i in 1 2 3 ;
do 
b=`./src/dsa_micros  -s${k}k -n16 -jcf -k0 -g3 -o${o} -i1000 | grep GB | cut -f 5 -d ' ' `
echo  $i ":" "./src/dsa_micros -s${k}k -n16 -jcf -k0 -g3 -o${o} -i1000" " : " $b >>  $logs/${time}.txt 
sleep 1
done
done
done 
done
done 