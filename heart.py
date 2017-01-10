import numpy as np
import os
import socket
import struct

class Sample:
    def __init__(self, value):
        self.timestamp = 0
        self.value = value

    @staticmethod
    def from_bytes(b):
        assert len(b) == 4
        s, = struct.unpack('I', b)
        return Sample(s)

class Heart(object):
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a receive buffer large enough for 1s of samples
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024*8)

    def connect(self):
        self.s.connect(('127.0.0.1', 1234))

    def read_sample(self):
        try:
            sample = self.s.recv(4)
        except socket.error:
            return None

        return Sample.from_bytes(sample)

    def disconnect(self):
        self.s.shutdown()
        self.s = None

    def setblocking(self, val):
        self.s.setblocking(val)

class HeartRecording(Heart):
    def __init__(self, f):
        super(HeartRecording, self).__init__()
        self.thefile = open(f, "rb")
        self.filename = f

    def connect(self):
        pass

    def read_sample(self):
        b = self.thefile.read(8)
        if len(b) == 0:
            return None
        return Sample.from_bytes(b)

    def to_numpy(self):
        res = os.stat(self.filename)
        size = res.st_size
        assert (size % 8) == 0

        # Problem: there are certain skips in the signal, roughly once ever 32
        # samples (but never double skips). Handle by repeating the prior
        # sample for now. But, this means we don't know the size in advance, so
        # can't allocate one np array to rule them all.

        # Burn first sample
        s = self.read_sample()
        prevtime = s.timestamp

        def combiner():
            allarray = None
            while True:
                newarray = np.empty(65536, np.int16)
                x = 0
                while x < 65536:
                    foo = yield None

                    # Check for breakout
                    if foo == None:
                        if x == 0:
                            yield allarray

                        # Trim newarray
                        newarray = newarray[0:x]
                        # Append to allarray
                        if allarray is None:
                            allarray = newarray
                        else:
                            allarray = np.concatenate((allarray, newarray))
                        yield allarray

                    # Received a sample -> store
                    newarray[x] = foo
                    x += 1

                # End of 2^16 loop...
                if allarray is None:
                    allarray = newarray
                else:
                    allarray = np.concatenate((allarray, newarray))

        gen = combiner()
        gen.next()
        while True:
                s = self.read_sample()
                if s == None:
                    break

                if s.timestamp != prevtime + 1:
                    # Must only ever skip by 1
                    assert s.timestamp == (prevtime + 2) % 65536
                    gen.send(s.value)
                    gen.send(s.value)
                else:
                    gen.send(s.value)

                prevtime = s.timestamp

        allarray = gen.send(None)
        return allarray
