#!/usr/bin/python

import sys
import numpy as np
import scipy
from heart import HeartRecording, Sample

heart = HeartRecording(sys.argv[1])

l = []
while True:
    s = heart.read_sample()
    if s == None:
        break;
    l.append(s.value)
