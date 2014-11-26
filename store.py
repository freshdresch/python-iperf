from Parser import *
import os, sys
import csv

if len(sys.argv) != 3:
    print "usage: python store.py <source.json> <target.csv>"
    sys.exit()
inFile = sys.argv[1]
outFile = sys.argv[2]

data = []
legend = ['Bits Per Second', 'Bytes', 'Interval 1', 'Interval 2', 'Interval 3', 'Interval 4', 'Interval 5']

par = Parser()
par.extract(inFile)
data.append([par.bps, par.bytes, par.intervalBPS[0], par.intervalBPS[1], par.intervalBPS[2], par.intervalBPS[3], par.intervalBPS[4]])


# test if file already exists before we open it
exists = os.path.isfile(outFile)
with open(outFile, 'a') as file:
    writer = csv.writer(file, delimiter=',')
    if not exists:
        writer.writerows([legend])
    writer.writerows(data)
