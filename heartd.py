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

# Train:
numas = 0
while True:
    f = reader.read(1)
    if ord(f[0]) == 0xAA:
        numas += 1
    else:
        numas = 0

    if numas == 2:
        break;

def pair2int(p):
    base = ord(p[0])
    base += ord(p[1]) * 256
    return base

clients = []

while True:
    millis = reader.read(2)
    fives = reader.read(2)
    sample = reader.read(2)
    aaas = reader.read(2)

    assert ord(fives[0]) == 0x55
    assert ord(fives[0]) == 0x55
    assert ord(aaas[0]) == 0xAA
    assert ord(aaas[1]) == 0xAA

    m = pair2int(millis)
    s = pair2int(sample)
    packed = struct.pack('LL', m, s)
    for x in clients:
        print "sending to a client lol"
        x.send(packed)

    #print "{},{}".format(pair2int(millis), pair2int(sample))

    try:
        u = netsock.accept()
        clients.append(u)
        print "got a client lol"
    except socket.error:
        pass

sock.close()

