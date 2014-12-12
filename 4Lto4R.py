from Client import *
from Server import *

from functools import partial
import threading
import time
import sys

if len(sys.argv) != 2:
	print "usage: python 4Lto4R.py <VM password>"
	sys.exit()
password = sys.argv[1]

# Server setup
srv1 = Server("vm12c10v01", "192.168.1.2", password)
srv1.setType("tcp")
srv1.listen("5201")
srv1.start("5")

srv2 = Server("vm12c10v02", "192.168.1.1", password)
srv2.setType("tcp")
srv2.listen("5201")
srv2.start("5")

srv3 = Server("vm12c10v03", "192.168.1.4", password)
srv3.setType("tcp")
srv3.listen("5201")
srv3.start("5")

srv4 = Server("vm12c10v04", "192.168.1.3", password)
srv4.setType("tcp")
srv4.listen("5201")
srv4.start("5")

# Client setup
cli1 = Client("vm12c11v01", "192.168.1.5", password)
cli1.setTarget("192.168.1.1", "5201")

cli2 = Client("vm12c12v01", "192.168.1.6", password)
cli2.setTarget("192.168.1.2", "5201")

cli3 = Client("vm12c13v01", "192.168.1.7", password)
cli3.setTarget("192.168.1.3", "5201")

cli4 = Client("vm12c14v01", "192.168.1.8", password)
cli1.setTarget("192.168.1.4", "5201")

thread1 = threading.Thread(target=partial(cli1.run, "5", "30"))
thread2 = threading.Thread(target=partial(cli2.run, "5", "30"))
thread3 = threading.Thread(target=partial(cli3.run, "5", "30"))
thread4 = threading.Thread(target=partial(cli4.run, "5", "30"))

time.sleep(5)

thread1.start()
thread2.start()
thread3.start()
thread4.start()

thread1.join()
thread2.join()
thread3.join()
thread4.join()

srv1.stop()
srv2.stop()
srv3.stop()
srv4.stop()
