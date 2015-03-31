from Client import *
from Server import *

from functools import partial
import threading
import time
import sys

if len(sys.argv) != 2:
	print "usage: python 11Rto11L.py <VM password>"
	sys.exit()
password = sys.argv[1]

vms = {}
with open("hosts.log") as f:
	for line in f:
		mapping = line.split()
		vms[ mapping[0] ] = mapping[1]

for key in vms:
	if key.startswith('vm12c12'):
		command = ["sshpass", "-p"+password, "ssh", "-n", key, "pkill", "iperf3"]
		subprocess.Popen(command)

