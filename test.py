from Client import *
from Server import *

import sys
import time
from functools import partial
import threading

if len(sys.argv) != 2:
	print "usage: python test.py <VM password>"
	sys.exit()

password = sys.argv[1]

srv1 = Server("vm12c10v01", "192.168.1.1", password)
srv1.setType("tcp")
srv1.listen("5201")
srv1.listen("5202")
srv1.listen("5203")
srv1.start("5")

srv2 = Server("vm12c11v01", "192.168.1.2", password)
srv2.setType("tcp")
srv2.listen("5201")
srv2.listen("5202")
srv2.listen("5203")
srv2.start("5")

srv3 = Server("vm12c12v01", "192.168.1.4", password)
srv3.setType("tcp")
srv3.listen("5201")
srv3.listen("5202")
srv3.listen("5203")
srv3.start("5")

srv4 = Server("vm12c13v01", "192.168.1.3", password)
srv4.setType("tcp")
srv4.listen("5201")
srv4.listen("5202")
srv4.listen("5203")
srv4.start("5")

cli1 = Client("vm12c10v01", "192.168.1.1", password)
cli1.setTarget("192.168.1.2", "5201")
cli1.setTarget("192.168.1.3", "5201")
cli1.setTarget("192.168.1.4", "5201")

cli2 = Client("vm12c11v01", "192.168.1.2", password)
cli2.setTarget("192.168.1.1", "5201")
cli2.setTarget("192.168.1.3", "5202")
cli2.setTarget("192.168.1.4", "5202")

cli3 = Client("vm12c12v01", "192.168.1.4", password)
cli3.setTarget("192.168.1.1", "5202")
cli3.setTarget("192.168.1.2", "5202")
cli3.setTarget("192.168.1.3", "5203")

cli4 = Client("vm12c13v01", "192.168.1.3", password)
cli4.setTarget("192.168.1.1", "5203")
cli4.setTarget("192.168.1.2", "5203")
cli4.setTarget("192.168.1.4", "5203")

thread1 = threading.Thread(target=partial(cli1.run, "5", "30"))
thread2 = threading.Thread(target=partial(cli2.run, "5", "30"))
thread3 = threading.Thread(target=partial(cli3.run, "5", "30"))
thread4 = threading.Thread(target=partial(cli4.run, "5", "30"))

# give some time for the threads to set everything up
time.sleep(5)

thread1.start()
thread2.start()
thread3.start()
thread4.start()

# baseline = time.time()
# t0 = time.time() - baseline
# print "*"*80
# print "t0:",t0
# print "*"*80

# cli1.run("5","30")

# t1 = time.time() - baseline
# print "*"*80
# print "t1:",t1
# print "*"*80

# cli2.run("5","30")

# t2 = time.time() - baseline
# print "*"*80
# print "t2:",t2
# print "*"*80

# cli3.run("5","30")

# t3 = time.time() - baseline
# print "*"*80
# print "t3:",t3
# print "*"*80

# cli4.run("5","30")

# t4 = time.time() - baseline
# print "*"*80
# print "t4:",t4
# print "*"*80


# cli.setTool("iperf3")
# cli.setType("udp")
# cli.setUdpOptions("20m","12")
# cli.run("5","30")

# cli.setUdpOptions("6g")
# cli.setTool("iperf")
