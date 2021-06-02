echo "Automation started"
date="$(date +"%Y_%m_%d_%H_%M_%S")"

for o in 16;do
for n in 1 2 4 8 16 32 64 128 ; do
for s in  1K 2K 4K 8K 16K 32K 64K 128K ; do
for i in 1000; do

logs="./logs/$date/$o"
mkdir -p $logs
echo $logs

log="$logs/${o}_${n}_${s}_${i}.txt"
echo "============================================================================="
cmd="/root/DSA/dsa_micros/src/dsa_micros -n${n} -s${s} -j -c -f -i${i} -o${o}" 
echo $cmd
bash -c "$cmd" 2>&1 | tee $log

done
done
done
done

cd ./$logs
grep -r "GB per sec =" | awk '{print $1","$5}' > summary.txt
grep -vwE "GB:" summary.txt | sed 's/:/,/Ig' | sed 's/_/,/Ig' > summary.csv
