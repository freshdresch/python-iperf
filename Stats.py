class Stats:
	""" Calculates shifted variance and means which 
	does not effect / bias the sample mean and variance,
	but avoids certain floating point precision issues. 
	Adapted from Wikipedia. """

	# http://en.wikipedia.org/wiki/Algorithms_for_calculating_variance

	def __init__(self, vals=[]):
		self.values = []
		self.shift = 0.0        # K
		self.numSamples = 0     # n
		self.firstMoment = 0.0  # E[x]
		self.secondMoment = 0.0 # E[x]^2
		for val in vals:
			self.add(val)

	def add(self,val):
		if (self.numSamples == 0):
			self.shift = val
		self.numSamples += 1
		self.values.append(val)
		self.firstMoment += (val - self.shift)
		self.secondMoment += (val - self.shift) * (val - self.shift)
 
	def remove(self,val):
		try:
			self.values.remove(val)
		except:
			return
		self.numSamples -= 1
		self.firstMoment -= (val - self.shift)
		self.secondMoment -= (val - self.shift) * (val - self.shift)
 
	def mean(self):
		return self.shift + self.firstMoment / self.numSamples
 
	def variance(self):
		numerator = self.secondMoment - (self.firstMoment * self.firstMoment) / self.numSamples
		return numerator / (self.numSamples - 1)
