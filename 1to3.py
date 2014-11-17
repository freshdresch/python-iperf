from Client import *
from Server import *

import sys

if len(sys.argv) != 2:
	print "usage: python 1to3.py <VM password>"
	sys.exit()
password = sys.argv[1]

srv1 = Server("vm12c10v01", "192.168.1.1", password)
srv1.setType("tcp")
srv1.listen("5301")
srv1.start("5")

srv2 = Server("vm12c12v01", "192.168.1.4", password)
srv2.setType("tcp")
srv2.listen("5201")
srv2.start("5")

srv3 = Server("vm12c13v01", "192.168.1.3", password)
srv3.setType("tcp")
srv3.listen("5201")
srv3.start("5")

cli = Client("vm12c11v01", "192.168.1.2", password)
cli.setTarget("192.168.1.1", "5301")
cli.setTarget("192.168.1.4", "5201")
cli.setTarget("192.168.1.3", "5201")
cli.run("5", "30")

srv1.stop()
srv2.stop()
srv3.stop()
