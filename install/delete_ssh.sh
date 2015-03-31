#! /bin/bash
source /users/onl/.topology

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
    echo "delete_ssh: $vmHostname"
    sshpass -p$1 ssh -n $vmHostname rm -rf .ssh/
		sshpass -p$1 ssh -n $vmHostname mkdir .ssh/
		sshpass -p$1 scp ~/.ssh/id_rsa.pub $vmHostname:~/.ssh/
		sshpass -p$1 ssh -n $vmHostname "cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys"
		sshpass -p$1 ssh -n $vmHostname "rm -f ~/.ssh/id_rsa.pub"
		sshpass -p$1 ssh -n $vmHostname "chmod 700 ~/.ssh/"
done < /users/onl/experiments/$LOGNAME
