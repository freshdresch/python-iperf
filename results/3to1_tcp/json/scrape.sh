#! /bin/bash
if [ $# -ne 2 ]; then
	echo "Usage: $0 <VM password> <test directory>"
	exit 0
fi

sshpass -p$1 scp vm12c11v01:~/client1.json $2/
sshpass -p$1 ssh -n vm12c11v01 rm *.json
sshpass -p$1 scp vm12c12v01:~/client2.json $2/
sshpass -p$1 ssh -n vm12c12v01 rm *.json
sshpass -p$1 scp vm12c13v01:~/client3.json $2/
sshpass -p$1 ssh -n vm12c13v01 rm *.json

