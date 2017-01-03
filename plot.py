#!/usr/bin/python

import sys
import matplotlib.pyplot as plt

data = []
with open(sys.argv[1], "r") as f:
    for x in f.readlines():
        x = x.rstrip('\n')
        x = x.rstrip('\r')
        x = x.rstrip()
        x = x.split(',')
        x = [y.rstrip(',') for y in x]
        x = [int(y) for y in x]
        data.append(x[1])

plt.plot(data)
plt.show()
