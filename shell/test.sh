for i in 1 2 4 8 12 16 ; do
echo "no of core :" $i >> 3_512.txt
./Parallel_run_shell.sh $i >> 3_512.txt 
done 