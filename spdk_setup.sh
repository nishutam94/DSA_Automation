#! /bin/bash

set -e 

echo -e "VT-d should be enabled from the Boot Menu. This configuration  is under EDKII Menu -> Socker Configuration-> IIO Configuration -> Intel VT For Directed I/O (VT-d) --> Intel VT For Directed I/O --> Enable\n"
echo "performance" | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
echo 2048 > /sys/devices/system/node/node0/hugepages/hugepages-2048kB/nr_hugepages
echo 2048 > /sys/devices/system/node/node1/hugepages/hugepages-2048kB/nr_hugepages

prepare_setup()
{

pip3 install pandas
pip3 install openpyxl
pip3 install libtmux

}

prepare_run_cmd()
{

git clone https://github.com/spdk/spdk
cd spdk
sudo scripts/pkgdep.sh --all
#git fetch "https://review.spdk.io/gerrit/spdk/spdk" refs/changes/48/6148/2 && git checkout FETCH_HEAD
#git fetch "https://review.spdk.io/gerrit/spdk/spdk" refs/changes/87/6287/3 && git checkout FETCH_HEAD
git fetch "https://review.spdk.io/gerrit/spdk/spdk" refs/changes/25/6325/6 && git checkout FETCH_HEAD for data collection 
#git fetch https://review.spdk.io/gerrit/spdk/spdk refs/changes/60/7660/2 && git checkout FETCH_HEAD  for memmeory cha
git submodule update --init
./configure --with-idxd --enable-debug
make

}

check_vtd_enabled()
{

	./scripts/setup.sh > setup_output.txt
	output=$(cat setup_output.txt| cut -d " " -f 7)
	output_arr=$(echo $output | tr " " "\n")
	
	for word in $output_arr
	do
        	if [[ $word == "vfio-pci" ]]; then
                	echo -e "VT-d is enabled in this system. You are good to go\n"
                	break
        	else
                	echo -e "VT-d is not enabled in the system. please enable it first\n"
			exit
        	fi
	done
}


main()
{
	prepare_setup
    prepare_run_cmd
	check_vtd_enabled
}

main

