import subprocess

class Server:
	""" A network testing server that can start an iperf3 
	server on any given port."""
	
	def __init__(self, host, addr):
		self.host = host
		self.addr = addr
		self.ports = []

	def listen(self, port):
		self.ports.append(port)

	def start(self, interval=''):
		command = ['ssh', '-n', self.host, 'iperf3', '-s', '-D']
		if interval:
			command.append('-i' + str(interval))
		command.append('-p')
		
		for port in self.ports:
			command.append(str(port))
			subprocess.Popen(command)
			# print ' '.join(map(str, command))

			start = command.index(port)
			while len(command) > start:
				command.pop(start)

	def stop(self):
		command = ["ssh", "-n", self.host, "pkill", "iperf3"]
		subprocess.Popen(command)
		# print ' '.join(map(str, command))
