import subprocess

class Server:
	""" A network testing server that can start an iperf 
	or iperf3 server on any given port. When using iperf, 
	file output does not work properly. Fortunately, 
	with iperf the server communicates its results back
	to the client, so we don't lose much detail unless
	the UDP sending rate is too high. We assume iperf3 
	by default. """
	
	def __init__(self, host, addr, password=""):
		self.host = host
		self.addr = addr
		self.password = password

		self.ports = []
		self.logFiles = []
		self.numIncoming = 0
		self.tool = "iperf3"
		self.test = ""

	def setTool(self, tool):
		self.tool = tool

	def setType(self, test):
		self.test = test.lower()
		
	def setPassword(self, password):
		self.password = password

	def listen(self, port):
		self.ports.append(port)
		self.numIncoming += 1

	def start(self, interval=""):
		command = ["sshpass", "-p"+self.password, "ssh", "-n", self.host]
		log = ""

		if self.tool is "iperf":
			command.append("iperf -s")
			if self.test is "udp":
				command.append("-u")
		elif self.tool is "iperf3":
			command.append("iperf3 -s")

		if interval:
			command.append("-i " + str(interval))
		command.append("-p")
		
		for idx,port in enumerate(self.ports):
			command.append(str(port))
			if self.tool is "iperf3":
				logstring = "-D --logfile="
				log = self.host
				if self.numIncoming > 1:
					log += ("_" + str(idx+1))
				log += ".log"	
				self.logFiles.append(log)
				logstring += log
				command.append(logstring)

			subprocess.Popen(command)
			print " ".join(map(str, command))
			start = command.index(port)
			while len(command) > start:
				command.pop(start)

	def stop(self):
		command = ["sshpass", "-p"+self.password, "ssh", "-n", self.host, "pkill", self.tool]
		subprocess.Popen(command)
