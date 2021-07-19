#!/bin/bash
date="$(date +"%Y_%m_%d")"
time="$(date +"%H_%M_%S")"

logs=./logs/$date/$1
mkdir -p $logs
#for flag in "-f" "-fc" "-c" ;
for flag in "-f" "-fc" "-c" ;
do
for o in 3 ;
do
#for k in "0,1,2,3" ,"0" "0,12" "0,12,24" "0,12,24,36";
for k in "0,1,2,3" ;
do	
for s in "128k" "32k";
do 

for i in 1 2 3 4 5;
do 
b=`./src/dsa_micros -s${s} -n16 ${flag} -k${k} -g3 -o${o} -m -i10 | grep GB | cut -f 5 -d ' ' `
echo  $i ":" "./src/dsa_micros -s${s} -n16 ${flag} -k${k} -g3 -m -o${o} -i10 " " : " $b >> $logs/${time}.txt 
sleep 1
done
done
done 
done
done
echo