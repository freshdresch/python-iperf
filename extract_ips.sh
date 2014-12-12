#! /bin/bash

if [ $# -ne 1 ]
then
   echo "Usage: $0 <VM password>"
   exit 0
fi

## create our hosts file
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
