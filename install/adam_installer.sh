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
    echo "$vmHostname"
		
    # fix ssh folder so we can use private key
    sshpass -p$1 ssh -n $vmHostname rm -rf .ssh/
    sshpass -p$1 ssh -n $vmHostname mkdir .ssh/
    sshpass -p$1 scp ~/.ssh/id_rsa.pub $vmHostname:~/.ssh/
    sshpass -p$1 ssh -n $vmHostname "cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys"
    sshpass -p$1 ssh -n $vmHostname "rm -f ~/.ssh/id_rsa.pub"
    sshpass -p$1 ssh -n $vmHostname "chmod 600 ~/.ssh/*"
    sshpass -p$1 ssh -n $vmHostname "chmod 700 ~/.ssh/"

    # install tools
    sshpass -p$1 scp tools.sh $vmHostname:~/
    sshpass -p$1 scp iperf-3.0.11.tar $vmHostname:~/
    sshpass -p$1 ssh -n $vmHostname chmod 777 tools.sh
    sshpass -p$1 ssh -n $vmHostname ./tools.sh $1 &
done < /users/onl/experiments/$LOGNAME

wait
