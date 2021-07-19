#!/bin/bash
date="$(date +"%Y_%m_%d")"
time="$(date +"%H_%M_%S")"
size="1g"
n="1"
logs=./logs/$date/sweep/$size
mkdir -p $logs

for ((i = 0; i <= ${1}; i=i+1))
do	
	#echo -n "$(( i/2+1 )) "
	#b1=`./src/dsa_micros -x100 -g3 -s1g -n1 -k$m -m -i10 | grep GB | cut -f 5 -d ' '` 
	#b2=`./src/dsa_micros -x100 -g3 -s16k -n$n -k$m -m -i10 | grep GB | cut -f 5 -d ' '`
	#b3=`./src/dsa_micros  -g3 -cf -s${size} -n32 -k0-$i -m -i1000 -o3 | grep GB | cut -f 5 -d ' '`
    b3=`./src/dsa_micros -g3 -cf -s${size} -n$n -k0-$i -m -i10 -o3 | grep GB | cut -f 5 -d ' '`
	b4=`./src/dsa_micros -g3 -cf -s${size} -n$n -k0-$i -m -i10 -o4 | grep GB | cut -f 5 -d ' '`
	b6=`./src/dsa_micros -g3 -cf -s${size} -n$n -k0-$i -m -i10 -o6 | grep GB | cut -f 5 -d ' '`
	
    
	echo $i ":" $size ":" $n ":" $b3 ":" $b4 ":" $b6 >> $logs/${time}.txt 
done

