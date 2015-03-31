#! /usr/bin/env python
## My client and server wrappers for iperf3
from Client import *
from Server import *

## systems code for threading, ideally will be replaced  with asynchronous
from functools import partial
import threading
import sys

## timing code
from timeit import default_timer as timer
import time

if len(sys.argv) != 2:
	print "usage: python 11Rto11L.py <VM password>"
	sys.exit()
password = sys.argv[1]

vms = {}
with open("hosts.log") as f:
	for line in f:
		mapping = line.split()
		vms[ mapping[0] ] = mapping[1]

climap = {}
srvmap = {}
for key, value in vms.iteritems():   # iter on both keys and values
	if key.startswith('vm12c12'):
		srvmap[key] = value
	else:
		climap[key] = value

clients = []
servers = []
threads = []

for key in srvmap:
	srv = Server(key, srvmap[key], password)
	srv.listen("5201")
	srv.start()
	servers.append(srv)

srvlist = srvmap.items()
for idx, key in enumerate(climap):
	cli = Client(key, climap[key], password)
	cli.setTarget(srvlist[idx][1], "5201")
	clients.append(cli)
	print key,climap[key] + " sends to " + srvlist[idx][0],srvlist[idx][1]

for cli in clients:
	thread = threading.Thread(target=partial(cli.run, 10))
	threads.append(thread)

time.sleep(10)

# before = timer()
for thread in threads:
	thread.start()

for thread in threads:
	thread.join()
# after = timer()

for srv in servers:
	srv.stop()

# print "%.3f seconds between starting iperf sessions and when all of them are done (some overhead expected)" % (after - before)

