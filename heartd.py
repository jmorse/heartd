#!/usr/bin/python

import struct
import os
import io
import bluetooth
import socket

bd_addr = "20:15:12:08:63:95"

port = 1

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))

netsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
netsock.bind(('127.0.0.1', 1234))
netsock.listen(1)
netsock.setblocking(False)

sock.send("+++AT+BAUD8\r")
sock.setblocking(True)
sock.readable = lambda: True
sock.closed = False
reader = io.BufferedReader(sock)

def readinto(b):
    self = sock
    foo = self.recv(len(b))
    if len(foo) == 0:
        return 0
    i = 0
    for x in foo:
        b[i] = x
        i += 1
    return len(foo)

sock.readinto = readinto

# Assuming spoons are not forks, we should read a byte with high bits set, then
# with no high bits set, to synchronise. Burn bytes until this happens.
# Obviously this isn't guaranteed to complete, but the signal is sufficiently
# noisy for this to not generally be the case
numas = 0
while True:
    f = reader.read(1)
    if ord(f[0]) > 3 and numas == 0:
        numas = 1
    elif ord(f[0]) <= 3 and numas == 1:
        break
    else:
        numas = 0

def pair2int(p):
    base = ord(p[0])
    base += ord(p[1]) * 256
    return base

clients = set()

while True:
    sample = reader.read(2)
    assert ord(sample[1]) <= 3

    s = pair2int(sample)
    packed = struct.pack('I', s)
    ded = []
    for x in clients:
        try:
            x.send(packed)
        except socket.error:
            ded.append(x)

    for x in ded:
        clients.remove(x)

    #print "{},{}".format(pair2int(millis), pair2int(sample))

    try:
        conn, addr = netsock.accept()
        clients.add(conn)
    except socket.error:
        pass

sock.close()

