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

	def setPassword(self, password):
		self.password = password

	def listen(self, port):
		self.ports.append(port)

	def start(self, interval=''):
		command = ['sshpass','-p'+self.password, 'ssh', '-n', self.host]
		command.append('iperf3 -s')
		if interval:
			command.append('-i' + str(interval))
		command.append('-p')
		
		for port in self.ports:
			command.append(str(port))
			subprocess.Popen(command)
			print ' '.join(map(str, command))

			start = command.index(port)
			while len(command) > start:
				command.pop(start)

	def stop(self):
		command = ["sshpass", "-p"+self.password, "ssh", "-n", self.host, "pkill", "iperf3"]
		subprocess.Popen(command)
		print ' '.join(map(str, command))
