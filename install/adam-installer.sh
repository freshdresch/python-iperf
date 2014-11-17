#! /bin/bash

if [ $# -ne 1 ]
then
   echo "Usage: $0 <VM password>"
   exit 0
fi

while read vmName vmHostname; do
         echo "$vmHostname" | grep "^vm" >& /dev/null
         if [ $? != 0 ]
         then
           continue
         fi
         echo "$vmHostname"
     sshpass -p$1 scp tools.sh $vmHostname:~/
     sshpass -p$1 scp iperf.tar.gz $vmHostname:~/
     sshpass -p$1 ssh -n $vmHostname chmod 777 tools.sh
     sshpass -p$1 ssh -n $vmHostname ./tools.sh $1
done < /users/onl/experiments/$LOGNAME
