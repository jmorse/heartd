#!/usr/bin/python

import argparse
import sys
import numpy as np
import scipy
from heart import HeartRecording, Sample

parser = argparse.ArgumentParser()
parser.add_argument('source')
parser.add_argument('target')

args = parser.parse_args()

heart = HeartRecording(args.source)

# Drops first sample...
refsample = heart.read_sample()
prevtime = refsample.timestamp

fail = 0
l = []
pair= False
s = heart.to_numpy()
np.save(args.target, s)
