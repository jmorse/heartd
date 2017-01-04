import socket
import struct

class Sample:
    def __init__(self, timestamp, value):
        self.timestamp = timestamp
        self.value = value

    @staticmethod
    def from_bytes(b):
        assert len(b) == 8
        t, s = struct.unpack('II', b)
        return Sample(t, s)

class Heart:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a receive buffer large enough for 1s of samples
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024*8)

    def connect(self):
        self.s.connect(('127.0.0.1', 1234))

    def read_sample(self):
        try:
            sample = self.s.recv(8)
        except socket.error:
            return None

        return Sample.from_bytes(sample)

    def disconnect(self):
        self.s.shutdown()
        self.s = None

    def setblocking(self, val):
        self.s.setblocking(val)
