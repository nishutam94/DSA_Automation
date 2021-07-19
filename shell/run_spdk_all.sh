echo "Automation started"
date="$(date +"%d-%m-%Y")"

for cpumask in  0x0f 0xff;do
for qdepth in 1 2 4 8 16 32  ; do
for trnsize in  1024 2048 4096 32768 65536 131072 ; do
for time in 5; do
for varify_enable in 0;do  
for run in 1; do
for work in fill;do 
for thread in 1 2 4 8;do 

logs="./logs/$date/$cpumask/$work"
mkdir -p $logs
echo $logs

if [ $varify_enable == 1 ] 
then 
    varify="-y"
else 
    varify=" "
fi 

export log="$logs/${work}_${qdepth}_${trnsize}_${cpumask}_${time}_${varify_enable}_${thread}_${run}.txt"
echo "============================================================================="
cmd="./build/examples/accel_perf -q $qdepth -t $time -o $trnsize -w $work -m $cpumask -T $thread $varify --wait-for-rpc 2>&1 | tee  $log ; exec sh" 
echo $cmd
screen -dm bash -c "$cmd"
sleep 3
./scripts/rpc.py idxd_scan_accel_engine -c 0
./scripts/rpc.py framework_start_init
sleep 15
cat $log
killall screen 
done
done
done
done
done
done
done
done

#cd ./logs/$date/
#grep -r "MiB/s" | awk '{print $1",",$2",",$3,",",$5",",$6,","$7}' > summary.txt
#grep -vwE "Total:" summary.txt | sed 's/:/,/Ig' | sed 's/_/,/Ig'  > summary.csv


