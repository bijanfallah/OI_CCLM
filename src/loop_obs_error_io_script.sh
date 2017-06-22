#!/bin/bash
# loop the io_script on observation error 

set -ex
NOO=1
here=$(pwd)
while [ $NOO -lt 31 ]; do
 sed -i "s/no_members=9999 #----/no_members=$NOO #----/g" ${here}/io_scrpt.sh
 ./io_scrpt.sh
 sed -i "s/no_members=$NOO #----/no_members=9999 #----/g" ${here}/io_scrpt.sh
 echo "FINISHED no_member = "$NOO
 NOO=`expr $NOO + 1`
 echo $NOO
done

