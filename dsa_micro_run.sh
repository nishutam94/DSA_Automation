echo "Automation started"
date="$(date +"%Y_%m_%d_%H_%M_%S")"
wd=$(pwd)

sudo /root/DSA/dsa_micros/setup_dsa.sh /root/DSA/dsa_micros/configs/4e1w-d.conf
for i in {0..3}; do echo -n "dsa$i/wq$i.0 "; s=`cat /sys/bus/dsa/devices/dsa$i/wq$i.0/state`; m=`cat /sys/bus/dsa/devices/dsa$i/wq$i.0/mode`; echo $s $m; done

for llc_var in "LLC" "Memory" ; do
#for S in "LSLD" ; do
for S in "LSLD" "RSLD" "LSRD" "RSRD"; do
for o in   3 5 6;do
#for n in 1 2 4 8 16 32 64 128 ; do
#for s in 1K 2K 4K 8K 16K 32K 64K 128K ; do
for n in 128 ; do
for s in 4K  ; do
for i in 1000; do
for k in '0' ; do
#for k in '0' '0,1'; do

if [ $S = "RSLD" ]; 
then
   memloc="1,-1"
elif [ $S = "LSRD" ];
then
   memloc="-1,1"
elif [ $S = "RSRD" ];
then
   memloc="1,1"
else
   memloc="-1,-1"
fi

llc=""
if [ "$llc_var" = "LLC" ]; 
then
    llc="-prd"
fi


logs="./logs/$date"
#logs="./logs/$date/$llc_var/$S"
mkdir -p $logs
echo $logs

log="$logs/${o}_${n}_${s}_${i}_${k}_${llc_var}_${S}.txt"
echo "================================================================================================="
cmd="/root/DSA/dsa_micros/src/dsa_micros -n${n} -s${s} -jcf -i${i} -o${o} -g3 -k${k} -S${memloc} ${llc}" 
echo $cmd
bash -c "$cmd" 2>&1 | tee $log

done
done
done
done
done

cd $logs
grep -r "GB per sec =" | awk '{print $1","$5}' > summary.txt
grep -vwE "GB:" summary.txt | sed 's/:/,/Ig' | sed 's/_/,/Ig' > summary.csv
python3 $wd/Sheet_transformer_micro.py -p "./"
echo "check summary : $logs/summary.csv"
cd $wd
done
done



#For data in LLC
#  sudo ./src/dsa_micros -n128 -s4k -jcf -i1000 -g3 -prd -o3

#For data in memory
#  sudo ./src/dsa_micros -n128 -s4k -jcf -i1000 -g3 -o3

