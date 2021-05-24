#!/bin/bash




VERSION=0.1
echo "System information :" $VERSION
echo "==============================================================="
echo ""
if test $UID -ne 0 
then
    echo >&2 "Please run this script as root user"
    exit 1
fi

echo "--------------------- Memory ---------------------------------"

dmidecode | grep  "Memory Technology: " | head -n 1 | xargs
echo -n "No of DIMMS :"
dmidecode | grep  "Volatile Size:" | grep "GB" | wc -l | xargs
dmidecode | grep  "Volatile Size:" | grep "GB" | head -n 1 | xargs
dmidecode | grep  "Speed: " | grep "MT/s" | head -n 1 | xargs
dmidecode | grep  "Configured Memory Speed:" | grep "MT/s" | head -n 1 | xargs

echo "---------------------- Plateform -----------------------------"
dmidecode | grep "Product Name:" | head -n 1 | xargs
echo -n "BIOS "
dmidecode | grep "Version:" | head -n 1 | xargs

echo "----------------------- CPU -----------------------------------"
lscpu | sed '4,12!d'
lscpu | sed '19,23!d'

echo "--------------------- OS ---------------------------------"
cat /etc/os-release | grep "NAME=" | head -n 1
cat /etc/os-release |  grep "VERSION="  | head -n 1
echo -n "kernel version : "
uname -r
echo "--------------------- OTHERS ---------------------------------"
echo -n "scaling governor : " 
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor | head -n 1

echo "==============================================================="