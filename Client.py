import subprocess

class Client:
	""" A network testing client that can initiate 
	multiple TCP or UDP tests with multiple servers,
	using iperf or iperf3. We assume iperf3 by default. """

	def __init__(self, host, addr, password=""):
		self.host = host
		self.addr = addr
		self.password = password

		self.targets = []
		self.tool = "iperf3"
		self.test = ""
		
		# UDP specific options
		self.bandwidth = ""
		self.packetlen = ""

	def setTarget(self,addr,port):
		self.targets.append((addr,port))
	
	def setTool(self, tool):
		self.tool = tool

	def setType(self, test):
		self.test = test.lower()
		
	def setPassword(self, password):
		self.password = password

	def setUdpOptions(self, bandwidth, packetlen=""):
		self.bandwidth = bandwidth
		self.packetlen = packetlen
		
	def run(self, interval, runtime):
		procs = []
		for target in self.targets:
			command = ["sshpass", "-p"+self.password, "ssh", "-n", self.host, \
					   self.tool, "-c", target[0], "-t", runtime, "-i", \
					   interval, "-p", target[1]]
			
			if self.test is "udp":
				command.append("-u")
				command.append("-b")
				command.append(self.bandwidth)
				if self.packetlen:
					command.append("-l")
					command.append(self.packetlen)

			p = subprocess.Popen(command)
			procs.append(p)

		# wait for all subprocesses to finish
		for p in procs:
			p.wait()
