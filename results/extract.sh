#! /bin/bash

if [ $# -ne 2 ]; then
	echo "Usage: $0 <test directory> <results csv>"
	exit 0
fi

target=${1%/}

cmd='find '
cmd+=$target
cmd+='/json/ -mindepth 1 -type d'

for dir in $(eval ${cmd})
do
	python store.py $dir/client1.json $2
	python store.py $dir/client2.json $2
	python store.py $dir/client3.json $2
done
