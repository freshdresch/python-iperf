#!/usr/bin/env python
from time import sleep
import subprocess
import threading
import sys

servers = []
hosts = []
mapper = {}
servers.append("vm12c01v01")

def getHosts():
	with open("hosts.log", "r") as infile:
		for line in infile:
			chunks = line.split()
			hosts.append(chunks[0])
			mapper[chunks[0]] = chunks[1]

def setupServers():
	for host in hosts:
		if host not in servers:
			continue
		log = "--logfile=" + host + ".log"
		subprocess.Popen(["sshpass","-p",sys.argv[1],"ssh","-n",host,"iperf3","-s","-D",log])
		print "iperf3 -s on",host
		# ret = subprocess.call(["sshpass","-p",sys.argv[1],"ssh","-n",host,"lsof","-i:5201"])
		# if ret is not 0:
		# 	print "error!"
		# 	exit(1)
		# subprocess.call(["sshpass","-p",sys.argv[1],"ssh","-n",host,"pkill","iperf3"])

def checkServers():
	for host in hosts:
		if host not in servers:
			continue
		subprocess.call(["sshpass","-p",sys.argv[1],"ssh","-n",host,"lsof","-i:5201"])
		print "checking server on",host
		# print "ret",ret
		# if ret is not 0:
		# print "alleged error"
			# print "Error! Server on",host,"did not start correctly. Aborting experiment."
			# cleanupServers()
			# sys.exit(1)

def cleanupServers():
	for host in hosts:
		if host not in servers:
			continue
		subprocess.call(["sshpass","-p",sys.argv[1],"ssh","-n",host,"pkill","iperf3"])
		print "cleaning up server on",host

def run():
	for host in hosts:
		if host in servers:
			continue
		p = subprocess.Popen(["sshpass","-p",sys.argv[1],"ssh","-n",host,"iperf3","-c", \
		 				  mapper[servers[0]],"-t30"])
		p.wait()
		

if __name__=="__main__":
	if len(sys.argv) is not 2:
		print "Usage: python 3to1.py <VM password>"
		sys.exit(1)

	
	# Staging
	getHosts()
	setupServers()
	checkServers()
	sleep(2)
	run()

	# sleep(10)
	# sleep(35)

	# run experiments
	# threads = []
	# for host in hosts:
	# 	if host in servers:
	# 		continue
	# 	client = threading.Thread(target=run,args)
	# 	threads.append(client)
	# 	client.start()
	
	# for client in threads:
	# 	client.join()
	cleanupServers()
