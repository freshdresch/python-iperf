import subprocess

class Client:
	""" A network testing client built on iperf3 that can initiate 
	multiple TCP or UDP tests with multiple servers. """

	def __init__(self, host, addr):
		self.host = host
		self.addr = addr
		self.targets = []
		self.test = ""
		
		# UDP specific options
		self.bandwidth = ""
		self.packetlen = ""

	def setTarget(self,addr,port):
		self.targets.append((addr,port))
	
	def setType(self, test):
		self.test = test.lower()

	def setUdpOptions(self, bandwidth, packetlen=""):
		self.bandwidth = bandwidth
		self.packetlen = packetlen

	def setTcpOptions(self, packetlen=""):
		self.packetlen = packetlen
		
	def run(self, runtime):
		procs = []
		for target in self.targets:
			command = [ 'ssh', '-n', self.host, 'iperf3', '-c', target[0], '-p', target[1] ]
			# logstring = '-J > ' + self.host + '.json\"'
			command.append('-i')
			command.append('0')
			if self.test == 'udp':
				command.append('-t')
				command.append(str(runtime))
				command.append('-u')
				command.append('-b')
				command.append(str(self.bandwidth))
				if self.packetlen: 
					command.append('-l')
					command.append(self.packetlen)
			else: ## tcp
				command.append('-t')
				command.append(str(runtime + 2))
				command.append('-O')
				command.append(str(2))
				if self.packetlen:
					command.append('-M')
					command.append(self.packetlen)
				command.append('-C')
				command.append('cubic')
				command.append('-l')
				command.append('1400')
			# command.append('\"')
			# command.append(logstring)
			# print " ".join(map(str, command))

			p = subprocess.Popen(command)
			procs.append(p)

		# wait for all subprocesses to finish
		for p in procs:
			p.wait()
