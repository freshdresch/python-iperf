from Client import *
from Server import *

from functools import partial
import threading
import time
import sys

if len(sys.argv) != 2:
	print "usage: python 3to1.py <VM password>"
	sys.exit()
password = sys.argv[1]

srv = Server("vm12c10v01", "192.168.1.1", password)
srv.setType("tcp")
srv.listen("5401")
srv.listen("5405")
srv.listen("5409")
srv.start("5")

cli1 = Client("vm12c11v01", "192.168.1.2", password)
cli1.setTarget("192.168.1.1", "5401")

cli2 = Client("vm12c12v01", "192.168.1.4", password)
cli2.setTarget("192.168.1.1", "5405")

cli3 = Client("vm12c13v01", "192.168.1.3", password)
cli3.setTarget("192.168.1.1", "5409")

thread1 = threading.Thread(target=partial(cli1.run, "5", "30"))
thread2 = threading.Thread(target=partial(cli2.run, "5", "30"))
thread3 = threading.Thread(target=partial(cli3.run, "5", "30"))

time.sleep(2)

thread1.start()
thread2.start()
thread3.start()

thread1.join()
thread2.join()
thread3.join()

srv.stop()
