date="$(date +"%d-%m-%Y")"
logs="./logs/$date"
mkdir -p $logs


for ((i = 0; i <= ${1}; i=i+1))
do
./instlat -x13 -k0-${i} -b1g -n1000 2>&1 | tee $logs/${i}.txt
done

#./shell.sh 12





