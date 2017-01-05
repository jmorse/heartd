#!/usr/bin/python

import sys
import numpy as np
import scipy
from heart import HeartRecording, Sample

heart = HeartRecording(sys.argv[1])

# Drops first sample...
refsample = heart.read_sample()
prevtime = refsample.timestamp

fail = 0
l = []
pair= False
s = heart.to_numpy()

print "fails: {}".format(fail)
