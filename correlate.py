#!/usr/bin/python

import sys
import numpy as np
import peakutils

arr = np.load(sys.argv[1])

ones = np.ones(1000)
avg = np.convolve(arr, ones)
arr1 = np.concatenate(arr, np.ones(999, dtype=np.int16))
avg /= 1000
normarr = arr1 - avg

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
    def __init__(self, p, r, t, ppeak, rpeak, tpeak):
        self.p =  p
        self.r = r
        self.t = t
        self.ppeak = ppeak
        self.rpeak = rpeak
        self.tpeak = tpeak

    @staticmethod
    def from_res(idx):
        ppeak = conarr[res[idx]]
        rpeak = conarr[res[idx+1]]
        tpeak = conarr[res[idx+2]]
        return Seq(res[idx], res[idx+1], res[idx+2], ppeak, rpeak, tpeak)

seqs = []
for x in range(len(res) - 2):
    if recognize_seq(x):
        seqs.append(Seq.from_res(x))

print len(seqs)
for x in seqs:
    print x.r - x.p
