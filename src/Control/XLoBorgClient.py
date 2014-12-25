#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import struct

s = socket.socket()         # Create a socket object
host = 'djb231.quns.cam.ac.uk'#socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service
s.connect((host, port))
for x in range(1000) :
    raw_input()
    s.send("accel")
    data=s.recv(1024)
    accel=struct.unpack('f'*(len(data)/4), data)

    s.send("mag")
    data=s.recv(1024)
    mag=struct.unpack('f'*(len(data)/4), data)

    print "X: ",accel[0]," Y: ",accel[1]," Z: ",accel[2]," mX: ",mag[0]," mY: ",mag[1]," mZ: ",mag[2]

s.send("")

s.close                     # Close the socket when done
