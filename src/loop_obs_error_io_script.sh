#!/bin/bash
# loop the io_script on observation error 
export LC_NUMERIC="en_US.UTF-8" #otherwise the seq command might not work
set -ex
#NOO=1
here=$(pwd)
#while [ $NOO -lt 31 ]; do

for i in $(seq 0.1 0.05 2); do
    sed -i "s/std_err=666/std_err=$i/g" ${here}/io_scrpt.sh
    ./io_scrpt.sh
    sed -i "s/std_err=$i/std_err=666/g" ${here}/io_scrpt.sh
    echo "FINISHED std_error of "$i
# NOO=`expr $NOO + 1`
 #echo $NOO
done

