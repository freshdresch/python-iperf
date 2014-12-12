# Assumes the output file is already in the folder
from math import floor
import json
import sys

class Parser:
    """ A class to extract any useful information from the iperf3
    json output. Then users can access whatever fields they
    are interested in. """

    def __init__(self):
        self.bps = 0
        self.bytes = 0
        self.runLength = 0
        self.intervalBPS = []
        self.intervalLength = 0
        self.hostUtilization = 0
        self.remoteUtilization = 0

    def extract(self, file):
        with open(file) as dataFile:
            data = json.load(dataFile)

        self.bps = data['end']['sum_received']['bits_per_second']
        self.bytes = data['end']['sum_received']['bytes']
        self.runLength = data['end']['sum_received']['seconds']
        self.hostUtilization = data['end']['cpu_utilization_percent']['host_total'] / 100.0
        self.remoteUtilization = data['end']['cpu_utilization_percent']['remote_total'] / 100.0
        self.intervalLength = floor(data['intervals'][0]['sum']['seconds'])
        for i in xrange(len(data['intervals'])):
            self.intervalBPS.append(data['intervals'][i]['sum']['bits_per_second'])
