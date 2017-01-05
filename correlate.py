#!/usr/bin/python

import sys
import numpy as np
import peakutils

arr = np.load(sys.argv[1])

lolsin = np.arange(0, np.pi, np.pi/100)
lolsin = np.sin(lolsin)
conarr = np.correlate(arr, lolsin)
res = peakutils.peak.indexes(conarr, thres=0.5, min_dist=10)

def recognize_seq(idx):
    ppeak = conarr[res[idx]]
    rpeak = conarr[res[idx+1]]
    tpeak = conarr[res[idx+2]]

    return ppeak < rpeak and ppeak < tpeak

class Seq:
    def __init__(self, p, r, t):
        self.p =  p
        self.r = r
        self.t = t

    @staticmethod
    def from_res(idx):
        ppeak = conarr[res[idx]]
        rpeak = conarr[res[idx+1]]
        tpeak = conarr[res[idx+2]]
        return Seq(ppeak, rpeak, tpeak)

seqs = []
for x in range(len(res) - 2):
    if recognize_seq(x):
        seqs.append(Seq.from_res(x))

print len(seqs)
