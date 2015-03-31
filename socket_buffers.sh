#! /bin/bash
source /users/onl/.topology

while read vmName vmHostname; do
	echo "$vmHostname" | grep "^vm" >& /dev/null
	if [ $? != 0 ]
	then
		continue
	fi
	echo -n "$vmHostname: "
	ssh -n $vmHostname "netstat -s | grep error"
done < /users/onl/experiments/$LOGNAME
