#! /bin/bash

if [ $# -ne 2 ]
then
   echo "Usage: $0 <VM password> <experiment script>"
   exit 0
fi

## create our experiment file
cat /dev/null > experiment.log
cat /dev/null > hosts.log

while read vmName vmHostname; do
	echo "$vmHostname" | grep "^vm" >& /dev/null
	if [ $? != 0 ]
	then
		continue
	fi
	echo "$vmHostname"

	sshpass -p$1 ssh -n $vmHostname "hostname" | xargs printf "%s " >> hosts.log
	sshpass -p$1 ssh -n $vmHostname 'ifconfig | grep "inet addr:192.168" | awk '\''{ print $2 }'\'' | cut -d":" -f2' >> hosts.log
done < /users/onl/experiments/$LOGNAME

cat hosts.log >> experiment.log
echo "" >> experiment.log

./$2 $1
