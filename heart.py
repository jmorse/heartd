import socket
import struct

class Sample:
    def __init__(self, timestamp, value):
        self.timestamp = timestamp
        self.value = value

class Heart:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a receive buffer large enough for 1s of samples
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024*8)

    def connect(self):
        self.s.connect(('127.0.0.1', 1234))

    def read_sample(self):
        sample = self.s.recv(8)
        assert len(sample) == 8
        t, s = struct.unpack('LL', sample)
        return Sample(t, s)

    def disconnect(self):
        self.s.shutdown()
        self.s = None

    def setblocking(self, val):
        self.s.setblocking(val)
